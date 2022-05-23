from datetime import datetime
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QDateEdit


class DateEdit(QDateEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.setCalendarPopup(True)
        self.setDisplayFormat("dd.MM.yyyy")
        self.setDate(QDate(datetime.now().date()))
