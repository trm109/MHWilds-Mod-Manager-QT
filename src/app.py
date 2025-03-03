from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMainWindow

# import MainWindow from src/main_window.py
from main_window import MainWindow
import sys
import os
import platform
from mod_manager import ModManager

app = QApplication(sys.argv)

modManager = ModManager(
    "/home/saik/.steam/steam/steamapps/common/MonsterHunterWilds",
    "/home/saik/Documents/MHWildsMods",
)

window = MainWindow(modManager)

window.show()

# Required files:
# - Documents/MHWildsMods/
# - Documents/MHWildsMods/config.json
os.makedirs(os.path.expanduser("~/Documents/MHWildsMods"), exist_ok=True)
if not os.path.exists(os.path.expanduser("~/Documents/MHWildsMods/config.json")):
    with open(os.path.expanduser("~/Documents/MHWildsMods/config.json"), "w") as f:
        f.write('{"gamedirectory": "", "modsdirectory": "", "mods": []}')


app.exec()
