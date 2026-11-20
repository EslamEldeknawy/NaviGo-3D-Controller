NaviGo V1.0 — Universal Open-Source 6-DOF 3D Navigation Controller

> **Print. Build. Navigate.**






<!-- استبدل السطر اللي فوق بصورتك الرئيسية للماوس عن طريق سحب الصورة وإفلاتها هنا في محرر GitHub -->

**NaviGo V1.0** is a universal, open-source, proportional 6-DOF (Six Degrees of Freedom) 3D navigation controller engineered for **Autodesk Fusion 360**, **Blender**, and **FreeCAD**. Powered by a **Raspberry Pi Pico (RP2040)**, an **ADXL335** analog accelerometer, and zero-force capacitive touch sensors, it communicates natively with each application's 3D camera API—keeping your regular mouse cursor 100% free while you pan, orbit, zoom, and roll simultaneously.

All supported applications run on the **exact same unified RP2040 firmware**—no reflashing or hardware changes required when switching between programs.

---

## Supported Software

| Software | Integration Type | Control Panel UI | Status |
| :--- | :--- | :--- | :--- |
| **Autodesk Fusion 360** | Native Camera API Add-in (`Python`) | Dockable Dark-Mode HTML Panel | Supported (One-Click Installer) |
| **Blender (3.0 – 4.x+)** | Native `RegionView3D` Add-on (`bpy`) | Integrated `View3D → Sidebar (N) → NaviGo` | Supported (Submitted to Blender Extensions) |
| **FreeCAD (0.21 – 1.x+)** | Native `Coin3D` Camera Module (`PySide`) | Dockable Dark-Mode Qt Control Panel | Supported |

*Want to add support for another CAD/3D tool (such as Inventor, Rhino, or Onshape)? NaviGo outputs clean 6-axis serial telemetry (`x,y,z,rx,ry,rz` at `115200` baud), making it easy to write companion plugins for any software with a camera API.*

---

## Get the Hardware & Software

