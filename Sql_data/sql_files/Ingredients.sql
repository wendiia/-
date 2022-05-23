--
-- ���� ������������ � ������� SQLiteStudio v3.3.3 � �� ��� 22 19:18:18 2022
--
-- �������������� ��������� ������: windows-1251
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- �������: ingredients
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
                            '����� ���������'
                        ),
                        (
                            2,
                            '�����'
                        ),
                        (
                            3,
                            '���'
                        ),
                        (
                            4,
                            '����'
                        ),
                        (
                            5,
                            '����'
                        ),
                        (
                            6,
                            '����'
                        ),
                        (
                            7,
                            '������� 15-20%'
                        ),
                        (
                            8,
                            '����'
                        ),
                        (
                            9,
                            '�����'
                        ),
                        (
                            10,
                            '����� 9%'
                        ),
                        (
                            11,
                            '����'
                        ),
                        (
                            12,
                            '������'
                        ),
                        (
                            13,
                            '��������� �����'
                        ),
                        (
                            14,
                            '����� ��������'
                        ),
                        (
                            15,
                            '�����'
                        ),
                        (
                            16,
                            '������ 9%'
                        ),
                        (
                            17,
                            '������'
                        ),
                        (
                            18,
                            '������'
                        );

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
