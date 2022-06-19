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
GROUP BY name_cake