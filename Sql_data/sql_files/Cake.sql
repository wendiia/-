--
-- Файл сгенерирован с помощью SQLiteStudio v3.3.3 в Вс май 22 19:05:50 2022
--
-- Использованная кодировка текста: windows-1251
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: cake
CREATE TABLE IF NOT EXISTS cake (
    id_cake INTEGER PRIMARY KEY NOT NULL,
    name_cake VARCHAR (40),
    cost INTEGER
);

INSERT INTO cake (
                     id_cake,
                     name_cake,
                     cost
                 )
                 VALUES (
                     1,
                     'Медовик',
                     1500
                 ),
                 (
                     2,
                     'Тирамису',
                     1200
                 ),
                 (
                     3,
                     'Наполеон',
                     2000
                 ),
                 (
                     4,
                     'Нежный',
                     4000
                 );

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
