import subprocess
import textwrap
import os
import sys

from core.constants import APP_NAME, APP_VERSION


def generate_version_file():
    parts = [int(x) for x in APP_VERSION.split(".")]
    while len(parts) < 4:
        parts.append(0)
    version_tuple = tuple(parts)

    content = textwrap.dedent(
        f"""
            # UTF-8
            VSVersionInfo(
              ffi=FixedFileInfo(
                filevers={version_tuple},
                prodvers={version_tuple},
                mask=0x3f,
                flags=0x0,
                OS=0x40004,
                fileType=0x1,
                subtype=0x0,
                date=(0, 0)
              ),
              kids=[
                StringFileInfo(
                  [
                  StringTable(
                    u'040904B0',
                    [StringStruct(u'CompanyName', u'Valiantsin Dzerakh (valentderah)'),
                    StringStruct(u'FileDescription', u'Yandex Music Global Hotkeys'),
                    StringStruct(u'FileVersion', u'{APP_VERSION}'),
                    StringStruct(u'InternalName', u'YandexMusicHotkeys'),
                    StringStruct(u'LegalCopyright', u'Copyright (c) 2026 Valiantsin Dzerakh'),
                    StringStruct(u'OriginalFilename', u'YandexMusicHotkeys.exe'),
                    StringStruct(u'ProductName', u'{APP_NAME}'),
                    StringStruct(u'ProductVersion', u'{APP_VERSION}')])
                  ]), 
                VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
              ]
            )
        """
    ).strip()

    if not os.path.exists("dist"):
        os.makedirs("dist")
    
    file_path = os.path.join("dist", "version_info.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {file_path} with version {APP_VERSION}")
    return file_path


def main():
    version_file = generate_version_file()

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        "--name", APP_NAME,
        "--add-data", "assets;assets",
        "--icon", "assets/icon.ico",
        "--version-file", version_file,

        # Exclude heavy unnecessary modules
        "--exclude-module", "numpy",
        "--exclude-module", "matplotlib",
        "--exclude-module", "tkinter",
        "--exclude-module", "scipy",
        "--exclude-module", "pandas",
        "--exclude-module", "IPython",

        "main.py"
    ]

    print(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd)

    print("\nBuild complete. Check the 'dist' folder.")


if __name__ == "__main__":
    main()
