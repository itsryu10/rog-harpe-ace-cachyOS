# rog-harpe-ace-cachyOS
A lightweight Python GUI for ASUS ROG Harpe Ace on CachyOS (Battery status &amp; controls)
# ROG Harpe Ace - Linux Control Center 🐭🐧

A lightweight Python/CustomTkinter GUI application to check battery status and control settings for the **ASUS ROG Harpe Ace Aim Lab Edition** on Linux systems.

Since ASUS Armoury Crate is not available natively on Linux, this tool provides a clean and native interface using direct HID raw communication.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## ⚡ Features
- 🔋 **Real-time Battery Level:** Read exact battery percentage and charging state (Wireless / Wired).
- 🎛️ **Modern GUI:** Built with CustomTkinter dark theme.
- ⚡ **Lightweight:** No heavy background services or bloatware.

---

## 🛠️ Requirements & Installation

### 1. Mandatory udev Rules (Important)
Linux restricts raw USB/HID access for non-root users. To run the app without `sudo`, you must apply the following udev rule once:

```bash
echo 'SUBSYSTEM=="hidraw", ATTRS{idVendor}=="0b05", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0b05", MODE="0666"' | sudo tee /etc/udev/rules.d/99-rog-harpe.rules

sudo udevadm control --reload-rules && sudo udevadm trigger

git clone https://github.com/itsryu10/rog-harpe-ace-linux.git
cd rog-harpe-ace-linux
pip install customtkinter hid
python gui_harpe.py

📦 Standalone Executable

You can also download the pre-compiled binary executable directly from the Releases section without needing Python installed.
🤝 Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to open an Issue or Pull Request.
📜 License

Distributed under the MIT License.
