from PyQt6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QHBoxLayout,
    QCheckBox,
)
import os
import zipfile
from mod_manager import ModManager, Mod, File


class ModsTab(QWidget):
    def __init__(self, modManager):
        super().__init__()
        self.layout = QFormLayout(self)

        self.modManager = modManager

        self.modList = ModList()

        refreshButton = QPushButton("Refresh")
        refreshButton.clicked.connect(self.refreshMods)

        self.layout.addRow(QLabel("Mods"))
        self.layout.addRow(self.modList)
        self.layout.addRow(refreshButton)

        self.setLayout(self.layout)

    def refreshMods(self):
        self.modManager.getMods()
        self.modList.modList.clear()
        for mod in self.modManager.mods:
            item = QListWidgetItem()
            item.setSizeHint(self.modList.sizeHint())
            self.modList.modList.addItem(item)
            self.modList.modList.setItemWidget(item, ModWidget(mod.filename))


class ModList(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.modList = QListWidget()

        self.layout.addWidget(self.modList)
        self.setLayout(self.layout)


# Widget for each mod in the mod list
# Takes in the name of the mod
class ModWidget(QWidget):
    def __init__(self, filename):
        super().__init__()
        self.layout = QHBoxLayout(self)

        self.filename = filename

        # name = filename without the .zip extension
        label = QLabel(filename.replace(".zip", ""))
        self.layout.addWidget(label)

        # CheckBox to disable or enable the mod
        self.enableBox = QCheckBox("Enable")
        self.enableBox.stateChanged.connect(self.handleToggle)
        self.layout.addWidget(self.enableBox)

        self.setLayout(self.layout)

    def handleToggle(self, state):
        # state is either 0 or 2 (off or on)
        print(state)
        if state == 0:
            print("uninstalling")
            uninstallMod(self.filename)
        else:
            print("installing")
            installMod(self.filename)