- **3D Printable Files (STL / 3MF) & Illustrated Assembly Guide:** [Download on Cults3D](https://cults3d.com/:5250150)
- **Custom 4-LED RGB PCB (Order Ready-Made):** [Order on PCBWay](https://www.pcbway.com/project/shareproject/NaviGo_V1_0_DIY_6_DOF_3D_Navigation_Controller_for_Autodesk_Fusion_360_4f7429b3.html)
- **Full Illustrated Build Guide & Schematics:** [View on Hackster.io](https://www.hackster.io/eslam-eldeknawy/navigo-v1-0-diy-6-dof-cad-navigation-mouse-for-fusion-360-744629)
- **Free Unified Firmware, Add-ins & User Manuals:** [Download Latest Release on GitHub](https://github.com/EslamEldeknawy/NaviGo-3D-Controller/releases/latest)

---

## Key Features

- **Universal Unified Firmware:** One `.uf2` firmware file works seamlessly across Fusion 360, Blender, and FreeCAD without reflashing.
- **True Proportional 6-DOF Control:** Smooth simultaneous Pan, Orbit, Proportional Zoom, and Horizon Roll while keeping your standard desktop mouse completely free.
- **Zero-Force Capacitive Touch:** Top and side touch sensors eliminate mechanical microswitch click forces so the controller stays planted on your desk.
- **Plug & Play Auto-Connection:** Automatically detects NaviGo's USB serial port, reconnects seamlessly if unplugged, and auto-recovers after Windows Sleep/Wake—no manual COM port setup required.
- **Smart Focus Awareness:** Automatically freezes viewport camera movement whenever your 3D software is minimized or unfocused.
- **Live Speed & Axis Customization:** Adjust Master, Pan, Orbit, Zoom, and Roll speeds, invert/swap axes, and trigger software `Re-Zero` calibration in real time.
- **6 Built-in WS2812B RGB Themes:** *Rainbow*, *The Matrix*, *Crimson Fire*, *Ocean Wave*, *Aurora*, and *Stealth (Off)*—switchable from hardware touch gestures or software UI.

---

## Quick Setup Order

> **IMPORTANT:** Always flash the firmware onto the Raspberry Pi Pico **before** assembling the 3D-printed enclosure.

### Step 1: Flash the Unified Firmware (Required Once)
1. Download **`NaviGo_V1.0_Firmware.uf2`** from the **[Latest Release](https://github.com/EslamEldeknawy/NaviGo-3D-Controller/releases/latest)**.
2. Hold the **BOOTSEL** button on your Raspberry Pi Pico while plugging it into your PC via USB, then release the button.
3. Drag and drop `NaviGo_V1.0_Firmware.uf2` into the `RPI-RP2` drive that appears. The board will reboot automatically.

### Step 2: Assemble the Hardware
Follow the illustrated **Assembly Guide** included with the 3D printing files on [Cults3D](https://cults3d.com/:5250150) to mount the electronics and assemble the enclosure.

### Step 3: Install the Companion Add-in for Your Software

#### 1. Autodesk Fusion 360
1. Close Autodesk Fusion 360.
2. Download and run **`Install_NaviGo.exe`** from the **[Latest Release](https://github.com/EslamEldeknawy/NaviGo-3D-Controller/releases/latest)**.
3. Click **Install NaviGo Add-in**, then launch Fusion 360.
4. Open **`Utilities` → `ADD-INS` → `NaviGo Settings`** to open the dockable control panel.

#### 2. Blender (Blender 3.0 – 4.x+)
1. Download the Blender package from the **[Latest Release](https://github.com/EslamEldeknawy/NaviGo-3D-Controller/releases/latest)**:
   - **Blender 4.2+:** Download **`navigo_6dof_controller-1.0.2.zip`** (drag and drop directly into Blender, or use `Edit → Preferences → Add-ons → Install from Disk`).
   - **Blender 3.0 – 4.1:** Download **`NaviGo_Blender_Legacy_v1.0.2.zip`** and install via `Edit → Preferences → Add-ons → Install`.
2. Enable **NaviGo - 6-DOF 3D Navigation Controller** in Preferences.
3. Press **`N`** in the 3D Viewport and open the **NaviGo** sidebar tab.

#### 3. FreeCAD (FreeCAD 0.21 – 1.x+)
1. Download **`NaviGo_FreeCAD_v1.0.0.zip`** from the **[Latest Release](https://github.com/EslamEldeknawy/NaviGo-3D-Controller/releases/latest)** and extract the `NaviGo` folder.
2. Copy the `NaviGo` folder into your FreeCAD user `Mod` directory (e.g., `%APPDATA%\FreeCAD\Mod\` or `%APPDATA%\FreeCAD\v1-1\Mod\`).
3. Restart FreeCAD and click **`NaviGo Settings`** in the top toolbar (or **`Tools` → `NaviGo Settings`**).

---

## Quick Gesture Reference

| Action | Knob Grip / Motion | Top Touch | Zoom Sensors (Far Right) |
| :--- | :--- | :---: | :---: |
| **Pan (All Directions)** | Hold sides & tilt | Off | Off |
| **Orbit (Rotate Model)** | Tilt knob | Touch Top | Off |
| **Zoom In** | Neutral (No tilt) | Off | Touch Front |
| **Zoom Out** | Neutral (No tilt) | Off | Touch Rear |
| **Roll (Tilt Horizon)** | Tilt knob (Orbit motion) | Touch Top | Touch Front **OR** Rear |
| **Cycle LED Theme** | Neutral | Off | Quick Tap **BOTH** |
| **Re-Zero Calibrate** | Neutral (Hands off knob) | Off | Hold **BOTH** (> 2 sec) |

For full details, download **`NaviGo_User_Manual.pdf`** and **`NaviGo_Hands_On_Guide.pdf`** from the Releases page.

---

## Important Compatibility Notice

- **Not a Standard Computer Mouse:** NaviGo does not move your Windows cursor or replace your regular desktop mouse.
- **Companion Add-in Required:** NaviGo operates through native camera API add-ins inside supported 3D applications (**Fusion 360**, **Blender**, and **FreeCAD**).

---

## License & Credits

- RP2040 firmware, Windows installer, Fusion 360 add-in, and FreeCAD add-on are released under the **MIT License**.
- The Blender add-on is released under **GPL-3.0-or-later** in compliance with Blender's Python API (`bpy`) licensing.
- 3D printable mechanical files (`STL` / `3MF`) are licensed separately on Cults3D.
- Created by **Eslam's Lab** (*Eslam Eldeknawy*).

---

## Development & AI Transparency

NaviGo's mechanical CAD design, custom PCB layout, electronics architecture, and physical prototyping were designed and built from the ground up by Eslam Eldeknawy. To accelerate software development, AI coding assistants were used as a pair-programming tool to help draft and iterate on the RP2040 firmware, the companion add-ins (Fusion 360, Blender, and FreeCAD), and the Windows installer—followed by extensive hands-on hardware testing, debugging, and real-world calibration.

---

## Support the Project

The NaviGo firmware, Windows installer, and all 3D software add-ins are 100% free and open-source. If NaviGo improved your CAD/3D workflow and you'd like to support future open-source hardware and software builds, you can buy me a coffee on Ko-fi!

[![Support me on Ko-fi](https://img.shields.io/badge/Support%20on-Ko--fi-FF5E5B?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/eslameldeknawy)
