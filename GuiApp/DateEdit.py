from datetime import datetime
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDateEdit


class DateEdit(QDateEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.setCalendarPopup(True)
        self.setDisplayFormat("dd.MM.yyyy")
        self.setDate(QDate(datetime.now().date()))
        self.setStyleSheet("""
                            font: 15pt "Microsoft YaHei UI Light";
                            font-weight: bold;
                            background-color: rgb(255, 198, 208);
                            border: none;
                            border-radius: 0px;
                                """)
