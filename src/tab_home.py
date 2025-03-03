import os
import subprocess
import platform
import webbrowser
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout


class HomeTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        instructionsLabel = QLabel(
            "Due to limitations with the Nexus Mods API, its not possible for mod managers to find/search/download mods.\nHow to install a mod:\n   1. Visit the Nexus Mods website\n   2. Download a mod (do not forget their dependencies) to the Documents/MHWildsMods folder.\n   3. Go to the 'Mods' tab.\n   4. Click 'Refresh'\n   5. Toggle the mod on/off\n   6. Start your game!\n\n\nTo get started, click the button below to open the Nexus Mods page for Monster Hunter: World."
        )
        self.layout.addWidget(instructionsLabel)
        # Bar that holds both buttons
        buttonBar = QHBoxLayout()
        self.layout.addLayout(buttonBar)

        # Open Mods Folder Button
        openModsFolderButton = QPushButton("Open Mods Folder")
        openModsFolderButton.clicked.connect(openModsFolder)
        buttonBar.addWidget(openModsFolderButton)

        # Open Nexus Mods Button
        openNexusButton = QPushButton("Open Nexus Mods")
        openNexusButton.clicked.connect(
            lambda: webbrowser.open("https://www.nexusmods.com/monsterhunterwilds")
        )
        buttonBar.addWidget(openNexusButton)

        # Open Project GitHub Button

        self.setLayout(self.layout)


def openModsFolder():
    # Determine if Windows or Linux
    if platform.system() == "Windows":
        os.system("start %userprofile%/Documents/MHWildsMods")  # TODO UNTESTED
    else:
        subprocess.Popen(["xdg-open", os.path.expanduser("~/Documents/MHWildsMods")])
