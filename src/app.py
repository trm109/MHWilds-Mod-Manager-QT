from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMainWindow

# import MainWindow from src/main_window.py
from main_window import MainWindow
import sys
import os
import platform
from mod_manager import ModManager

app = QApplication(sys.argv)

### Generating required files and folders
# Primary folder
print("Checking for required files")
if not os.path.exists(os.path.expanduser("~/Documents/MHWildsMods")):
    os.makedirs(os.path.expanduser("~/Documents/MHWildsMods"))
    print("MHWildsMods Directory created")
else:
    print("MHWildsMods Directory already exists")

# Folder that stores the extracted mods
if not os.path.exists(os.path.expanduser("~/Documents/MHWildsMods/imported")):
    os.makedirs(os.path.expanduser("~/Documents/MHWildsMods/imported"))
    print("MHWildsMods/imported Directory created")
else:
    print("MHWildsMods/imported Directory already exists")

# Config file
if not os.path.exists(os.path.expanduser("~/Documents/MHWildsMods/config.json")):
    with open(os.path.expanduser("~/Documents/MHWildsMods/config.json"), "w") as f:
        f.write(
            '{"gamedirectory": "", "modsdirectory": "", "mods": [], "os": "'
            + platform.system()
            + '"}'
        )
    print("Config file created")
else:
    print("Config file already exists")


### Determine default game directory and mod directory
# Default game directory, changes based on OS
gameDir = (
    os.path.expanduser("~/.steam/steam/steamapps/common/MonsterHunterWilds")
    if platform.system() == "Linux"
    else "C:\\Program Files\\Steam\\steamapps\\common\\MonsterHunterWilds"
)
# Default mod directory
modDir = os.path.expanduser("~/Documents/MHWildsMods")

## Initialize ModManager
modManager = ModManager(gameDir, modDir)
# pass modManager to MainWindow
window = MainWindow(modManager)

window.show()

app.exec()
