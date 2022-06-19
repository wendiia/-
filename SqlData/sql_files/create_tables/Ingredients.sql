--
-- Файл сгенерирован с помощью SQLiteStudio v3.3.3 в Вс май 22 19:18:18 2022
--
-- Использованная кодировка текста: windows-1251
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: ingredients
CREATE TABLE IF NOT EXISTS ingredients (
    id_ingr INTEGER PRIMARY KEY NOT NULL,
    name_ingr VARCHAR (35) 
);

INSERT INTO ingredients (
                            id_ingr,
                            name_ingr
                        )
                        VALUES (
                            1,
                            'масло сливочное'
                        ),
                        (
                            2,
                            'сахар'
                        ),
                        (
                            3,
                            'мед'
                        ),
                        (
                            4,
                            'сода'
                        ),
                        (
                            5,
                            'яйца'
                        ),
                        (
                            6,
                            'мука'
                        ),
                        (
                            7,
                            'сметана 15-20%'
                        ),
                        (
                            8,
                            'вода'
                        ),
                        (
                            9,
                            'водка'
                        ),
                        (
                            10,
                            'уксус 9%'
                        ),
                        (
                            11,
                            'соль'
                        ),
                        (
                            12,
                            'молоко'
                        ),
                        (
                            13,
                            'ванильный сахар'
                        ),
                        (
                            14,
                            'банка сгущенки'
                        ),
                        (
                            15,
                            'кефир'
                        ),
                        (
                            16,
                            'творог 9%'
                        ),
                        (
                            17,
                            'сливки'
                        ),
                        (
                            18,
                            'коньяк'
                        );

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
