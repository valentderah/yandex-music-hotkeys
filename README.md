English | [Русский](README.ru.md)

## Yandex Music Hotkeys <img src="./assets/icon.png" width="20px">

Global hotkeys for controlling the Yandex Music desktop application on Windows.<br>
The application runs in the background and allows you to control playback even if the Yandex Music window is minimized
or not in focus.

<img src="assets/banner-en.png">

## Default Hotkeys

| Action         | Combination          |
|----------------|----------------------|
| Next Track     | `Ctrl` + `Right` (→) |
| Previous Track | `Ctrl` + `Left` (←)  |
| Play/Pause     | `Ctrl` + `Space`     |

## Installation & Run

### Option 1: Use EXE file

Download [YMHotkeys.exe](https://github.com/valentderah/yandex-music-hotkeys/releases/download/v1.0.0/YMHotkeys.exe) from
the [releases](https://github.com/valentderah/yandex-music-hotkeys/releases) section.

### Option 2: Run from source or build

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

OR

3. Build your own .exe:
   ```bash
   python build.py
   ```
