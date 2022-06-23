from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QDate
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtWidgets import QMainWindow
import asyncio
import SqlData
from GuiApp import *
from asyncqt import asyncSlot
from Singleton import Singleton


@Singleton()
class OrderSystem(QMainWindow):
    """Класс OrderSystem содержит набор функций, импортируемых классов и модулей,
    при помощи которых реализована логика работы приложения

    Note:
        Возможны проблемы с кодировкой в Linux
    """
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = UiMainWindow(self)
        self.ui.setup_ui()
        self.db = SqlData.ex_db
        self.window_size = 0
        self.all_money = ""
        self.dict_cake_id = {}
        self.widgets_mas = []
        self.ingredients = []
        self.min_date, self.max_date = ("", "")
        self.one_row_flag = True
        self.animation = None
        self.click_position = None
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        QtWidgets.QSizeGrip(self.ui.size_grip)
        self.ui.main_header.mouseMoveEvent = self.move_window
        self.ui.btn_toggle.clicked.connect(lambda: self.slide_left_menu())
        self.ui.stacked_widget.setCurrentWidget(self.ui.home_page)
        self.settings_ui_btns()
        self.async_init()
        self.show()

    def move_window(self, e):
        """Позволяет перемещать рабочее окно приложения
        Parameters
        ----------
        e : QMouseEvent
            класс события мыши
        """
        if not self.isMaximized():
            if e.buttons() == Qt.LeftButton:
                self.move(self.pos() + e.globalPos() - self.click_position)
                self.click_position = e.globalPos()
                e.accept()

    @asyncSlot()
    async def async_init(self):
        """
        Точка входа в асинхронность
        """
        result = await asyncio.gather(self.db.min_max_dates(), self.db.get_ingredients(), self.db.cake_id())
        self.min_date, self.max_date = result[0][0], result[0][1]
        self.ingredients = result[1]
        self.dict_cake_id = result[2]
        self.ui.date_begin_ingr.setDate(QDate.fromString(self.min_date, "yyyy-MM-dd"))
        self.ui.date_end_ingr.setDate(QDate.fromString(self.max_date, "yyyy-MM-dd"))
        self.ui.combo_ingr.addItems(self.ingredients)

        await self.load_date()
        await self.clicked_btn()
        await self.list_ingredients()

    async def clicked_btn(self):
        """Присваивание функций кнопкам, которые связаны с управлением таблицей, списком ингредиентов"""
        self.ui.btn_load.clicked.connect(self.load_date)
        self.ui.btn_add.clicked.connect(self.add_new_row)
        self.ui.btn_del.clicked.connect(self.delete_row)
        self.ui.btn_save.clicked.connect(self.save_data)
        self.ui.btn_products.clicked.connect(self.list_ingredients)

    def mousePressEvent(self, event):
        """Срабатывает при нажатии ЛКМ в приложении
        Основное применение - отслеживание координат мыши
        Parameters
        ----------
        event : QMouseEvent
            класс событий мыши
        """
        self.click_position = event.globalPos()

    def slide_left_menu(self):
        """
        Выдвижение левой боковой панели при нажатии на btn_toggle
        """
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
        """
        Присваивание функций кнопкам GUI
        """
        self.ui.btn_min.clicked.connect(lambda: self.showMinimized())
        self.ui.btn_restore.clicked.connect(lambda: self.restore_maximize_win())
        self.ui.btn_close.clicked.connect(lambda: self.close())
        self.ui.btn_home_menu.clicked.connect(lambda: self.ui.stacked_widget.setCurrentWidget(self.ui.home_page))
        self.ui.btn_orders_menu.clicked.connect(lambda: self.ui.stacked_widget.setCurrentWidget(self.ui.orders_page))
        self.ui.btn_products_menu.clicked.connect(lambda:
                                                  self.ui.stacked_widget.setCurrentWidget(self.ui.products_page))

    def restore_maximize_win(self):
        """
        Расширение окна и уменьшение до нормального размера
        """
        win_status = self.window_size
        if win_status == 0:
            self.window_size = 1
            self.showMaximized()
        else:
            self.window_size = 0
            self.showNormal()

    @asyncSlot()
    async def load_date(self):
        """
        Загрузка данных с бд sql CakeDb.db. Срабатывает при нажатии на кнопку 'Загрузить'.
        """
        self.widgets_mas.clear()
        data_orders = await self.db.orders_data()
        all_money = await self.db.all_money()
        all_money = f"Итоговая прибыль: {all_money[0]} руб."
        self.ui.lbl_cost.setText(all_money)
        self.ui.tbl.setRowCount(0)

        for row_number, row_data in enumerate(data_orders):
            self.ui.tbl.insertRow(row_number)
            self.widgets_mas.append([ComboPickCake(self, self.dict_cake_id), DateEdit(self),
                                     DateEdit(self)])

            for col_number, col_data in enumerate(row_data):
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
        self.one_row_flag = True

    @asyncSlot()
    async def list_ingredients(self):
        """
        Формирование всего списка ингредиентов для добавления в comboBox
        """
        self.min_date = self.ui.date_begin_ingr.date().toPyDate().strftime('%Y-%m-%d')
        self.max_date = self.ui.date_end_ingr.date().toPyDate().strftime('%Y-%m-%d')
        self.ui.list_ingredients.clear()
        result_list = await self.db.list_ingredients(self.ui.combo_ingr.currentText(), self.min_date, self.max_date)
        self.ui.list_ingredients.addItems(result_list)

    @asyncSlot()
    async def save_data(self):
        """Сохранение данных в таблицу sql. Срабатывает при нажатии на кнопку 'Сохранить'"""
        try:
            data = []

            for row in range(self.ui.tbl.rowCount()):
                data.append([])
                if not self.ui.tbl.item(row, 0).text().isdigit():
                    self.ui.lbl_info_tbl.setText('ID должен быть числом')
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

            save_rows_count = await self.db.save_data(data)
            self.ui.lbl_info_tbl.setText(f"Данные были сохранены: (кол-во: {save_rows_count})")
            self.one_row_flag = True

        except AttributeError:
            self.ui.lbl_info_tbl.setText('Заполните все поля корректно')

    @asyncSlot()
    async def add_new_row(self):
        """
        Добавление новой строки.Срабатывает при нажатии на кнопку 'Добавить'
        Без сохранения данных можно добавить только одну строку, за это отвечает one_row_flag
        """
        if self.one_row_flag:
            row_position = self.ui.tbl.rowCount()
            res = str((await self.db.last_id_orders())[0] + 1)

            self.ui.tbl.insertRow(row_position)
            self.widgets_mas.append([ComboPickCake(self, self.dict_cake_id), DateEdit(self), DateEdit(self)])

            self.ui.tbl.setItem(row_position, 0, QtWidgets.QTableWidgetItem(res))
            self.ui.tbl.setCellWidget(row_position, 4, self.widgets_mas[row_position][0])
            self.ui.tbl.setCellWidget(row_position, 5, self.widgets_mas[row_position][1])
            self.ui.tbl.setCellWidget(row_position, 6, self.widgets_mas[row_position][2])
            self.ui.tbl.setItem(row_position, 7, QtWidgets.QTableWidgetItem("-"))

            self.one_row_flag = False
        else:
            self.ui.lbl_info_tbl.setText('Сохраните таблицу')

    def delete_row(self):
        """Удаление выбранной строки. Срабатывает при нажатии на кнопку 'Удалить'"""
        if self.ui.tbl.rowCount() > 0 and self.ui.tbl.currentRow() != -1:
            current_row = self.ui.tbl.currentRow()
            self.ui.tbl.removeRow(current_row)
            del self.widgets_mas[current_row]
