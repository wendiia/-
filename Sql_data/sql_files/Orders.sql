--
-- Файл сгенерирован с помощью SQLiteStudio v3.3.3 в Вс май 22 18:31:31 2022
--
-- Использованная кодировка текста: windows-1251
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: orders
CREATE TABLE IF NOT EXISTS orders (
    id_main    INTEGER PRIMARY KEY NOT NULL,
    fio        STRING (40),
    phone      STRING (40),
    id_cake    INTEGER REFERENCES cake (id_cake) ON DELETE CASCADE ON UPDATE CASCADE,
    date_begin DATE,
    date_end   DATE
);

INSERT INTO orders (id_main,
                          fio,
                          phone,
                          id_cake,
                          date_begin,
                          date_end
                      )
                      VALUES
                      (
                          1,
                          'Иванов',
                          79776436578,
                          3,
                          '2022-05-01',
                          '2022-05-02'
                      ),
                      (
                          2,
                          'Сидоров',
                          79776436578,
                          1,
                          '2022-05-02',
                          '2022-05-12'
                      ),
                      (
                          3,
                          'Кургатов',
                          79776436578,
                          2,
                          '2022-06-07',
                          '2022-06-10'
                      ),
                      (
                          4,
                          'Мирин',
                          79776436578,
                          3,
                          '2022-06-25',
                          '2022-06-29'
                      ),
                      (
                          5,
                          'Кургатов',
                          79776436578,
                          2,
                          '2022-07-07',
                          '2022-07-14'
                      ),
                      (
                          6,
                          'Мирин',
                          79776436578,
                          4,
                          '2022-08-11',
                          '2022-08-18'
                      ),
                      (
                          8,
                          'Сидорров',
                          79776436578,
                          1,
                          '2022-08-21',
                          '2022-08-26'
                      ),
                      (
                          9,
                          'Кургатов',
                          79776436578,
                          2,
                          '2022-11-04',
                          '2022-11-14'
                      ),
                      (
                          10,
                          'Мирин',
                          79776436578,
                          3,
                          '2022-11-07',
                          '2022-11-12'
                      ),
                      (
                          11,
                          'Кургатов',
                          79776436578,
                          2,
                          '2022-11-13',
                          '2022-11-15'
                      );

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
