import sqlite3 as sql
import aiosqlite
import os


class Database:
    """Класс Database создает базу данных, если она была не создана, наполняет ее шаблонными данными
        Основная задача - применение запросов к базе данных CakrDb.db
    """
    def __init__(self):
        self.max_date = ""
        self.min_date = ""
        self.db = "./SqlData/CakeDb.db"
        self.connection = sql.connect(self.db)
        self.cur = self.connection.cursor()
        sql_files_list = sorted(os.listdir("./SqlData/sql_files/create_tables/"))
        for i in sql_files_list:
            with open("./SqlData/sql_files/create_tables/" + i, 'r') as sql_file:
                sql_script = sql_file.read()
                try:
                    self.cur.executescript(sql_script)
                    self.connection.commit()
                except sql.Error as e:
                    self.error = f"Ошибка выполнения запроса {e} Имя файла: {sql_file.name}"  # убрать
        if self.connection:
            self.connection.close()

    async def orders_data(self):
        """Составляет и выполняет запрос на взятие данных с таблицы orders
        """
        query = "SELECT id_main, surname, name, phone, name_cake, date_begin, date_end, cost " \
                "FROM cake INNER JOIN orders USING (id_cake)"
        async with aiosqlite.connect(self.db) as db:
            async with db.execute(query) as cursor:
                return await cursor.fetchall()

    async def save_data(self, data):
        """Составляет и выполняет запрос на сохранение данных в таблицу orders
            Parameters
            ----------
            data : list
                список с данными из таблицы приложения
        """
        query = """INSERT INTO orders (id_main, surname, name, phone, id_cake, date_begin, date_end)
                   VALUES (?, ?, ?, ?, ?, ?, ?)"""
        async with aiosqlite.connect(self.db) as db:
            async with db.cursor() as cursor:
                await cursor.execute("DELETE FROM orders")  # удаление старых данных с таблицы sql
                await cursor.executemany(query, data)  # вставка новых данных в таблицу sql
            await db.commit()
            return cursor.rowcount

    async def list_ingredients(self, ingredient, min_date, max_date):
        """Составляет и выполняет запрос на взятие суммарного количество ингредиентов по взятым параметрам
            Parameters
            ----------
            ingredient : str
                выбранный ингредиент из comboBox
            min_date : str
                ранняя дата из таблицы orders
            max_date : str
                поздняя дата из таблицы orders
        """
        list_ingr = []
        data = [min_date, max_date]
        if ingredient == "Все ингредиенты":
            with open("./SqlData/sql_files/queries/get_list_ingredients.sql", 'r') as sql_file:
                query = sql_file.read()
        else:
            with open("./SqlData/sql_files/queries/get_list_ingredients_filter.sql", 'r') as sql_file:
                query = sql_file.read()
            data.append(ingredient)
        length_data = len(data)
        async with aiosqlite.connect(self.db) as db:
            async with db.execute(query, data) as cursor:
                async for i in cursor:
                    if length_data == 3:
                        result_str = f"{i[0]}{'-' * (25 - len(i[1]))}{i[2]} {i[3]}"
                    else:
                        result_str = f"{i[0]}{'-' * (25 - len(i[0]))}{i[1]} {i[2]}"
                    list_ingr.append(result_str)
            return list_ingr

    async def all_money(self):
        """Составляет и выполняет запрос на получение суммарной прибыли
        """
        with open("./SqlData/sql_files/queries/get_all_money.sql", 'r') as sql_file:
            async with aiosqlite.connect(self.db) as db:
                async with db.execute(sql_file.read()) as cursor:
                    return await cursor.fetchone()

    async def min_max_dates(self):
        """Составляет и выполняет запрос на получение ранней и поздней дат
        """
        async with aiosqlite.connect(self.db) as db:
            async with db.cursor() as cur:
                await cur.execute("SELECT MIN(date_begin), MAX(date_begin) FROM orders")
                return await cur.fetchone()

    async def get_ingredients(self):
        """Составляет и выполняет запрос на получение всего спискса ингредиентов
        """
        async with aiosqlite.connect(self.db) as db:
            async with db.cursor() as cur:
                await cur.execute("SELECT name_ingr FROM ingredients")
                return [" ".join(x) for x in await cur.fetchall()]

    async def cake_id(self):
        """
        Составляет и выполняет запрос формирование dict_cake_id, где {id_cake: name_cake}, из таблицы cake (cake_db)
        """
        dict_cake_id = {}
        async with aiosqlite.connect(self.db) as db:
            async with db.execute("SELECT id_cake, name_cake FROM cake") as cursor:
                async for i in cursor:
                    dict_cake_id[i[1]] = i[0]
            return dict_cake_id

    async def last_id_orders(self):
        """
        Составляет и выполняет запрос получение последнего id из таблицы orders
        """
        async with aiosqlite.connect(self.db) as db:
            async with db.execute("SELECT id_main FROM orders ORDER BY id_main DESC LIMIT 1") as cursor:
                return await cursor.fetchone()
