# -*- coding: utf-8 -*-
# NaviGo V1.0 - 6-DOF 3D Navigation Controller Add-on for FreeCAD
# Author: Eslam Eldeknawy (Eslam's Lab)

import os
import sys
import json
import time
import threading
import ctypes

import FreeCAD
import FreeCADGui
from pivy import coin
from PySide import QtCore, QtGui, QtWidgets

if sys.platform == "win32":
    from ctypes import wintypes

QActionCompat = getattr(QtGui, "QAction", None) or getattr(QtWidgets, "QAction", None)
QT_HORIZONTAL = getattr(QtCore.Qt, "Horizontal", None) or QtCore.Qt.Orientation.Horizontal
QT_RIGHT_DOCK = getattr(QtCore.Qt, "RightDockWidgetArea", None) or QtCore.Qt.DockWidgetArea.RightDockWidgetArea

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

THEME_NAMES = [
    "Rainbow",
    "The Matrix",
    "Crimson Fire",
    "Ocean Wave",
    "Aurora",
    "Stealth (Off)",
]

settings = DEFAULT_SETTINGS.copy()
stop_event = threading.Event()
packet_lock = threading.Lock()
latest_packet = None
connection_state = {"connected": False, "port": "", "dirty": False}

_serial_thread = None
_navigo_timer = None
_navigo_dock = None
_navigo_action = None
_last_wall_time = 0.0
_last_mono_time = 0.0
_boot_attempts = 0
_bootstrapped = False
_scheduled = False


# ==========================================
# التحقق من أن نافذة FreeCAD هي النشطة حالياً
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
def load_settings():
    global settings
    settings = DEFAULT_SETTINGS.copy()
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                settings.update(json.load(f))
        except Exception:
            pass


def save_settings():
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
    except Exception:
        pass


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

                    self.send_command(f"T{int(settings.get('theme', 0))}")

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
# تحديث كاميرا الـ 3D Viewport في FreeCAD (Coin3D)
# ==========================================
def apply_camera_move(pkt):
    doc = FreeCADGui.ActiveDocument
    if not doc:
        return
    view = doc.ActiveView
    if not view or not hasattr(view, "getCameraNode"):
        return
    cam = view.getCameraNode()
    if not cam:
        return

    x, y, z, rx, ry, rz = pkt
    if x == 0.0 and y == 0.0 and z == 0.0 and rx == 0.0 and ry == 0.0 and rz == 0.0:
        return

    if settings.get("swap_xy", False):
        x, y = y, x
        rx, ry = ry, rx

    inv_x = -1.0 if settings.get("invert_x", False) else 1.0
    inv_y = -1.0 if settings.get("invert_y", False) else 1.0
    inv_z = -1.0 if settings.get("invert_zoom", False) else 1.0
    m = float(settings.get("master_speed", 1.0))

    x *= inv_x
    y *= inv_y
    z *= inv_z
    ry *= inv_x
    rx *= inv_y

    pan_s = float(settings.get("pan_speed", 0.03)) * m
    zoom_s = float(settings.get("zoom_speed", 0.003)) * m
    orbit_s = float(settings.get("orbit_speed", 0.012)) * m
    roll_s = float(settings.get("roll_speed", 0.015)) * m

    pos = cam.position.getValue()
    orient = cam.orientation.getValue()
    focal = float(cam.focalDistance.getValue())
    if focal <= 0.001:
        focal = 10.0

    forward = orient.multVec(coin.SbVec3f(0.0, 0.0, -1.0))
    right = orient.multVec(coin.SbVec3f(1.0, 0.0, 0.0))
    up = orient.multVec(coin.SbVec3f(0.0, 1.0, 0.0))

    target = pos + (forward * focal)
    is_ortho = isinstance(cam, coin.SoOrthographicCamera)

    # 1. PAN
    if x != 0.0 or y != 0.0:
        ref_dist = float(cam.height.getValue()) if is_ortho else focal
        scale_factor = max(ref_dist * 0.015, 0.02)
        delta_pan = (right * (x * pan_s * scale_factor)) + (up * (-y * pan_s * scale_factor))
        pos = pos + delta_pan
        target = target + delta_pan

    # 2. ZOOM
    if z != 0.0:
        zoom_factor = max(0.5, min(1.5, 1.0 - (z * zoom_s * 0.1)))
        if is_ortho:
            new_height = max(0.001, min(100000.0, float(cam.height.getValue()) * zoom_factor))
            cam.height.setValue(new_height)
        focal = max(0.01, min(100000.0, focal * zoom_factor))
        pos = target - (forward * focal)

    # 3. ORBIT & 4. ROLL
    if rx != 0.0 or ry != 0.0 or rz != 0.0:
        q_yaw = coin.SbRotation(coin.SbVec3f(0.0, 1.0, 0.0), -ry * orbit_s)
        q_pitch = coin.SbRotation(coin.SbVec3f(1.0, 0.0, 0.0), rx * orbit_s)
        q_roll = coin.SbRotation(coin.SbVec3f(0.0, 0.0, 1.0), -rz * roll_s)
        orient = coin.SbRotation((orient * q_yaw * q_pitch * q_roll).getValue())
        new_forward = orient.multVec(coin.SbVec3f(0.0, 0.0, -1.0))
        pos = target - (new_forward * focal)

    cam.orientation.setValue(orient)
    cam.position.setValue(pos)
    cam.focalDistance.setValue(focal)


