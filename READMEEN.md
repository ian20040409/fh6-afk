# Forza Horizon AFK Script

This Python AFK helper is built for the Forza Horizon series. It simulates a virtual Xbox controller to provide stable automatic throttle control, with soft-start traction protection and anti-AFK throttle releases for long-running sessions.<br>
https://youtube.com/live/bFRetrKjcRw
<br><br>
![In-game assist settings](blog-imgs/img1.png)
<br><br>

## Features

* **Automatic throttle control**: Simulates the Xbox controller right trigger (RT) with steady output.
* **Soft Start**: Limits throttle during the first part of a run, such as 50% throttle for the first 60 seconds, to reduce wheelspin on high-power RWD or AWD cars.
* **Anti-AFK**: Briefly releases the throttle at lightly randomized intervals to mimic real player input.
* **Safe stop flow**: Uses a startup countdown and lets you stop by closing the console window, avoiding issues with games blocking global hotkeys.

## Requirements

* Operating system: Windows 10 or later
* Runtime: Python 3.x. During installation, enable **Add Python to PATH**.

## Environment Setup (Manual)

This script depends on external Python packages:

* **vgamepad**: Creates a virtual Xbox 360 controller on Windows and sends controller input. ViGEmBus may be installed automatically on first setup or first run.
* **keyboard**: Used by older hotkey-based variants. The EN countdown version only requires `vgamepad`.

Run this command in Terminal or Command Prompt:

```bash
pip install vgamepad keyboard
```

## Installation and Usage

### Method 1: Automatic Runner (Recommended)

1. Download `AFKgameEN.py` and `RunAFKEN.ps1`, then place both files in the same folder.
2. Right-click `RunAFKEN.ps1` and choose **Run with PowerShell**.
3. If Windows shows a User Account Control (UAC) prompt, choose **Yes**. The runner installs required packages and starts the script.

```bash
powershell -ExecutionPolicy Bypass -File .\RunAFKEN.ps1
```

```bash
Set-ExecutionPolicy Bypass -Scope Process
```

### Method 2: Manual Run

1. Install the packages listed in the environment setup section.
2. Open Command Prompt as Administrator.
3. Run `python your\file\path\AFKgameEN.py`.

### After Starting

1. **Configure parameters**: Follow the console prompts. Press Enter to use each default value.
2. **Switch back to the game**: After setup, the script starts a 10-second countdown. Click back into the Forza Horizon game window during this time.
3. **Stop AFK mode**: Press `Alt + Tab` to leave the game, then close the black console window. The script releases virtual controller inputs safely.

## Parameter Guide

You can tune these values when the script starts:

* **Normal driving throttle**: Throttle depth during normal straight-line driving. Default: 100%.
* **Soft-start duration**: Time to limit throttle at startup. Default: 60 seconds.
* **Soft-start throttle**: Maximum throttle during the soft-start phase. Default: 50%.
* **Throttle acceleration**: Linear throttle ramp speed in percent per second. Default: 50.
* **Throttle release interval**: Anti-AFK trigger interval. Default: 15 seconds.
* **Start delay**: Time to switch back to the game after setup. Default: 10 seconds.

## Notes

* Make sure your real keyboard and mouse are connected or paired correctly to avoid virtual controller driver conflicts.
* The game must be the active foreground window for the script to affect gameplay.
* Some antivirus tools may flag virtual controller drivers. Allowlist the driver if needed.

## Recommended In-Game Difficulty and Assist Settings

For best results, set the in-game driving assist preset to **All Assists**. This lets the game handle steering and braking while the script controls throttle.

Recommended difficulty settings:

| Setting | Recommended Option | Notes |
| :--- | :--- | :--- |
| **Braking** | Assisted | Lets the game slow down near corners to avoid leaving the track. |
| **Steering** | Auto-Steering | Critical for keeping the car on the racing line. |
| **Traction Control** | On | Reduces wheelspin and improves stability. Keep it on for AFK reliability, even if turning it off gives a CR bonus. |
| **Stability Control** | On | Prevents spinouts at high speed or in corners. Keep it on for AFK reliability. |
| **Shifting** | Automatic | Lets the game handle gear changes. |
| **Driving Line** | Full | Helps auto-steering and assisted braking detect the racing line and braking points. |
| **Damage and Tire Wear** | Cosmetic | Prevents long races from reducing vehicle performance. |
| **Rewind** | Off | Not needed for AFK runs, and changing this option does not affect CR bonus rewards. |
| **Launch Control** | On | Adds extra stability during launch. |
