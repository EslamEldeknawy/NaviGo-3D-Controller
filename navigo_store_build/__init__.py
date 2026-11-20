bl_info = {
    "name": "NaviGo - 6-DOF 3D Navigation Controller",
    "author": "Eslam Eldeknawy (Eslam's Lab)",
    "version": (1, 0, 2),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar (N) > NaviGo",
    "description": "True proportional analog 6-DOF 3D viewport navigation for the NaviGo RP2040 controller",
    "category": "3D View",
}

import bpy
import os
import sys
import json
import time
import threading
import ctypes
from mathutils import Vector, Quaternion

if sys.platform == "win32":
    from ctypes import wintypes

# إضافة مسار الإضافة لاستيراد مكتبة serial المدمجة بدون الحاجة لـ pip
ADDON_DIR = os.path.dirname(os.path.realpath(__file__))
if ADDON_DIR not in sys.path:
    sys.path.insert(0, ADDON_DIR)

try:
    import serial
    import serial.tools.list_ports
    HAS_SERIAL = True
except ImportError:
    serial = None
    HAS_SERIAL = False

SETTINGS_PATH = os.path.join(ADDON_DIR, "navigo_settings.json")

DEFAULT_SETTINGS = {
    "master_speed": 1.0,
    "pan_speed": 0.03,
    "zoom_speed": 0.003,
    "orbit_speed": 0.012,
    "roll_speed": 0.015,
    "invert_x": False,
    "invert_y": False,
    "swap_xy": False,
    "invert_zoom": False,
    "theme": 0,
}

THEME_ITEMS = [
    ("0", "Rainbow", "Rainbow RGB cycle", 0),
    ("1", "The Matrix", "Matrix green cascade", 1),
    ("2", "Crimson Fire", "Warm fire glow", 2),
    ("3", "Ocean Wave", "Cool ocean blue-cyan", 3),
    ("4", "Aurora", "Northern lights blend", 4),
    ("5", "Stealth (Off)", "Turn off LEDs", 5),
]

stop_event = threading.Event()
packet_lock = threading.Lock()
latest_packet = None
connection_state = {"connected": False, "port": "", "dirty": False}
serial_thread = None
_is_loading_props = False
_last_wall_time = 0.0
_last_mono_time = 0.0


# ==========================================
# التحقق من أن نافذة Blender هي النشطة حالياً
# ==========================================
def is_app_focused():
    if sys.platform != "win32":
        return True
    try:
        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        if not hwnd or user32.IsIconic(hwnd):
            return False
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        return pid.value == os.getpid()
    except Exception:
        return True


# ==========================================
# حفظ وتحميل الإعدادات
# ==========================================
def load_settings_dict():
    data = DEFAULT_SETTINGS.copy()
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                data.update(json.load(f))
        except Exception:
            pass
    return data


def save_settings_from_props(props):
    if _is_loading_props:
        return
    data = {
        "master_speed": round(float(props.master_speed), 3),
        "pan_speed": round(float(props.pan_speed), 4),
        "orbit_speed": round(float(props.orbit_speed), 4),
        "zoom_speed": round(float(props.zoom_speed), 4),
        "roll_speed": round(float(props.roll_speed), 4),
        "invert_x": bool(props.invert_x),
        "invert_y": bool(props.invert_y),
        "swap_xy": bool(props.swap_xy),
        "invert_zoom": bool(props.invert_zoom),
        "theme": int(props.theme),
    }
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass


def apply_dict_to_props(props, data):
    global _is_loading_props
    _is_loading_props = True
    try:
        props.master_speed = float(data.get("master_speed", 1.0))
        props.pan_speed = float(data.get("pan_speed", 0.03))
        props.orbit_speed = float(data.get("orbit_speed", 0.012))
        props.zoom_speed = float(data.get("zoom_speed", 0.003))
        props.roll_speed = float(data.get("roll_speed", 0.015))
        props.invert_x = bool(data.get("invert_x", False))
        props.invert_y = bool(data.get("invert_y", False))
        props.swap_xy = bool(data.get("swap_xy", False))
        props.invert_zoom = bool(data.get("invert_zoom", False))
        theme_str = str(int(data.get("theme", 0)))
        if theme_str in {"0", "1", "2", "3", "4", "5"}:
            props.theme = theme_str
    finally:
        _is_loading_props = False


# ==========================================
# البحث التلقائي عن منفذ NaviGo
# ==========================================
def find_navigo_port():
    if not HAS_SERIAL:
        return None
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if p.serial_number and "NAVIGO" in p.serial_number.upper():
            return p.device
    for p in ports:
        desc = (p.description or "") + " " + (p.product or "")
        if "NAVIGO" in desc.upper():
            return p.device
    for p in ports:
        if p.vid == 0x2E8A:
            return p.device
    return None


