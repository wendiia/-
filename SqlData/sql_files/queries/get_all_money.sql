SELECT SUM(cost)
FROM orders
INNER JOIN cake USING(id_cake)