def _on_timer_tick():
    global latest_packet, _last_wall_time, _last_mono_time

    if stop_event.is_set():
        return

    now_wall = time.time()
    now_mono = time.monotonic()
    if _last_wall_time > 0.0 and _last_mono_time > 0.0:
        if (now_wall - _last_wall_time > 2.5) or (now_mono - _last_mono_time > 2.5):
            if _serial_thread:
                _serial_thread.trigger_reconnect(delay=0.8)
    _last_wall_time = now_wall
    _last_mono_time = now_mono

    if connection_state["dirty"]:
        connection_state["dirty"] = False
        if _navigo_dock and _navigo_dock.widget():
            _navigo_dock.widget().refresh_status()

    pkt = None
    with packet_lock:
        if latest_packet is not None:
            pkt = latest_packet
            latest_packet = None

    if pkt is not None and is_app_focused():
        try:
            apply_camera_move(pkt)
        except Exception as e:
            FreeCAD.Console.PrintWarning(f"NaviGo Camera Error: {e}\n")


# ==========================================
# لوحة التحكم المدمجة (Dark-Mode Dock Widget)
# ==========================================
PANEL_QSS = """
QWidget#NaviGoRoot {
    background-color: #181a1f;
    color: #e6e9ef;
    font-family: "Segoe UI", sans-serif;
    font-size: 12px;
}
QFrame.Card {
    background-color: #22262e;
    border: 1px solid #2f3542;
    border-radius: 8px;
}
QLabel.SectionTitle {
    color: #8b95a5;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 0.6px;
}
QLabel.ValLabel {
    color: #00d2ff;
    font-weight: bold;
}
QSlider::groove:horizontal {
    height: 5px;
    background: #14161a;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #00d2ff;
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
}
QPushButton.ToggleBtn, QPushButton.ThemeBtn {
    background-color: #1b1e24;
    color: #e6e9ef;
    border: 1px solid #2f3542;
    border-radius: 6px;
    padding: 6px 8px;
    font-weight: bold;
}
QPushButton.ToggleBtn:checked, QPushButton.ThemeBtn:checked {
    border-color: #00d2ff;
    background-color: #16323d;
    color: #00d2ff;
}
QPushButton.ActionBtn {
    background-color: #282e38;
    color: #e6e9ef;
    border: 1px solid #2f3542;
    border-radius: 6px;
    padding: 7px 10px;
    font-weight: bold;
}
QPushButton.ActionBtn:hover {
    border-color: #00d2ff;
}
"""


class NaviGoControlWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("NaviGoRoot")
        self.setStyleSheet(PANEL_QSS)
        self._syncing = False
        self._sliders = {}
        self._val_labels = {}
        self._toggles = {}
        self._theme_btns = []
        self._build_ui()
        self.sync_from_settings()
        self.refresh_status()

    def _make_card(self, title_text):
        card = QtWidgets.QFrame()
        card.setProperty("class", "Card")
        v = QtWidgets.QVBoxLayout(card)
        v.setContentsMargins(10, 8, 10, 10)
        v.setSpacing(6)
        lbl = QtWidgets.QLabel(title_text.upper())
        lbl.setProperty("class", "SectionTitle")
        v.addWidget(lbl)
        return card, v

    def _build_ui(self):
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(8)

        hdr = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("NaviGo V1.0")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;")
        self.badge = QtWidgets.QLabel("Waiting for NaviGo...")
        self.badge.setStyleSheet("padding: 3px 8px; border-radius: 10px; font-size: 11px; font-weight: bold;")
        btn_refresh = QtWidgets.QPushButton("↻")
        btn_refresh.setFixedSize(26, 24)
        btn_refresh.setToolTip("Reconnect USB Port")
        btn_refresh.setProperty("class", "ActionBtn")
        btn_refresh.clicked.connect(lambda: _serial_thread and _serial_thread.trigger_reconnect(0.1))

        hdr.addWidget(title)
        hdr.addStretch()
        hdr.addWidget(self.badge)
        hdr.addWidget(btn_refresh)
        root.addLayout(hdr)

        speed_card, sv = self._make_card("Speed Controls")
        slider_specs = [
            ("master_speed", "Master Speed", 2, 30, 10.0, "{:.1f}x"),
            ("pan_speed", "Pan", 5, 100, 1000.0, "{:.3f}"),
            ("orbit_speed", "Orbit", 2, 40, 1000.0, "{:.3f}"),
            ("zoom_speed", "Zoom", 1, 15, 1000.0, "{:.3f}"),
            ("roll_speed", "Roll", 2, 40, 1000.0, "{:.3f}"),
        ]
        for key, label, mn, mx, scale, fmt in slider_specs:
            row_h = QtWidgets.QHBoxLayout()
            lbl_n = QtWidgets.QLabel(label)
            lbl_v = QtWidgets.QLabel("")
            lbl_v.setProperty("class", "ValLabel")
            row_h.addWidget(lbl_n)
            row_h.addStretch()
            row_h.addWidget(lbl_v)
            sv.addLayout(row_h)

            sld = QtWidgets.QSlider(QT_HORIZONTAL)
            sld.setMinimum(mn)
            sld.setMaximum(mx)
            sld.valueChanged.connect(lambda val, k=key, sc=scale, f=fmt: self._on_slider(k, val / sc, f))
            sv.addWidget(sld)
            self._sliders[key] = (sld, scale, fmt)
            self._val_labels[key] = lbl_v

        root.addWidget(speed_card)

        axis_card, av = self._make_card("Axis & Direction")
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(6)
        toggle_specs = [
            ("invert_x", "Invert X", 0, 0),
            ("invert_y", "Invert Y", 0, 1),
            ("swap_xy", "Swap X ↔ Y", 1, 0),
            ("invert_zoom", "Invert Zoom", 1, 1),
        ]
        for key, text, r, c in toggle_specs:
            btn = QtWidgets.QPushButton(text)
            btn.setCheckable(True)
            btn.setProperty("class", "ToggleBtn")
            btn.toggled.connect(lambda checked, k=key: self._on_toggle(k, checked))
            grid.addWidget(btn, r, c)
            self._toggles[key] = btn
        av.addLayout(grid)
        root.addWidget(axis_card)

        theme_card, tv = self._make_card("LED Lighting Theme")
        tgrid = QtWidgets.QGridLayout()
        tgrid.setSpacing(6)
        for idx, name in enumerate(THEME_NAMES):
            btn = QtWidgets.QPushButton(name)
            btn.setCheckable(True)
            btn.setProperty("class", "ThemeBtn")
            btn.clicked.connect(lambda _=False, i=idx: self._on_theme(i))
            tgrid.addWidget(btn, idx // 2, idx % 2)
            self._theme_btns.append(btn)
        tv.addLayout(tgrid)
        root.addWidget(theme_card)

        act_row = QtWidgets.QHBoxLayout()
        btn_cal = QtWidgets.QPushButton("Re-Zero (Calibrate)")
        btn_cal.setProperty("class", "ActionBtn")
        btn_cal.clicked.connect(self._on_calibrate)

        btn_rst = QtWidgets.QPushButton("Reset Defaults")
        btn_rst.setProperty("class", "ActionBtn")
        btn_rst.clicked.connect(self._on_reset)

        act_row.addWidget(btn_cal)
        act_row.addWidget(btn_rst)
        root.addLayout(act_row)
        root.addStretch()

    def refresh_status(self):
        if not HAS_SERIAL:
            self.badge.setText("Missing 'serial' lib")
            self.badge.setStyleSheet("background:#2c2024; color:#ff5c5c; padding:3px 8px; border-radius:10px; font-weight:bold;")
        elif connection_state["connected"]:
            self.badge.setText(f"Connected ({connection_state['port']})")
            self.badge.setStyleSheet("background:#193024; color:#2ecc71; padding:3px 8px; border-radius:10px; font-weight:bold;")
        else:
            self.badge.setText("Waiting for NaviGo...")
            self.badge.setStyleSheet("background:#2c2024; color:#ff5c5c; padding:3px 8px; border-radius:10px; font-weight:bold;")

    def sync_from_settings(self):
        self._syncing = True
        try:
            for key, (sld, scale, fmt) in self._sliders.items():
                val = float(settings.get(key, DEFAULT_SETTINGS[key]))
                sld.setValue(int(round(val * scale)))
                self._val_labels[key].setText(fmt.format(val))
            for key, btn in self._toggles.items():
                btn.setChecked(bool(settings.get(key, False)))
            cur_theme = int(settings.get("theme", 0))
            for i, btn in enumerate(self._theme_btns):
                btn.setChecked(i == cur_theme)
        finally:
            self._syncing = False

    def _on_slider(self, key, val, fmt):
        self._val_labels[key].setText(fmt.format(val))
        if not self._syncing:
            settings[key] = round(val, 4)
            save_settings()

    def _on_toggle(self, key, checked):
        if not self._syncing:
            settings[key] = bool(checked)
            save_settings()

    def _on_theme(self, theme_id):
        settings["theme"] = int(theme_id)
        save_settings()
        self.sync_from_settings()
        if _serial_thread:
            _serial_thread.send_command(f"T{theme_id}")

    def _on_calibrate(self):
        if _serial_thread:
            _serial_thread.send_command("Z")
        FreeCAD.Console.PrintMessage("NaviGo: Re-Zero Calibrated\n")

    def _on_reset(self):
        global settings
        settings = DEFAULT_SETTINGS.copy()
        save_settings()
        self.sync_from_settings()
        if _serial_thread:
            _serial_thread.send_command("T0")
        FreeCAD.Console.PrintMessage("NaviGo: Settings Reset to Defaults\n")


def toggle_navigo_panel():
    global _navigo_dock
    mw = FreeCADGui.getMainWindow()
    if not mw:
        return
    if _navigo_dock is None:
        _navigo_dock = QtWidgets.QDockWidget("NaviGo Control Panel", mw)
        _navigo_dock.setObjectName("NaviGo_Control_Dock")
        _navigo_dock.setWidget(NaviGoControlWidget(_navigo_dock))
        mw.addDockWidget(QT_RIGHT_DOCK, _navigo_dock)
    else:
        _navigo_dock.setVisible(not _navigo_dock.isVisible())
    if _navigo_dock.isVisible() and _navigo_dock.widget():
        _navigo_dock.widget().sync_from_settings()
        _navigo_dock.widget().refresh_status()


def _ensure_menu_and_toolbar():
    global _navigo_action
    mw = FreeCADGui.getMainWindow()
    if not mw or not QActionCompat:
        return

    if _navigo_action is None:
        _navigo_action = mw.findChild(QActionCompat, "NaviGo_Settings_Action")
    if _navigo_action is None:
        _navigo_action = QActionCompat("NaviGo Settings", mw)
        _navigo_action.setObjectName("NaviGo_Settings_Action")
        _navigo_action.setToolTip("Open NaviGo 6-DOF Controller Panel")
        _navigo_action.triggered.connect(toggle_navigo_panel)

    menubar = mw.menuBar()
    if menubar:
        for m_act in menubar.actions():
            menu = m_act.menu()
            if menu and ("tools" in m_act.text().replace("&", "").lower() or "أدوات" in m_act.text()):
                if _navigo_action not in menu.actions():
                    menu.addSeparator()
                    menu.addAction(_navigo_action)
                break

    tb = mw.findChild(QtWidgets.QToolBar, "NaviGo_Toolbar")
    if not tb:
        tb = mw.addToolBar("NaviGo")
        tb.setObjectName("NaviGo_Toolbar")
        tb.addAction(_navigo_action)


def _bootstrap_navigo():
    global _serial_thread, _navigo_timer, _last_wall_time, _last_mono_time, _bootstrapped
    if _bootstrapped:
        return
    try:
        load_settings()
        _ensure_menu_and_toolbar()

        mw = FreeCADGui.getMainWindow()
        if mw and hasattr(mw, "workbenchActivated"):
            mw.workbenchActivated.connect(lambda _name: QtCore.QTimer.singleShot(200, _ensure_menu_and_toolbar))

        _last_wall_time = time.time()
        _last_mono_time = time.monotonic()

        stop_event.clear()
        _serial_thread = NaviGoSerialThread()
        _serial_thread.start()

        _navigo_timer = QtCore.QTimer()
        _navigo_timer.timeout.connect(_on_timer_tick)
        _navigo_timer.start(15)

        _bootstrapped = True
        FreeCAD.Console.PrintMessage("NaviGo V1.0 Add-on Started (Background Service Active)\n")
    except Exception as e:
        FreeCAD.Console.PrintError(f"NaviGo Startup Failed: {e}\n")


def _try_bootstrap():
    global _boot_attempts
    _boot_attempts += 1
    if not getattr(FreeCAD, "GuiUp", False) or FreeCADGui.getMainWindow() is None:
        if _boot_attempts < 40:
            QtCore.QTimer.singleShot(500, _try_bootstrap)
        return
    _bootstrap_navigo()


def schedule_start(addon_dir=None):
    global _scheduled, ADDON_DIR, SETTINGS_PATH
    if addon_dir:
        ADDON_DIR = addon_dir
        SETTINGS_PATH = os.path.join(ADDON_DIR, "navigo_settings.json")
    if not _scheduled:
        _scheduled = True
        QtCore.QTimer.singleShot(800, _try_bootstrap)