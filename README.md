<div align="center">

#  NaviGo — 6-DOF 3D CAD & Engine Controller
### **Unified Auto-Flasher, Sensor Configurator & Native 8-Suite Add-in Manager**

[![Release](https://img.shields.io/badge/Release-v1.1.0-0284c7?style=for-the-badge)](../../releases/latest)
[![OS](https://img.shields.io/badge/OS-Windows_10_%26_11-0f172a?style=for-the-badge)](#)
[![MCU](https://img.shields.io/badge/MCU-Waveshare_RP2040--Zero-38bdf8?style=for-the-badge)](#)
[![Suites](https://img.shields.io/badge/Native_Suites-8_Platforms-10b981?style=for-the-badge)](#)

**True native 6-DOF viewport navigation across 8 industry-standard CAD, 3D modeling, and game-engine suites—powered by a 1-click Windows configurator and automatic 8-sensor firmware.**

[⬇️ Download Install_NaviGo.exe (v1.1.0)](../../releases/latest) &bull; [📺 Eslam's Lab on YouTube](https://www.youtube.com/c/EslamsLab)

<br>

### Supported Platforms

![Fusion 360](https://img.shields.io/badge/Fusion_360-FF6B00?style=for-the-badge&logo=autodesk&logoColor=white)
![Inventor](https://img.shields.io/badge/Inventor-D97706?style=for-the-badge&logo=autodesk&logoColor=white)
![3ds Max](https://img.shields.io/badge/3ds_Max-0D9488?style=for-the-badge&logo=autodesk&logoColor=white)
![AutoCAD](https://img.shields.io/badge/AutoCAD-E11D48?style=for-the-badge&logo=autodesk&logoColor=white)
![Maya](https://img.shields.io/badge/Maya-0284C7?style=for-the-badge&logo=autodesk&logoColor=white)
![Blender](https://img.shields.io/badge/Blender-F5792A?style=for-the-badge&logo=blender&logoColor=white)
![FreeCAD](https://img.shields.io/badge/FreeCAD-CB333B?style=for-the-badge&logo=freecad&logoColor=white)
![Unity](https://img.shields.io/badge/Unity-111827?style=for-the-badge&logo=unity&logoColor=white)

<br>

<img src="installer_ui.png" alt="NaviGo V1.1 Universal Installer & Hardware Setup" width="460" />

</div>

---

##  Software Highlights (`Install_NaviGo.exe` v1.1)

Most DIY 6-DOF controllers rely on choppy keyboard/mouse shortcuts, require manual Python library setups, or lock you into a single accelerometer chip. **NaviGo v1.1** puts the entire hardware and software stack into a single standalone Windows executable:

- **🖱️  1-Click Firmware Flashing (`Auto-Boot + .uf2`):** Flashes Firmware v1.1 directly onto the **Waveshare RP2040-Zero** (or standard Raspberry Pi Pico) with zero external tools.
- **🪄  Automatic 8-Sensor Detection:** Automatically detects whether you connected an analog `ADXL335` or any of 7 I2C accelerometers (`ADXL345`, `MPU6050`, `MPU6500`, `MPU9250`, `LIS3DH`, `MMA8452Q`, `BMI160`). Includes a live **`Detect Sensor`** test button and EEPROM mode persistence.
- **💡 Custom WS2812B LED Ring Count (`1–64 LEDs`):** Set your exact LED count (`4, 8, 12, 16, 24`, or any value `1–64`) and save directly to EEPROM via **`Apply HW Config`**. The ring provides real-time reactive color feedback for **Orbit**, **Pan**, and **Zoom** modes.
- **➕  8-Platform Native Add-in Manager:** Automatically detects installed versions on your PC and lets you **Install**, **Repair**, or **Uninstall** native camera plugins individually or in batch.
- **🎯 Zero-Latency Native Viewport APIs:** Communicates directly with each application's native camera API for smooth, proportional 6-DOF control without overriding your custom hotkeys.
- **🚫 Zero Custom PCB Architecture:** Engineered for direct point-to-point wiring between standard off-the-shelf modules.

---

## 🧩 Supported Software Suites (Native Integrations)

| Suite | Supported Versions | Integration Architecture |
| :--- | :--- | :--- |
| **Autodesk Fusion 360** | Latest | Native Viewport Add-in |
| **Autodesk Inventor** | 2025 – 2026+ | Native Viewport Add-in |
| **Autodesk 3ds Max** | 2022 – 2027+ | Native Viewport Plugin |
| **Autodesk AutoCAD** | 2025 – 2027+ | Native Viewport API |
| **Autodesk Maya** | 2022 – 2027+ | Native Viewport Plugin |
| **Blender** | 3.x / 4.x+ | Native Add-on |
| **FreeCAD** | 0.21 / 1.0+ | Native Workbench Module |
| **Unity Editor** | Unity 2022 / Unity 6+ | Native Scene View Integration |

---

## 🔌 Supported Hardware Modules

| Component | Supported Hardware | Configuration in `Install_NaviGo.exe` |
| :--- | :--- | :--- |
| **Microcontroller** | **Waveshare RP2040-Zero** (USB-C) or standard RP2040 Pico | 1-click `.uf2` flash via **Flash Firmware v1.1** |
| **Accelerometer** *(Any 1)* | **Analog:** `ADXL335`<br>**I2C:** `ADXL345`, `MPU6050`, `MPU6500`, `MPU9250`, `LIS3DH`, `MMA8452Q`, `BMI160` | Set **Sensor Mode (EEPROM)** to `Auto` or lock a specific sensor |
| **Touch Inputs** | **3&times; TTP233** Capacitive Touch Sensors | 1&times; Mode Toggle (Orbit / Pan) + 2&times; Zoom In / Out |
| **Reactive LEDs** | **Any WS2812B Addressable Ring (< 55 mm OD)** | Set **LED Ring Count (`1–64`)** &rarr; **Apply HW Config** |

---

## 🚀 Quick Usage

1. Download **`Install_NaviGo.exe`** from the [Latest Release](../../releases/latest) and run it on Windows 10/11.
2. Close open CAD/3D applications so the serial port is free.
3. Click **`Flash Firmware v1.1 to RP2040 (Auto-Boot + .uf2)`** *(if flashing a new Waveshare RP2040-Zero for the first time, hold **BOOT** and tap **RESET** while connected via USB-C)*.
4. Choose your **LED Ring Count (1–64)**, keep **Sensor Mode** on `Auto`, and click **`Apply HW Config`** followed by **`Detect Sensor`**.
5. Select your installed design suites in Section 2 and click **`Install / Repair Selected`**.

---

## 📜 Copyright & License

Copyright &copy; 2026 **Eslam Eldeknawy ([Eslam's Lab](https://eslamslab.blogspot.com))**. All rights reserved.  
`Install_NaviGo.exe` and its bundled firmware/add-ins are provided free for personal use with NaviGo hardware. Unauthorized commercial redistribution or re-hosting is prohibited.
