# NaviGo V2.0 — DIY 6-DOF 3D Navigation Controller

**Print. Build. Navigate.**  
A completely redesigned, **100% PCB-free** DIY 6-DOF 3D navigation controller powered by the **Waveshare RP2040-Zero**, delivering smooth native viewport control across **8 major CAD, 3D, and game-engine platforms** on **Windows & Linux**.

![Platform](https://img.shields.io/badge/OS-Windows%20%7C%20Linux-0284C7?style=for-the-badge)
![Microcontroller](https://img.shields.io/badge/MCU-RP2040--Zero-141820?style=for-the-badge)
![Apps](https://img.shields.io/badge/Native%20Plugins-8%20Platforms-16A34A?style=for-the-badge)
![Architecture](https://img.shields.io/badge/Hardware-PCB--Free-D97706?style=for-the-badge)

---

## 🎥 Watch NaviGo V2.0 in Action (All 8 Platforms)

[![NaviGo V2.0 Demo Across 8 CAD, 3D & Engine Apps](https://img.youtube.com/vi/HrUuJDkjKqE/maxresdefault.jpg)](https://youtu.be/HrUuJDkjKqE)

▶️ **[Watch Full 2:46 Demo on YouTube](https://youtu.be/HrUuJDkjKqE)** — Native viewport navigation across 3ds Max, Blender, FreeCAD, Inventor, Maya, Unity, Fusion 360, and AutoCAD, plus a top-down view of the reactive WS2812B LED force arc.

---

## 🚀 Get the Complete DIY Build Package

This repository hosts the **Universal Software Installer & Firmware updates** only.  
The complete DIY package — including all **3D-printable STL/3MF files (Parts 0–8)** and **2 full illustrated PDF guides** (Mechanical Assembly + Electronics & Wiring) — is available on Gumroad:

👉 **[Download NaviGo V2.0 Complete DIY Package on Gumroad](https://eslamslab.gumroad.com/l/navigo-v2/FIRST50)**  
🔥 **Launch Offer:** Use code **`FIRST50`** at checkout for an exclusive early-bird discount *(limited to the first 50 makers!)*

> **Don't have a 3D printer or don't want to solder?**  
> We are preparing **Hardware DIY Kits** and **Pre-Assembled Plug & Play** units.  
> ⏳ **[Join the Official Hardware Waitlist Here](https://tally.so/r/Yj48Ev)**

---

## ✨ What’s New in V2.0

- **100% PCB-Free Architecture:** Eliminates custom PCB fabrication. Uses a generic off-the-shelf WS2812B LED ring and a simple 2×6 stripboard power rail.
- **Auto-Detect 8+ Accelerometers:** Firmware v2.0 automatically detects your sensor on boot:
  - **Analog:** `ADXL335` / `GY-61` (or any 3.3V analog accelerometer such as `MMA7361`).
  - **I2C Digital (7 models):** `ADXL345`, `MPU6050`, `MPU6500`, `MPU9250`, `LIS3DH`, `MMA8452Q`, `BMI160`.
- **Integrated-Spacer Spring:** The standalone spacer from V1.0 is merged directly into the high-tension spring (`Part 2`) for cleaner assembly.
- **Onboard EEPROM Hardware Tuning:** Configure LED count (`4–64 LEDs`), ring rotation, `Invert X/Y`, `Swap X/Y`, and `Swap Zoom` directly from the installer — no code editing or resoldering required.
- **One-Click Universal Installer (Windows & Linux):** Flash firmware (`NaviGo.uf2`), detect sensors, tune EEPROM settings, and install/repair native plugins from one interface.

---

## 🖥️ Supported Software (8 Native Platforms)

| Platform | Supported Versions | OS Support |
| :--- | :--- | :--- |
| **Autodesk Fusion 360** | Current / Latest | Windows |
| **Blender** | 3.x / 4.x+ | Windows & Linux |
| **FreeCAD** | 0.21 / 1.0+ (incl. AppImage) | Windows & Linux |
| **Autodesk Inventor** | 2025–2026+ | Windows |
| **Autodesk 3ds Max** | 2022–2027+ | Windows |
| **Autodesk AutoCAD** | 2025–2027+ | Windows |
| **Autodesk Maya** | 2022–2027+ | Windows & Linux |
| **Unity Editor** | 2022 / Unity 6+ | Windows & Linux |

---
## 🛠️ Bill of Materials (BOM)

All electronic parts are inexpensive, off-the-shelf modules (~$10–$15 total) with **zero custom PCBs** required:

| Component | Qty | Specification & Notes |
| :--- | :---: | :--- |
| **Waveshare RP2040-Zero** | 1× | USB-C microcontroller (flashed with `NaviGo.uf2` v2.0) |
| **Accelerometer Module** | 1× | **Analog:** `ADXL335` (`GY-61`) **OR I2C (any 1):** `ADXL345`, `MPU6050`, `MPU6500`, `MPU9250`, `LIS3DH`, `MMA8452Q`, `BMI160` |
| **Capacitive Touch Modules** | 3× | Compact `TTP223` / `TTP233` red modules (1× Top Mode Toggle + 2× Side Zoom In/Out) |
| **WS2812B LED Ring** | 1× | `4–64 LEDs` (`16-LED` ring standard); `ID ≥ 42 mm`, `OD ≤ 70 mm` — runs directly on `3.3V` |
| **Prototype Stripboard** | 1× | Small `2 × 6` hole piece (veroboard) for the `3.3V` and `GND` power distribution rails |
| **M3 × 16 mm Screws** | 8× | `4×` for Middle Stack (`Part 7 → 3`) + `4×` for Bottom Base Closure (`Part 8 → 6`) |
| **M3 × 8 mm Screws** | 8× | Fastens accelerometer holder upward through the spring (`Part 2`) into the knob |
| **Thin Flexible Wire** | ~1 m | `28–30 AWG` silicone wire or peeled `4-wire` RGB ribbon (`15 cm` leads inside moving knob) |
| **Thin Double-Sided Tape** | — | Non-foam thin tape for mounting touch sensors, accelerometer, and LED ring (hot glue optional) |


## ⚡ Quick Hardware & Pinout Overview (RP2040-Zero)

> **⚠️ 3.3V POWER ONLY:** Every module (Accelerometer, 3× Touch Sensors, and the WS2812B LED Ring) MUST be powered from the **3.3V (`3V3`)** pin. Do **NOT** connect anything to the `5V` pin.

| Component / Signal | RP2040-Zero Pin | Notes |
| :--- | :--- | :--- |
| **WS2812B LED Ring (`DI`)** | `GPIO 0` | Connect to **Data IN (`DI`)** only; ignore `DO` (`4–64 LEDs`, 16-LED standard) |
| **Zoom OUT Touch (`TTP223`)** | `GPIO 2` | Swappable with Zoom IN via Installer |
| **Zoom IN Touch (`TTP223`)** | `GPIO 3` | Swappable with Zoom OUT via Installer |
| **Main Top Touch (`TTP223`)** | `GPIO 4` | Mounted inside knob (`15 cm` flexible leads) |
| **Analog Accel (`XOUT / YOUT`)** | `GPIO 26 / GPIO 27` | Axis order swappable in EEPROM / CAD panel |
| **I2C Accel (`SDA / SCL`)** | `GPIO 26 / GPIO 27` | `SDA → GPIO 26`, `SCL → GPIO 27` (**Do NOT swap!**) |
| **Power Rail (All 5 Modules)** | `3.3V & GND` | Distribute via a `2×6` stripboard rail — **never use 5V** |

*(Full step-by-step wiring diagrams and exploded 3D assembly views are included in the 2 PDF guides on Gumroad.)*

---

## 📦 Software & Firmware Updates

Already built your NaviGo? Grab the latest Universal Installer and Firmware from the **[Releases](../../releases)** page:

- **Windows:** Run `Install_NaviGo.exe` → click **Flash Firmware v2.0** → click **Detect Sensor** → install your native plugins in one click.
- **Linux (Ubuntu / Arch / Fedora):** Extract `NaviGo_Linux_V2.0.tar.gz` and run the included installer script to flash firmware and deploy plugins for Blender, FreeCAD, Maya, and Unity.

---

## 📜 License

All software binaries, firmware, 3D models, and documentation for **NaviGo V2.0** are copyright © 2026 **Eslam Eldeknawy (Eslam's Lab)** and licensed for **strictly personal, non-commercial use only**. Redistribution, reselling, or commercial manufacturing without written permission is prohibited.
