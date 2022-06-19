--
-- Файл сгенерирован с помощью SQLiteStudio v3.3.3 в Вс май 22 19:19:00 2022
--
-- Использованная кодировка текста: windows-1251
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: units
CREATE TABLE IF NOT EXISTS units (
    id_unit INTEGER PRIMARY KEY NOT NULL,
    name_unit VARCHAR (10) 
);

INSERT INTO units (
                      id_unit,
                      name_unit
                  )
                  VALUES (
                      1,
                      'г'
                  ),
                  (
                      2,
                      'кг'
                  ),
                  (
                      3,
                      'мл'
                  ),
                  (
                      4,
                      'л'
                  ),
                  (
                      5,
                      'шт'
                  ),
                  (
                      6,
                      'ч.л.'
                  ),
                  (
                      7,
                      'ст.л.'
                  );

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
