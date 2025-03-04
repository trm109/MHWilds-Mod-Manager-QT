from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMainWindow

# import MainWindow from src/main_window.py
from main_window import MainWindow
import sys
import os
import platform
from mod_manager import ModManager

app = QApplication(sys.argv)

print("Checking for required files")
if not os.path.exists(os.path.expanduser("~/Documents/MHWildsMods")):
    os.makedirs(os.path.expanduser("~/Documents/MHWildsMods"))
    print("Directory created")
else:
    print("Directory already exists")

if not os.path.exists(os.path.expanduser("~/Documents/MHWildsMods/config.json")):
    with open(os.path.expanduser("~/Documents/MHWildsMods/config.json"), "w") as f:
        f.write('{"gamedirectory": "", "modsdirectory": "", "mods": []}')
    print("Config file created")
else:
    print("Config file already exists")

modManager = ModManager(
    "/home/saik/.steam/steam/steamapps/common/MonsterHunterWilds",
    "/home/saik/Documents/MHWildsMods",
)

window = MainWindow(modManager)

window.show()

# Required files:
# - Documents/MHWildsMods/
# - Documents/MHWildsMods/config.json


app.exec()
