import sqlite3 as sql


class Database:
    def __init__(self, bd_path):
        self.connection = sql.connect(bd_path)
        self.cur = self.connection.cursor()
        self.error = "Таблицы созданы"  # убрать

        sql_files_list = ['./Sql_data/sql_files/Cake.sql', './Sql_data/sql_files/Ingredients.sql',
                          './Sql_data/sql_files/Orders.sql', './Sql_data/sql_files/Recipes.sql',
                          './Sql_data/sql_files/Units.sql']
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

        # self.add_users()
        # self.output_users()

    # def output_users(self):
    #     self.cur.execute("SELECT * FROM users;")
    #     one_result = self.cur.fetchall()
    #     print(one_result)
    #
    # def add_users(self, ):
    #     print('strings amount')
    #     strings_amount = int(input())
    #     data_tuple = ['', '', '', '']
    #     for i in range(strings_amount):
    #         data_tuple[0] = i
    #         print(i + 1)
    #         data_tuple[1] = input()
    #         data_tuple[2] = input()
    #         data_tuple[3] = input()
    #         self.cur.execute("INSERT INTO users VALUES (?, ?, ?, ?);", data_tuple)
    #         self.connection.commit()
    #
