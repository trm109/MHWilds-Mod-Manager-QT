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
    QMessageBox,
)
import os
import zipfile
from mod_manager import ModManager, Mod


class ModsTab(QWidget):
    def __init__(self, modManager):
        super().__init__()
        self.layout = QFormLayout(self)

        self.modManager = modManager

        self.modList = ModList()

        refreshButton = QPushButton("Refresh")
        refreshButton.clicked.connect(self.refreshMods)
        self.refreshMods()  # Refresh mods on startup
        # TODO make refresh also re-import mods

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
            self.modList.modList.setItemWidget(item, ModWidget(mod))


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
    def __init__(self, mod):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.mod = mod
        self.name = mod.modName
        self.version = mod.version
        self.description = mod.description
        self.author = mod.author

        # name
        label = QLabel(self.name)
        self.layout.addWidget(label)
        # version
        label = QLabel(self.version)
        self.layout.addWidget(label)
        # description
        label = QLabel(self.description)
        self.layout.addWidget(label)
        # author
        label = QLabel(self.author)
        self.layout.addWidget(label)

        # CheckBox to disable or enable the mod
        self.enableBox = QCheckBox("Enable")
        self.enableBox.setChecked(self.mod.enabled)
        self.enableBox.stateChanged.connect(self.handleToggle)
        self.layout.addWidget(self.enableBox)

        # Make all the widgets the same width
        self.layout.setStretchFactor(label, 1)

        self.setLayout(self.layout)

    def handleToggle(self, state):
        # state is either 0 or 2 (off or on)
        print(state)
        if state == 0:
            print("uninstalling")
            self.mod.uninstall()
        else:
            print("installing")
            self.mod.install()
            specialCase = self.mod.determineSpecialCase()
            if specialCase is not None:
                if specialCase.startswith("ERROR"):
                    dialog = QMessageBox()
                    dialog.setWindowTitle("Error")
                    dialog.setText(
                        "Error while installing "
                        + self.mod.modName
                        + "\n"
                        + specialCase
                    )
                    dialog.exec()
