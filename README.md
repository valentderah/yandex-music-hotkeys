English | [Русский](README.ru.md)

# Yandex Music Hotkeys

Global hotkeys for controlling the Yandex Music desktop application on Windows.

The application runs in the background and allows you to control playback even if the Yandex Music window is minimized
or not in focus.

## Features

- ⏯ **Play/Pause**
- ⏭ **Next Track**
- ⏮ **Previous Track**

[//]: # (- ⚙️ **Customizable Hotkeys** &#40;JSON configuration&#41;)
[//]: # (- 🚫 **Input Suppression** &#40;Hotkeys are not passed to other applications&#41;)

## Installation & Usage

### Option 1: Use EXE file

Download `YandexMusicHotkeys.exe` from the releases section or build it yourself.

### Option 2: Run from Source

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Default Hotkeys

| Action         | Combination          |
|----------------|----------------------|
| Next Track     | `Ctrl` + `Right` (→) |
| Previous Track | `Ctrl` + `Left` (←)  |
| Play/Pause     | `Ctrl` + `Space`     |

[//]: # (| Volume Up      | `Ctrl` + `Up` &#40;↑&#41;    |)
[//]: # (| Volume Down    | `Ctrl` + `Down` &#40;↓&#41;  |)
