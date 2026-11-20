# NaviGo V1.0 — 6-DOF 3D Navigation Controller for Autodesk Fusion 360

> **Print. Build. Navigate.**

**NaviGo V1.0** is a custom 6-DOF (Six Degrees of Freedom) 3D navigation controller engineered specifically for **Autodesk Fusion 360**, powered by a **Raspberry Pi Pico (RP2040)**, an **ADXL335** accelerometer, and capacitive touch sensors.

This repository hosts the **free software package**: RP2040 firmware (`.uf2`), the one-click Windows installer (`Install_NaviGo.exe`), the Fusion 360 Python add-in, and the user manuals.

---

## Get the 3D Printable Files (STL / 3MF)

- **Mechanical 3D Printing Files & Illustrated Assembly Guide:** Available on **[Cults3D — Download Here](https://cults3d.com/:5250150)**
* **Free Software, Firmware & Manuals:** Download directly from **[GitHub Releases (Latest)](https://github.com/EslamEldeknawy/NaviGo-3D-Controller/releases/latest)**



---

## Key Features

* **Full 6-DOF Camera Control:** Smooth Pan, Orbit, Zoom, and Roll inside Autodesk Fusion 360.
* **Plug & Play Auto-Connection:** Automatically detects NaviGo's USB port and reconnects seamlessly if unplugged—no manual COM port setup required.
* **One-Click Windows Installer:** `Install_NaviGo.exe` installs, updates (while preserving your settings), or cleanly uninstalls the Fusion 360 add-in in seconds.
* **Dark-Mode Control Panel:** Dockable Fusion 360 panel with live speed sliders (Master, Pan, Orbit, Zoom, Roll), axis toggles (`Invert X`, `Invert Y`, `Swap X ↔ Y`, `Invert Zoom`), and `Re-Zero` calibration.
* **6 Built-in LED Lighting Themes:** *Rainbow*, *The Matrix*, *Crimson Fire*, *Ocean Wave*, *Aurora*, and *Stealth (Off)*—switchable from hardware or software.

---

## Quick Setup Order

> **IMPORTANT:** Always flash the firmware onto the Raspberry Pi Pico **before** assembling the 3D-printed enclosure.

### Step 1: Flash the Firmware (Do This First)
1. Download **`NaviGo_V1.0_Firmware.uf2`** from the **[Latest Release](https://github.com/EslamEldeknawy/NaviGo-3D-Controller/releases/latest)**.
2. Hold the **BOOTSEL** button on your Raspberry Pi Pico while plugging it into your PC via USB, then release the button.
3. Drag and drop `NaviGo_V1.0_Firmware.uf2` into the `RPI-RP2` drive that appears. The board will reboot automatically.

### Step 2: Assemble the Hardware
Follow the illustrated **Assembly Guide** included with the 3D printing files on Cults3D to mount the electronics and assemble the enclosure.

### Step 3: Install the Fusion 360 Add-in
1. Close Autodesk Fusion 360.
2. Download and run **`Install_NaviGo.exe`** from the **[Latest Release](https://github.com/EslamEldeknawy/NaviGo-3D-Controller/releases/latest)**.
3. Click **Install NaviGo Add-in**, then launch Fusion 360.
4. Plug in NaviGo and open **`Utilities` → `ADD-INS` → `NaviGo Settings`** to customize your controller.

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
## Get the Hardware & Software

* **3D Printable Files (STL / 3MF) & Illustrated Assembly Guide:** [Download on Cults3D]([https://cults3d.com/en/3d-model/gadget/navigo-the-ultimate-diy-6-dof-cad-navigation-mouse-fusion-360-212c68502da05017087e](https://cults3d.com/en/creations/navigo-v1-0-diy-6-dof-3d-navigation-controller-for-autodesk-fusion-360))
* **Custom 4-LED RGB PCB (Order Ready-Made):** [Order on PCBWay](https://www.pcbway.com/project/shareproject/NaviGo_V1_0_DIY_6_DOF_3D_Navigation_Controller_for_Autodesk_Fusion_360_4f7429b3.html)
* **Free Firmware, One-Click Windows Installer & Manuals:** [Download Latest Release on GitHub](https://github.com/EslamEldeknawy/NaviGo-3D-Controller/releases/latest)

## Important Compatibility Notice

* **Not a Standard Computer Mouse:** NaviGo does not move your Windows cursor or replace your regular desktop mouse.
* **Fusion 360 Exclusive:** Designed specifically as a companion tool for **Autodesk Fusion 360**; it will not operate outside of Fusion 360.
* **Add-in Required:** The NaviGo Fusion 360 Add-in must be installed and running for the controller to work.

---

## License & Credits

* Software & firmware are released under the **MIT License**.
* 3D printable mechanical files (`STL` / `3MF`) are licensed separately on Cults3D.
* Created by **Eslam's Lab** (*Eslam Eldeknawy*).
  
## Development & AI Transparency
NaviGo's mechanical CAD design, custom PCB layout, electronics architecture, and physical prototyping were designed and built from the ground up by Eslam Eldeknawy. To accelerate software development, AI coding assistants were used as a pair-programming tool to help draft and iterate on the RP2040 firmware, the Fusion 360 Python add-in, and the Windows installer—followed by extensive hands-on hardware testing, debugging, and real-world calibration.

## Support the Project

The NaviGo firmware, one-click Windows installer, and Fusion 360 add-in are 100% free and open-source. If NaviGo improved your CAD workflow and you'd like to support future open-source hardware and software builds, you can buy me a coffee on Ko-fi!



[![Support me on Ko-fi](https://img.shields.io/badge/Support%20on-Ko--fi-FF5E5B?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/eslameldeknawy)

