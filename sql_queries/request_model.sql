-- Requete pour creer le dataframe de l entrainement du model de prediction

SELECT o.*, c.*
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered' AND o.order_purchase_timestamp BETWEEN '2017-07-01 00:00:00' AND '2018-01-01 00:00:00';