# ==========================================
# ثريد استقبال وإرسال بيانات السيريال (مع التعافي بعد Sleep)
# ==========================================
class NaviGoSerialThread(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.ser = None
        self.lock = threading.Lock()
        self.force_reconnect = False
        self.reconnect_delay = 0.0

    def send_command(self, cmd_str):
        with self.lock:
            try:
                if self.ser and self.ser.is_open:
                    self.ser.write(cmd_str.encode("utf-8"))
            except Exception:
                pass

    def trigger_reconnect(self, delay=0.0):
        self.reconnect_delay = max(self.reconnect_delay, float(delay))
        self.force_reconnect = True

    def _close_serial(self):
        with self.lock:
            if self.ser:
                try:
                    self.ser.close()
                except Exception:
                    pass
                self.ser = None

    def run(self):
        global latest_packet
        was_connected = False
        active_port = ""
        health_counter = 0

        while not stop_event.is_set():
            if not HAS_SERIAL:
                stop_event.wait(2.0)
                continue

            try:
                if self.force_reconnect:
                    self.force_reconnect = False
                    delay = self.reconnect_delay
                    self.reconnect_delay = 0.0
                    self._close_serial()
                    active_port = ""
                    if was_connected:
                        was_connected = False
                        connection_state["connected"] = False
                        connection_state["port"] = ""
                        connection_state["dirty"] = True
                    if delay > 0.0 and stop_event.wait(delay):
                        break

                if self.ser is None or not self.ser.is_open:
                    port = find_navigo_port()
                    if not port:
                        stop_event.wait(1.0)
                        continue

                    ser = serial.Serial(port, 115200, timeout=0.05)
                    ser.dtr = True
                    ser.rts = True
                    if stop_event.wait(0.15):
                        ser.close()
                        break
                    ser.reset_input_buffer()

                    with self.lock:
                        self.ser = ser

                    active_port = port
                    health_counter = 0
                    was_connected = True
                    connection_state["connected"] = True
                    connection_state["port"] = port
                    connection_state["dirty"] = True

                    # استرجاع ثيم الإضاءة المحفوظ عند الاتصال أو بعد Sleep
                    saved_theme = int(load_settings_dict().get("theme", 0))
                    self.send_command(f"T{saved_theme}")

                # فحص دوري لصحة منفذ الويندوز كل ~1 ثانية لاكتشاف أي فصل صامت
                health_counter += 1
                if health_counter >= 80:
                    health_counter = 0
                    with self.lock:
                        if self.ser:
                            _ = self.ser.cts
                    if find_navigo_port() != active_port:
                        raise OSError("NaviGo port disconnected or re-enumerated")

                if self.ser and self.ser.in_waiting > 0:
                    raw_data = self.ser.read(self.ser.in_waiting).decode("utf-8", errors="ignore")
                    lines = raw_data.strip().split("\n")
                    if lines:
                        last_line = lines[-1].strip()
                        if last_line.count(",") == 5 and any(c not in "0,.-" for c in last_line):
                            parts = last_line.split(",")
                            if len(parts) == 6:
                                vals = tuple(float(v) for v in parts)
                                with packet_lock:
                                    latest_packet = vals

                stop_event.wait(0.012)

            except Exception:
                self._close_serial()
                active_port = ""

                if was_connected:
                    was_connected = False
                    connection_state["connected"] = False
                    connection_state["port"] = ""
                    connection_state["dirty"] = True

                stop_event.wait(1.0)

        self._close_serial()


# ==========================================
# تحديث كاميرا الـ 3D Viewport في Blender
# ==========================================
def get_target_view3d():
    wm = bpy.context.window_manager
    if not wm:
        return None, None
    best_area = None
    best_rv3d = None
    best_score = -1

    for win in wm.windows:
        if not win.screen:
            continue
        for area in win.screen.areas:
            if area.type == "VIEW_3D":
                space = area.spaces.active
                rv3d = getattr(space, "region_3d", None)
                if rv3d:
                    score = area.width * area.height
                    if score > best_score:
                        best_score = score
                        best_area = area
                        best_rv3d = rv3d
    return best_area, best_rv3d


def redraw_all_view3d():
    wm = bpy.context.window_manager
    if not wm:
        return
    for win in wm.windows:
        if not win.screen:
            continue
        for area in win.screen.areas:
            if area.type == "VIEW_3D":
                area.tag_redraw()


def navigo_timer():
    global latest_packet, _last_wall_time, _last_mono_time

    if stop_event.is_set():
        return None

    # اكتشاف استيقاظ الكمبيوتر من Sleep / Hibernate تلقائياً
    now_wall = time.time()
    now_mono = time.monotonic()
    if _last_wall_time > 0.0 and _last_mono_time > 0.0:
        if (now_wall - _last_wall_time > 2.5) or (now_mono - _last_mono_time > 2.5):
            if serial_thread:
                serial_thread.trigger_reconnect(delay=0.8)
    _last_wall_time = now_wall
    _last_mono_time = now_mono

    if connection_state["dirty"]:
        connection_state["dirty"] = False
        redraw_all_view3d()

    pkt = None
    with packet_lock:
        if latest_packet is not None:
            pkt = latest_packet
            latest_packet = None

    if pkt is not None and is_app_focused():
        x, y, z, rx, ry, rz = pkt
        if x != 0.0 or y != 0.0 or z != 0.0 or rx != 0.0 or ry != 0.0 or rz != 0.0:
            wm = bpy.context.window_manager
            props = getattr(wm, "navigo_props", None)
            area, rv3d = get_target_view3d()

            if props and area and rv3d:
                if props.swap_xy:
                    x, y = y, x
                    rx, ry = ry, rx

                inv_x = -1.0 if props.invert_x else 1.0
                inv_y = -1.0 if props.invert_y else 1.0
                inv_z = -1.0 if props.invert_zoom else 1.0
                m = props.master_speed

                x *= inv_x
                y *= inv_y
                z *= inv_z
                ry *= inv_x
                rx *= inv_y

                pan_s = props.pan_speed * m
                zoom_s = props.zoom_speed * m
                orbit_s = props.orbit_speed * m
                roll_s = props.roll_speed * m

                # 1. PAN
                if x != 0.0 or y != 0.0:
                    scale_factor = max(rv3d.view_distance * 0.015, 0.02)
                    local_pan = Vector((x * pan_s * scale_factor, -y * pan_s * scale_factor, 0.0))
                    rv3d.view_location += rv3d.view_rotation @ local_pan

                # 2. ZOOM
                if z != 0.0:
                    zoom_factor = 1.0 - (z * zoom_s * 0.1)
                    new_dist = rv3d.view_distance * zoom_factor
                    rv3d.view_distance = max(0.001, min(100000.0, new_dist))

                # 3. ORBIT & 4. ROLL
                if rx != 0.0 or ry != 0.0 or rz != 0.0:
                    q_yaw = Quaternion((0.0, 1.0, 0.0), -ry * orbit_s)
                    q_pitch = Quaternion((1.0, 0.0, 0.0), rx * orbit_s)
                    q_roll = Quaternion((0.0, 0.0, 1.0), -rz * roll_s)
                    rv3d.view_rotation = (rv3d.view_rotation @ q_yaw @ q_pitch @ q_roll).normalized()

                area.tag_redraw()

    return 0.015


# ==========================================
# خصائص وأزرار واجهة Blender (N-Panel)
# ==========================================
def on_prop_update(self, context):
    save_settings_from_props(self)


def on_theme_update(self, context):
    save_settings_from_props(self)
    if serial_thread and not _is_loading_props:
        serial_thread.send_command(f"T{self.theme}")


class NaviGoProperties(bpy.types.PropertyGroup):
    master_speed: bpy.props.FloatProperty(
        name="Master Speed", default=1.0, min=0.2, max=3.0, step=10, precision=1,
        options={"SKIP_SAVE"}, update=on_prop_update
    )
    pan_speed: bpy.props.FloatProperty(
        name="Pan", default=0.030, min=0.005, max=0.100, step=0.5, precision=3,
        options={"SKIP_SAVE"}, update=on_prop_update
    )
    orbit_speed: bpy.props.FloatProperty(
        name="Orbit", default=0.012, min=0.002, max=0.040, step=0.2, precision=3,
        options={"SKIP_SAVE"}, update=on_prop_update
    )
    zoom_speed: bpy.props.FloatProperty(
        name="Zoom", default=0.003, min=0.001, max=0.015, step=0.1, precision=3,
        options={"SKIP_SAVE"}, update=on_prop_update
    )
    roll_speed: bpy.props.FloatProperty(
        name="Roll", default=0.015, min=0.002, max=0.040, step=0.2, precision=3,
        options={"SKIP_SAVE"}, update=on_prop_update
    )
    invert_x: bpy.props.BoolProperty(
        name="Invert X", default=False, options={"SKIP_SAVE"}, update=on_prop_update
    )
    invert_y: bpy.props.BoolProperty(
        name="Invert Y", default=False, options={"SKIP_SAVE"}, update=on_prop_update
    )
    swap_xy: bpy.props.BoolProperty(
        name="Swap X <-> Y", default=False, options={"SKIP_SAVE"}, update=on_prop_update
    )
    invert_zoom: bpy.props.BoolProperty(
        name="Invert Zoom", default=False, options={"SKIP_SAVE"}, update=on_prop_update
    )
    theme: bpy.props.EnumProperty(
        name="LED Theme", items=THEME_ITEMS, default="0",
        options={"SKIP_SAVE"}, update=on_theme_update
    )


class NAVIGO_OT_calibrate(bpy.types.Operator):
    bl_idname = "navigo.calibrate"
    bl_label = "Re-Zero (Calibrate)"
    bl_description = "Send Re-Zero center calibration command to NaviGo controller"

    def execute(self, context):
        if serial_thread:
            serial_thread.send_command("Z")
        self.report({"INFO"}, "NaviGo Re-Zero Calibrated")
        return {"FINISHED"}


class NAVIGO_OT_reset_defaults(bpy.types.Operator):
    bl_idname = "navigo.reset_defaults"
    bl_label = "Reset Defaults"
    bl_description = "Reset all NaviGo speeds and axis settings to defaults"

    def execute(self, context):
        props = context.window_manager.navigo_props
        apply_dict_to_props(props, DEFAULT_SETTINGS)
        save_settings_from_props(props)
        if serial_thread:
            serial_thread.send_command("T0")
        self.report({"INFO"}, "NaviGo Settings Reset to Defaults")
        return {"FINISHED"}


class NAVIGO_OT_reconnect(bpy.types.Operator):
    bl_idname = "navigo.reconnect"
    bl_label = "Reconnect"
    bl_description = "Rescan USB ports and reconnect to NaviGo"

    def execute(self, context):
        if serial_thread:
            serial_thread.trigger_reconnect(delay=0.1)
        return {"FINISHED"}


class NAVIGO_PT_main_panel(bpy.types.Panel):
    bl_label = "NaviGo V1.0"
    bl_idname = "NAVIGO_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "NaviGo"

    def draw(self, context):
        layout = self.layout
        props = context.window_manager.navigo_props

        # حالة الاتصال
        box = layout.box()
        row = box.row(align=True)
        if not HAS_SERIAL:
            row.label(text="Missing 'serial' folder!", icon="ERROR")
        elif connection_state["connected"]:
            row.label(text=f"Connected ({connection_state['port']})", icon="CHECKMARK")
            row.operator("navigo.reconnect", text="", icon="FILE_REFRESH")
        else:
            row.label(text="Waiting for NaviGo...", icon="TIME")
            row.operator("navigo.reconnect", text="", icon="FILE_REFRESH")

        # التحكم في السرعات
        box = layout.box()
        box.label(text="Speed Controls", icon="PREFERENCES")
        col = box.column(align=True)
        col.prop(props, "master_speed", slider=True)
        col.prop(props, "pan_speed", slider=True)
        col.prop(props, "orbit_speed", slider=True)
        col.prop(props, "zoom_speed", slider=True)
        col.prop(props, "roll_speed", slider=True)

        # اتجاه المحاور
        box = layout.box()
        box.label(text="Axis & Direction", icon="ORIENTATION_VIEW")
        grid = box.grid_flow(row_major=True, columns=2, even_columns=True, align=True)
        grid.prop(props, "invert_x", toggle=True)
        grid.prop(props, "invert_y", toggle=True)
        grid.prop(props, "swap_xy", toggle=True)
        grid.prop(props, "invert_zoom", toggle=True)

        # ألوان الإضاءة
        box = layout.box()
        box.label(text="LED Lighting Theme", icon="LIGHT")
        grid = box.grid_flow(row_major=True, columns=2, even_columns=True, align=True)
        grid.prop(props, "theme", expand=True)

        # أزرار المعايرة وإعادة الضبط
        row = layout.row(align=True)
        row.scale_y = 1.25
        row.operator("navigo.calibrate", icon="ORIENTATION_CURSOR")
        row.operator("navigo.reset_defaults", icon="LOOP_BACK")


classes = (
    NaviGoProperties,
    NAVIGO_OT_calibrate,
    NAVIGO_OT_reset_defaults,
    NAVIGO_OT_reconnect,
    NAVIGO_PT_main_panel,
)


def register():
    global serial_thread, _last_wall_time, _last_mono_time
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.navigo_props = bpy.props.PointerProperty(type=NaviGoProperties)

    if bpy.context.window_manager:
        apply_dict_to_props(bpy.context.window_manager.navigo_props, load_settings_dict())

    _last_wall_time = time.time()
    _last_mono_time = time.monotonic()

    stop_event.clear()
    serial_thread = NaviGoSerialThread()
    serial_thread.start()

    if not bpy.app.timers.is_registered(navigo_timer):
        bpy.app.timers.register(navigo_timer, first_interval=0.1, persistent=True)


def unregister():
    global serial_thread
    stop_event.set()

    if bpy.app.timers.is_registered(navigo_timer):
        bpy.app.timers.unregister(navigo_timer)

    if serial_thread and serial_thread.is_alive():
        serial_thread.join(timeout=0.3)
    serial_thread = None

    if hasattr(bpy.types.WindowManager, "navigo_props"):
        del bpy.types.WindowManager.navigo_props

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()