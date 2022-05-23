--
-- ���� ������������ � ������� SQLiteStudio v3.3.3 � �� ��� 22 19:19:00 2022
--
-- �������������� ��������� ������: windows-1251
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- �������: units
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
                      '�'
                  ),
                  (
                      2,
                      '��'
                  ),
                  (
                      3,
                      '��'
                  ),
                  (
                      4,
                      '�'
                  ),
                  (
                      5,
                      '��'
                  ),
                  (
                      6,
                      '�.�.'
                  ),
                  (
                      7,
                      '��.�.'
                  );

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
