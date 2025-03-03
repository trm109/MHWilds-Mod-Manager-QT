from PyQt6.QtWidgets import QWidget, QVBoxLayout


class SettingsTab(QWidget):
    def __init__(self, modManager):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.setLayout(self.layout)
