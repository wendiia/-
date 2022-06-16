import sqlite3 as sql
import aiosqlite


class Database:
    def __init__(self, db_path):
        self.max_date = ""
        self.min_date = ""
        self.db = db_path
        self.connection = sql.connect(self.db)
        self.cur = self.connection.cursor()

        sql_files_list = ['./SqlData/sql_files/Cake.sql', './SqlData/sql_files/Ingredients.sql',
                          './SqlData/sql_files/Orders.sql', './SqlData/sql_files/Recipes.sql',
                          './SqlData/sql_files/Units.sql']
        for i in sql_files_list:
            with open(i, 'r') as sql_file:
                sql_script = sql_file.read()
                try:
                    self.cur.executescript(sql_script)
                    self.connection.commit()
                except sql.Error as e:
                    self.error = f"Ошибка выполнения запроса {e} Имя файла: {sql_file.name}"  # убрать
        if self.connection:
            self.connection.close()

    async def orders_data(self):
        query = "SELECT id_main, surname, name, phone, name_cake, date_begin, date_end, cost " \
                "FROM cake INNER JOIN orders USING (id_cake)"
        async with aiosqlite.connect(self.db) as db:
            async with db.execute(query) as cursor:
                cur_result = await cursor.fetchall()
            return cur_result

    async def save_data(self, data):
        query = """INSERT INTO orders (id_main, surname, name, phone, id_cake, date_begin, date_end)
                   VALUES (?, ?, ?, ?, ?, ?, ?)"""
        async with aiosqlite.connect(self.db) as db:
            async with db.cursor() as cursor:
                await cursor.execute("DELETE FROM orders")  # удаление старых данных с таблицы sql
                await cursor.executemany(query, data)  # вставка новых данных в таблицу sql
                count_rows = cursor.rowcount
            await db.commit()
            return count_rows

    async def list_ingredients(self, ingredient, min_date, max_date):
        list_ingr = []
        data = [min_date, max_date]
        if ingredient == "Все ингредиенты":
            query = self.get_list_ingredients()
        else:
            query = self.get_list_ingredients_filter()
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
        query = self.get_all_money()
        async with aiosqlite.connect(self.db) as db:
            async with db.execute(query) as cursor:
                cur_result = await cursor.fetchall()
            return cur_result

    async def min_max_dates(self):
        async with aiosqlite.connect(self.db) as db:
            async with db.cursor() as cur:
                await cur.execute("SELECT MIN(date_begin), MAX(date_begin) FROM orders")
                self.min_date, self.max_date = await cur.fetchone()
            return self.min_date, self.max_date

    async def get_ingredients(self):
        async with aiosqlite.connect(self.db) as db:
            async with db.cursor() as cur:
                await cur.execute("SELECT name_ingr FROM ingredients")
                result = await cur.fetchall()
                result = [" ".join(x) for x in result]
            return result

    async def cake_id(self):
        """Формирование dict_cake_id, где {id_cake: name_cake}, из таблицы cake (cake_db)"""
        dict_cake_id = {}
        async with aiosqlite.connect(self.db) as db:
            async with db.execute("SELECT id_cake, name_cake FROM cake") as cursor:
                async for i in cursor:
                    dict_cake_id[i[1]] = i[0]
            return dict_cake_id

    @staticmethod
    def get_list_ingredients():
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
        return query

    @staticmethod
    def get_list_ingredients_filter():
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
        return query

    @staticmethod
    def get_all_money():
        query = """
                    SELECT SUM(cost)
                    FROM orders 
                    INNER JOIN cake USING(id_cake)"""
        return query
