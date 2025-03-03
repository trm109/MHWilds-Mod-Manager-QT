from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QTabWidget,
    QLabel,
    QFormLayout,
    QListWidget,
)
from tab_home import HomeTab
from tab_mods import ModsTab
from tab_settings import SettingsTab


class MainWindow(QMainWindow):
    def __init__(self, modManager):
        super().__init__()

        self.title = "Mod Manager"
        self.width = 800
        self.height = 600

        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)

        self.tab_widget = ManagerTabs(modManager)
        self.setCentralWidget(self.tab_widget)
        self.show()


class ManagerTabs(QWidget):
    def __init__(self, modManager):
        super().__init__()
        self.layout = QVBoxLayout(self)

        tabs = QTabWidget()
        tabs.resize(300, 200)

        homeTab = HomeTab()
        modsTab = ModsTab(modManager)
        settingsTab = SettingsTab(modManager)

        tabs.addTab(homeTab, "Home")
        tabs.addTab(modsTab, "Mods")
        tabs.addTab(settingsTab, "Settings")

        self.layout.addWidget(tabs)
        self.setLayout(self.layout)
