# NaviGo V1.0 — 6-DOF 3D Navigation Controller for Fusion 360 & Blender

> **Print. Build. Navigate.**

**NaviGo V1.0** is an open-source, proportional 6-DOF (Six Degrees of Freedom) 3D navigation controller engineered for **Autodesk Fusion 360** and **Blender**. Powered by a **Raspberry Pi Pico (RP2040)**, an **ADXL335** analog accelerometer, and zero-force capacitive touch sensors, it communicates natively with each program's camera API—keeping your regular mouse cursor 100% free while you pan, orbit, zoom, and roll simultaneously.

Both programs run on the **exact same RP2040 firmware**—no reflashing or hardware changes required when switching between Fusion 360 and Blender.

---

## Get the Hardware & Software

- **3D Printable Files (STL / 3MF) & Illustrated Assembly Guide:** [Download on Cults3D](https://cults3d.com/:5250150)
- **Custom 4-LED RGB PCB (Order Ready-Made):** [Order on PCBWay](https://www.pcbway.com/project/shareproject/NaviGo_V1_0_DIY_6_DOF_3D_Navigation_Controller_for_Autodesk_Fusion_360_4f7429b3.html)
- **Full Illustrated Build Guide & Schematics:** [View on Hackster.io](https://www.hackster.io/eslam-eldeknawy/navigo-v1-0-diy-6-dof-cad-navigation-mouse-for-fusion-360-744629)
- **Free Firmware, Add-ins & User Manuals:** [Download Latest Release on GitHub](https://github.com/EslamEldeknawy/NaviGo-3D-Controller/releases/latest)

---

## Key Features

- **Dual-Software Support (Fusion 360 & Blender):** Native camera API integration for both Autodesk Fusion 360 and Blender using a single unified RP2040 firmware.
- **Full 6-DOF Camera Control:** Smooth simultaneous Pan, Orbit, Proportional Zoom, and Horizon Roll while keeping your standard mouse cursor completely free.
- **Plug & Play Auto-Connection:** Automatically detects NaviGo's USB serial port, reconnects seamlessly if unplugged, and auto-recovers after Windows Sleep/Wake—no manual COM port setup required.
- **Smart Focus Protection:** Automatically pauses viewport camera movement when Fusion 360 or Blender is minimized or unfocused.
- **Dedicated Control Panels:**
  - **Fusion 360:** Dockable dark-mode HTML panel (`Utilities → ADD-INS → NaviGo Settings`) + one-click Windows installer (`Install_NaviGo.exe`).
  - **Blender:** Integrated sidebar panel (`View3D → Sidebar (N) → NaviGo`) with live speed sliders, axis toggles (`Invert X`, `Invert Y`, `Swap X ↔ Y`, `Invert Zoom`), and `Re-Zero` calibration.
- **6 Built-in LED Lighting Themes:** *Rainbow*, *The Matrix*, *Crimson Fire*, *Ocean Wave*, *Aurora*, and *Stealth (Off)*—switchable from hardware or software.

---

## Quick Setup Order

> **IMPORTANT:** Always flash the firmware onto the Raspberry Pi Pico **before** assembling the 3D-printed enclosure.

### Step 1: Flash the Firmware (Do This First)
1. Download **`NaviGo_V1.0_Firmware.uf2`** from the **[Latest Release](https://github.com/EslamEldeknawy/NaviGo-3D-Controller/releases/latest)**.
2. Hold the **BOOTSEL** button on your Raspberry Pi Pico while plugging it into your PC via USB, then release the button.
3. Drag and drop `NaviGo_V1.0_Firmware.uf2` into the `RPI-RP2` drive that appears. The board will reboot automatically.

### Step 2: Assemble the Hardware
Follow the illustrated **Assembly Guide** included with the 3D printing files on [Cults3D](https://cults3d.com/:5250150) to mount the electronics and assemble the enclosure.

### Step 3: Install the Companion Add-in (Choose Your Software)

#### Option A: Autodesk Fusion 360
1. Close Autodesk Fusion 360.
2. Download and run **`Install_NaviGo.exe`** from the **[Latest Release](https://github.com/EslamEldeknawy/NaviGo-3D-Controller/releases/latest)**.
3. Click **Install NaviGo Add-in**, then launch Fusion 360.
4. Plug in NaviGo and open **`Utilities` → `ADD-INS` → `NaviGo Settings`** to customize your controller.

#### Option B: Blender (Blender 3.0 – 4.x+)
1. Download the Blender add-on package from the **[Latest Release](https://github.com/EslamEldeknawy/NaviGo-3D-Controller/releases/latest)**:
   - **Blender 4.2+:** Download **`navigo_6dof_controller-1.0.2.zip`** (drag and drop directly into Blender, or use `Edit → Preferences → Add-ons → Install from Disk`).
   - **Blender 3.0 – 4.1:** Download **`NaviGo_Blender_Legacy_v1.0.2.zip`** and install via `Edit → Preferences → Add-ons → Install`.
2. Enable **NaviGo - 6-DOF 3D Navigation Controller** in Preferences.
3. In the 3D Viewport, press **`N`** to open the sidebar and select the **NaviGo** tab.

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
- **Supported Software:** Designed specifically as a native companion controller for **Autodesk Fusion 360** and **Blender**; it will not operate outside of these applications.
- **Add-in Required:** The respective NaviGo companion add-in must be installed and enabled for the controller to work.

---

## License & Credits

- RP2040 firmware, Windows installer, and Fusion 360 add-in are released under the **MIT License**.
- The Blender add-on is released under **GPL-3.0-or-later** in compliance with Blender's Python API (`bpy`) licensing.
- 3D printable mechanical files (`STL` / `3MF`) are licensed separately on Cults3D.
- Created by **Eslam's Lab** (*Eslam Eldeknawy*).

---

## Development & AI Transparency

NaviGo's mechanical CAD design, custom PCB layout, electronics architecture, and physical prototyping were designed and built from the ground up by Eslam Eldeknawy. To accelerate software development, AI coding assistants were used as a pair-programming tool to help draft and iterate on the RP2040 firmware, the Autodesk Fusion 360 add-in, the Blender add-on, and the Windows installer—followed by extensive hands-on hardware testing, debugging, and real-world calibration.

---

## Support the Project

The NaviGo firmware, Windows installer, Fusion 360 add-in, and Blender add-on are 100% free and open-source. If NaviGo improved your 3D workflow and you'd like to support future open-source hardware and software builds, you can buy me a coffee on Ko-fi!

[![Support me on Ko-fi](https://img.shields.io/badge/Support%20on-Ko--fi-FF5E5B?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/eslameldeknawy)
