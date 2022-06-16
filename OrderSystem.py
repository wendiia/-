from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QDate
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtWidgets import QMainWindow
import asyncio
import SqlData
from GuiApp import *
WINDOW_SIZE = 0


class OrderSystem(QMainWindow):
    def __init__(self):
        self.all_money = None
        self.ex = None
        self.dict_cake_id = {}  # словарь {id_cake: name_cake}, из таблицы cake (cake_db)
        self.widgets_mas = []  # экземпляры объектов класса виджетов: [[Combo_cakes(), Date_edit(), Date_edit()]]
        self.ingredients = []
        self.min_date = ""
        self.max_date = ""
        self.row_flag = True
        self.animation = None
        self.click_position = None
        QMainWindow.__init__(self)

        self.ui = UiMainWindow(self)
        self.ui.setup_ui()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        QtWidgets.QSizeGrip(self.ui.size_grip)

        def move_window(e):
            if not self.isMaximized():
                if e.buttons() == Qt.LeftButton:
                    self.move(self.pos() + e.globalPos() - self.click_position)
                    self.click_position = e.globalPos()
                    e.accept()

        self.ui.main_header.mouseMoveEvent = move_window
        self.ui.btn_toggle.clicked.connect(lambda: self.slide_left_menu())
        self.ui.stacked_widget.setCurrentWidget(self.ui.orders_page)
        self.settings_ui_btns()

        self.db = "./SqlData/CakeDb.db"  # подумай где лучше хранить в датабазе или тут
        asyncio.run(self.main_async())

        self.ui.date_begin_ingr.setDate(QDate.fromString(self.min_date, "yyyy-MM-dd"))
        self.ui.date_end_ingr.setDate(QDate.fromString(self.max_date, "yyyy-MM-dd"))
        self.ui.combo_ingr.addItems(self.ingredients)

        # вызов начальных ф-ий
        self.clicked_btn()
        self.load_date()  # загрузка изначальнеых данных с бд
        self.list_ingredients()
        self.show()

    def mousePressEvent(self, event):
        self.click_position = event.globalPos()

    def slide_left_menu(self):
        width = self.ui.left_side_menu.width()
        if width == 50:
            new_width = 160
        else:
            new_width = 50
        self.animation = QPropertyAnimation(self.ui.left_side_menu, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def settings_ui_btns(self):
        self.ui.btn_min.clicked.connect(lambda: self.showMinimized())
        self.ui.btn_restore.clicked.connect(lambda: self.restore_maximize_win())
        self.ui.btn_close.clicked.connect(lambda: self.close())
        self.ui.btn_home_menu.clicked.connect(lambda: self.ui.stacked_widget.setCurrentWidget(self.ui.home_page))
        self.ui.btn_orders_menu.clicked.connect(lambda: self.ui.stacked_widget.setCurrentWidget(self.ui.orders_page))
        self.ui.btn_products_menu.clicked.connect(lambda:
                                                  self.ui.stacked_widget.setCurrentWidget(self.ui.products_page))

    def restore_maximize_win(self):
        global WINDOW_SIZE
        win_status = WINDOW_SIZE
        if win_status == 0:
            WINDOW_SIZE = 1
            self.showMaximized()
        else:
            WINDOW_SIZE = 0
            self.showNormal()

    async def main_async(self):
        self.ex = SqlData.Database(self.db)
        result = await asyncio.gather(self.ex.min_max_dates(), self.ex.get_ingredients(),
                                      self.ex.cake_id(), self.ex.orders_data())
        self.min_date, self.max_date = result[0][0], result[0][1]
        self.ingredients = result[1]
        self.dict_cake_id = result[2]

    def clicked_btn(self):
        """Обработчик кнопок"""
        self.ui.btn_load.clicked.connect(self.load_date)
        self.ui.btn_add.clicked.connect(self.add_new_row)
        self.ui.btn_del.clicked.connect(self.delete_row)
        self.ui.btn_save.clicked.connect(self.save_data)
        self.ui.btn_products.clicked.connect(self.list_ingredients)

    def load_date(self):
        """
        Загрузка данных с бд sql CakeDb.db. Срабатывает при нажатии на кнопку 'Загрузить'.
        """
        # очищение списков, хранящих экземпляры виджетов comboBox и dateEdit
        self.widgets_mas.clear()
        data_orders = asyncio.run(self.ex.orders_data())
        all_money = f"Итоговая прибыль: {str(asyncio.run(self.ex.all_money())[0][0]) } руб."
        self.ui.lbl_cost.setText(all_money)

        self.ui.tbl.setRowCount(0)

        for row_number, row_data in enumerate(data_orders):  # проход по данным таблицы sql
            # вставка новой строки и добавление виджетов в списки
            self.ui.tbl.insertRow(row_number)
            self.widgets_mas.append([ComboPickCake(self, self.dict_cake_id), DateEdit(self),
                                     DateEdit(self)])

            for col_number, col_data in enumerate(row_data):  # заполнение таблицы данными
                if col_number not in [4, 5, 6]:
                    self.ui.tbl.setItem(row_number, col_number, QtWidgets.QTableWidgetItem(str(col_data)))
                elif col_number == 4:
                    self.ui.tbl.setCellWidget(row_number, col_number, self.widgets_mas[row_number][0])
                    self.widgets_mas[row_number][0].setCurrentText(col_data)
                elif col_number == 5:
                    date = QDate.fromString(col_data, "yyyy-MM-dd")
                    self.ui.tbl.setCellWidget(row_number, col_number, self.widgets_mas[row_number][1])
                    self.widgets_mas[row_number][1].setDate(QDate(date))
                elif col_number == 6:
                    date = QDate.fromString(col_data, "yyyy-MM-dd")
                    self.ui.tbl.setCellWidget(row_number, col_number, self.widgets_mas[row_number][2])
                    self.widgets_mas[row_number][2].setDate(QDate(date))

        self.ui.lbl_info_tbl.setText("Данные загружены")
        self.row_flag = True

    def save_data(self):
        """Сохранение данных в таблицу sql. Срабатывает при нажатии на кнопку 'Сохранить'"""
        try:
            data = []  # список, хранящий данные из таблицы для составления sql запроса

            for row in range(self.ui.tbl.rowCount()):  # заполнение data
                data.append([])
                if not self.ui.tbl.item(row, 0).text().isdigit():
                    raise Exception
                data[row].append(self.ui.tbl.item(row, 0).text())
                data[row].append(self.ui.tbl.item(row, 1).text())
                data[row].append(self.ui.tbl.item(row, 2).text())
                data[row].append(self.ui.tbl.item(row, 3).text())
                data[row].append(self.dict_cake_id[self.widgets_mas[row][0].currentText()])
                two_date = [self.widgets_mas[row][1].date().toPyDate().strftime('%Y-%m-%d'),
                            self.widgets_mas[row][2].date().toPyDate().strftime('%Y-%m-%d')]
                data[row].append(two_date[0])
                data[row].append(two_date[1])

            save_rows_count = asyncio.run(self.ex.save_data(data))
            self.ui.lbl_info_tbl.setText(f"Данные были сохранены: (кол-во: {save_rows_count})")
            self.row_flag = True

        except AttributeError:  # если ячейка(ки) пустые или неправильный тип вводимых данных
            self.ui.lbl_info_tbl.setText('Заполните все поля корректно')

    def add_new_row(self):
        """
        Добавление новой строки.Срабатывает при нажатии на кнопку 'Добавить'
        Без сохранения данных можно добавить только одну строку, за это отвечает self.row_flag
        """
        if self.row_flag:  # если была добавлена одна несохранненая строка
            row_position = self.ui.tbl.rowCount()
            new_id = str(int(self.ui.tbl.item(row_position - 1, 0).text()) + 1)

            # добавление новой строки и виджетов в списки их хранения
            self.ui.tbl.insertRow(row_position)
            self.widgets_mas.append([ComboPickCake(self, self.dict_cake_id), DateEdit(self), DateEdit(self)])

            # вставка виджетов в таблицу
            self.ui.tbl.setItem(row_position, 0, QtWidgets.QTableWidgetItem(new_id))
            self.ui.tbl.setCellWidget(row_position, 4, self.widgets_mas[row_position][0])
            self.ui.tbl.setCellWidget(row_position, 5, self.widgets_mas[row_position][1])
            self.ui.tbl.setCellWidget(row_position, 6, self.widgets_mas[row_position][2])
            self.ui.tbl.setItem(row_position, 7, QtWidgets.QTableWidgetItem("-"))

            self.row_flag = False
        else:  # попытка добавить более одной несохранненой строки
            self.ui.lbl_info_tbl.setText('Сохраните таблицу')

    def delete_row(self):
        """Удаление выбранной строки. Срабатывает при нажатии на кнопку 'Удалить'"""
        if self.ui.tbl.rowCount() > 0 and self.ui.tbl.currentRow() != -1:  # если таблица непустая
            current_row = self.ui.tbl.currentRow()
            self.ui.tbl.removeRow(current_row)
            # удаление экземпляров виджетов
            del self.widgets_mas[current_row]

    def list_ingredients(self):
        self.min_date = self.ui.date_begin_ingr.date().toPyDate().strftime('%Y-%m-%d')
        self.max_date = self.ui.date_end_ingr.date().toPyDate().strftime('%Y-%m-%d')
        self.ui.list_ingredients.clear()
        result_list = asyncio.run(self.ex.list_ingredients(self.ui.combo_ingr.currentText(),
                                                           self.min_date, self.max_date))
        self.ui.list_ingredients.addItems(result_list)
