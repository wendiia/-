--
-- ���� ������������ � ������� SQLiteStudio v3.3.3 � �� ��� 22 19:05:50 2022
--
-- �������������� ��������� ������: windows-1251
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- �������: cake
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
                     '�������',
                     1500
                 ),
                 (
                     2,
                     '��������',
                     1200
                 ),
                 (
                     3,
                     '��������',
                     2000
                 ),
                 (
                     4,
                     '������',
                     4000
                 );

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
