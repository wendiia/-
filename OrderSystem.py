#!/usr/bin/python
# -*- coding: windows-1251 -*-
import sqlite3
from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate
import Sql_data
from GuiApp import *


class OrderSystem(UiMainWindow):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.bd = "./Sql_data/CakeDb.db"
        Sql_data.Database(self.bd)
        self.dict_cake_id = {}  # словарь {id_cake: name_cake}, из таблицы cake (cake_db)
        self.widgets_mas = []  # екземпляры объектов класса виджетов: [[Combo_cakes(), Date_edit(), Date_edit()]]
        self.row_flag = True

        connection = sqlite3.connect(self.bd)
        cur = connection.cursor()
        query = """SELECT MIN(date_begin), MAX(date_begin)
                   FROM orders"""
        cur.execute(query)
        min_date, max_date = cur.fetchone()

        date_ingredients = (QDate.fromString(min_date, "yyyy-MM-dd"), QDate.fromString(max_date, "yyyy-MM-dd"))
        self.date_begin_ingr.setDate(QDate(date_ingredients[0]))
        self.date_end_ingr.setDate(QDate(date_ingredients[1]))
        query = """SELECT name_ingr
                   FROM ingredients"""
        cur.execute(query)
        result = [" ".join(x) for x in cur.fetchall()]
        self.combo_ingr.addItem("Все ингредиенты")
        self.combo_ingr.addItems(result)
        connection.close()

        # вызов начальных ф-ий
        self.cake_id()
        self.clicked_btn()
        self.load_date()  # загрузка изначальнеых данных с бд
        self.list_ingedients()

    def list_ingedients(self):
        connection = sqlite3.connect(self.bd)
        cur = connection.cursor()
        min_date = self.date_begin_ingr.date().toPyDate().strftime('%Y-%m-%d')
        max_date = self.date_end_ingr.date().toPyDate().strftime('%Y-%m-%d')
        data = [min_date, max_date]
        if self.combo_ingr.currentText() == "Все ингредиенты":
            query = """
                        SELECT name_ingr, SUM(count), name_unit
                        FROM
                            (SELECT id_cake
                            FROM orders
                            WHERE date_begin BETWEEN ? and ?) query1
                        INNER JOIN recipes USING (id_cake)
                        INNER JOIN ingredients USING (id_ingr)
                        INNER JOIN units USING (id_unit)
                        GROUP BY name_ingr"""
        else:
            query = """
                        SELECT name_cake, name_ingr, SUM(count), name_unit
                        FROM
                            (SELECT id_cake
                            FROM orders
                            WHERE date_begin BETWEEN ? and ?) query1
                        INNER JOIN cake USING(id_cake)
                        INNER JOIN recipes USING (id_cake)
                        INNER JOIN ingredients USING (id_ingr)
                        INNER JOIN units USING (id_unit)
                        WHERE name_ingr =  ?
                        GROUP BY name_cake"""
            data.append(self.combo_ingr.currentText())  # ------------------------!
        length_data = len(data)
        self.list_ingr.clear()
        for i in cur.execute(query, data):
            if length_data == 3:
                result_str = f"{i[0]}{'-' * (30 - len(i[1]))}{i[2]} {i[3]}"
            else:
                result_str = f"{i[0]}{'-' * (30 - len(i[0]))}{i[1]} {i[2]}"
            self.list_ingr.addItem(result_str)
        connection.close()

    def cake_id(self):
        """Формирование dict_cake_id, где {id_cake: name_cake}, из таблицы cake (cake_db)"""
        connection = sqlite3.connect(self.bd)
        cur = connection.cursor()
        query = "SELECT id_cake, name_cake " \
                "FROM cake"
        for i in cur.execute(query):
            self.dict_cake_id[i[1]] = i[0]
        connection.close()

    def clicked_btn(self):
        """Обработчик кнопок"""
        self.btn_load.clicked.connect(self.load_date)
        self.btn_add.clicked.connect(self.add_new_row)
        self.btn_del.clicked.connect(self.delete_row)
        self.btn_save.clicked.connect(self.save_data)
        self.btn_list_update.clicked.connect(self.list_ingedients)

    def load_date(self):
        """
        Загрузка данных с бд sql CakeDb.db. Срабатывает при нажатии на кнопку 'Загрузить'.
        """
        # очищение списков, хранящих экземпляры виджетов comboBox и dateEdit
        self.widgets_mas.clear()

        connection = sqlite3.connect(self.bd)
        cur = connection.cursor()
        query = "SELECT id_main, fio, phone, name_cake, date_begin, date_end, cost " \
                "FROM cake INNER JOIN orders USING (id_cake)"

        self.tbl.setRowCount(0)
        for row_number, row_data in enumerate(cur.execute(query)):  # проход по данным таблицы sql
            # вставка новой строки и добавление виджетов в списки
            self.tbl.insertRow(row_number)

            self.widgets_mas.append([ComboPickCake(self.main_window, self.dict_cake_id), DateEdit(self.main_window),
                                     DateEdit(self.main_window)])

            for col_number, col_data in enumerate(row_data):  # заполнение таблицы данными
                if col_number not in [3, 4, 5]:
                    self.tbl.setItem(row_number, col_number, QtWidgets.QTableWidgetItem(str(col_data)))
                elif col_number == 3:
                    self.tbl.setCellWidget(row_number, col_number, self.widgets_mas[row_number][0])
                    self.widgets_mas[row_number][0].setCurrentText(col_data)
                elif col_number == 4:
                    date = QDate.fromString(col_data, "yyyy-MM-dd")
                    self.tbl.setCellWidget(row_number, col_number, self.widgets_mas[row_number][1])
                    self.widgets_mas[row_number][1].setDate(QDate(date))
                elif col_number == 5:
                    date = QDate.fromString(col_data, "yyyy-MM-dd")
                    self.tbl.setCellWidget(row_number, col_number, self.widgets_mas[row_number][2])
                    self.widgets_mas[row_number][2].setDate(QDate(date))

        connection.close()
        self.lbl_info.setText("Данные загружены")
        self.row_flag = True

    def add_new_row(self):
        """
        Добавление новой строки.Срабатывает при нажатии на кнопку 'Добавить'
        Без сохранения данных можно добавить только одну строку, за это отвечает self.row_flag
        """
        if self.row_flag:  # если была добавлена одна несохранненая строка
            row_position = self.tbl.rowCount()
            new_id = str(int(self.tbl.item(row_position - 1, 0).text()) + 1)

            # добавление новой строки и виджетов в списки их хранения
            self.tbl.insertRow(row_position)
            self.widgets_mas.append([ComboPickCake(self.main_window, self.dict_cake_id), DateEdit(self.main_window),
                                     DateEdit(self.main_window)])

            # вставка виджетов в таблицу
            self.tbl.setItem(row_position, 0, QtWidgets.QTableWidgetItem(new_id))
            self.tbl.setCellWidget(row_position, 3, self.widgets_mas[row_position][0])
            self.tbl.setCellWidget(row_position, 4, self.widgets_mas[row_position][1])
            self.tbl.setCellWidget(row_position, 5, self.widgets_mas[row_position][2])
            self.tbl.setItem(row_position, 6, QtWidgets.QTableWidgetItem("-"))

            self.row_flag = False
        else:  # попытка добавить более одной несохранненой строки
            self.lbl_info.setText('Сохраните таблицу')

    def delete_row(self):
        """Удаление выбранной строки. Срабатывает при нажатии на кнопку 'Удалить'"""
        if self.tbl.rowCount() > 0 and self.tbl.currentRow() != -1:  # если таблица непустая
            current_row = self.tbl.currentRow()
            self.tbl.removeRow(current_row)
            # удаление экземпляров виджетов
            del self.widgets_mas[current_row]

    def save_data(self):
        """Сохранение данных в таблицу sql. Срабатывает при нажатии на кнопку 'Сохранить'"""
        try:
            data = []  # список, хранящий данные из таблицы для составления sql запроса

            for row in range(self.tbl.rowCount()):  # заполнение data
                data.append([])
                if not self.tbl.item(row, 0).text().isdigit():
                    raise Exception
                data[row].append(self.tbl.item(row, 0).text())
                data[row].append(self.tbl.item(row, 1).text())
                data[row].append(self.tbl.item(row, 2).text())
                data[row].append(self.dict_cake_id[self.widgets_mas[row][0].currentText()])
                two_date = [self.widgets_mas[row][1].date().toPyDate().strftime('%Y-%m-%d'),
                            self.widgets_mas[row][2].date().toPyDate().strftime('%Y-%m-%d')]
                data[row].append(two_date[0])
                data[row].append(two_date[1])

            connection = sqlite3.connect(self.bd)
            cur = connection.cursor()
            query = "INSERT INTO orders (id_main, fio, phone, id_cake, date_begin, date_end)" \
                    "VALUES (?, ?, ?, ?, ?, ?);"
            cur.execute("DELETE FROM orders")  # удаление старых данных с таблицы sql
            cur.executemany(query, data)  # вставка новых данных в таблицу sql
            self.lbl_info.setText(f"Данные были сохранены: (кол-во: {cur.rowcount})")
            connection.commit()
            connection.close()
            self.row_flag = True

        except AttributeError as e:  # если ячейка(ки) пустые или неправильный тип вводимых данных
            print(e)
            self.lbl_info.setText('Заполните все поля корректно')
