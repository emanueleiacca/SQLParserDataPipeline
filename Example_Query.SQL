--SELECT

#Group Functions and Aliases:

SELECT first_name, last_name, COUNT(*) AS total_orders
FROM customers
JOIN orders ON customers.id = orders.customer_id
GROUP BY first_name, last_name;

--#Nested Functions:

SELECT customer_id, MAX(EXTRACT(YEAR FROM order_date)) AS last_order_year
FROM orders
GROUP BY customer_id;

--#Complex Joins with Nested Selects:

SELECT c.customer_name, o.order_id, (SELECT SUM(payment_amount) FROM payments WHERE payments.order_id = o.id) AS total_paid
FROM customers c
JOIN orders o ON c.id = o.customer_id;

--#Multiple Nested Selects and Functions:

SELECT e.name, e.position,
   (SELECT AVG(s.salary) FROM employees s WHERE s.department = e.department) AS avg_department_salary,
   (SELECT COUNT(*) FROM projects p WHERE p.manager_id = e.id) AS projects_managed
FROM employees e;

--#Using CONCAT and SUBSTR Functions:

SELECT 
    user_id,
    CONCAT(first_name, ' ', last_name) AS full_name,
    email,
    CONCAT('Phone: ', SUBSTR(phone_number, 1, 3), ' - ', SUBSTR(phone_number, 4, 3), '-', SUBSTR(phone_number, 7)) AS formatted_phone
FROM users;

--#FROM

--#Multiple Joins with Aliases and Subquery in Join Condition:

SELECT a.name, b.product_id, c.description
FROM customers AS a
JOIN orders AS b ON a.customer_id = b.customer_id
JOIN products AS c ON b.product_id = c.product_id AND c.stock > (SELECT MIN(stock) FROM products)
WHERE a.region = 'North America';

--#Left Join with Function in the ON Clause:

SELECT e.employee_name, d.department_name
FROM employees AS e
LEFT JOIN departments AS d ON e.department_id = d.department_id AND YEAR(e.hire_date) = 2020
ORDER BY d.department_name;

--#Doesn't handle Nested Functions

--#UNNEST

--#UNNEST with aggregate function and GROUP BY:

SELECT t1.id, COUNT(unnested_items) AS num_items
FROM table1 t1
LEFT JOIN unnest(array[(1, 'apple'), (2, 'banana')]) AS unnested_items ON true
GROUP BY t1.id;

--#Multiple Joins


SELECT * FROM table1
CROSS JOIN UNNEST(ARRAY[(1, 'apple'), (2, 'banana')]) AS fruits
LEFT JOIN UNNEST(ARRAY[(3, 'carrot'), (4, 'date')]) AS vegetables
WHERE fruits.item1 > 0;

--#UNNEST with multiple conditions and CASE statements:

SELECT t1.id,
       CASE 
           WHEN unnested_items.item_name = 'apple' THEN 'Fruit'
           WHEN unnested_items.item_name = 'banana' THEN 'Fruit'
           ELSE 'Other'
       END AS category
FROM table1 t1
LEFT JOIN unnest(array[(1, 'apple'), (2, 'banana'), (3, 'carrot'), (4, 'date')]) AS unnested_items ON true;

--#UNNEST with window function and PARTITION BY:

SELECT t1.id,
       unnested_items.item_name,
       COUNT(*) OVER (PARTITION BY unnested_items.item_name) AS num_occurrences
FROM table1 t1
LEFT JOIN unnest(array[(1, 'apple'), (2, 'banana'), (3, 'apple'), (4, 'banana')]) AS unnested_items ON true;
