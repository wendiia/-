from PyQt6.QtWidgets import QComboBox


class ComboPickCake(QComboBox):
    def __init__(self, parent, id_cakes):
        super().__init__(parent)
        self.addItems(list(id_cakes.keys()))
        self.setAutoFillBackground(False)
        self.setEditable(True)
        self.setFrame(True)
