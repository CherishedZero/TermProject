DROP SCHEMA IF EXISTS store;

CREATE DATABASE IF NOT EXISTS store;

USE store;

CREATE TABLE IF NOT EXISTS vendors (
vendor_id INT PRIMARY KEY AUTO_INCREMENT,
vendor_name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
prod_id INT PRIMARY KEY AUTO_INCREMENT,
prod_name VARCHAR(50) NOT NULL,
genre VARCHAR(20) NOT NULL,
developer VARCHAR(100) NOT NULL,
release_date DATE NOT NULL,
price DECIMAL(9,2) NOT NULL,
inventory INT NOT NULL,
vendor_id INT NOT NULL,
CONSTRAINT `vendors_fk_products` FOREIGN KEY (`vendor_id`) REFERENCES `store`.`vendors` (`vendor_id`)
);

CREATE TABLE IF NOT EXISTS customers (
customer_id INT PRIMARY KEY AUTO_INCREMENT,
first_name VARCHAR(50) NOT NULL,
last_name VARCHAR(50) NOT NULL,
email VARCHAR(50) NOT NULL UNIQUE,
address VARCHAR(100),
phone VARCHAR(15) NOT NULL
);

CREATE TABLE IF NOT EXISTS invoices (
invoice_id INT PRIMARY KEY AUTO_INCREMENT,
customer_id INT NOT NULL,
time_of_sale DATETIME NOT NULL DEFAULT NOW(),
CONSTRAINT `customers_fk_invoices` FOREIGN KEY (`customer_id`) REFERENCES `store`.`customers` (`customer_id`)
);

CREATE TABLE IF NOT EXISTS invoice_products (
invoice_id INT NOT NULL,
prod_id INT NOT NULL,
quantity INT NOT NULL,
PRIMARY KEY (`invoice_id`, `prod_id`),
CONSTRAINT `invoices_fk_invoice_products` FOREIGN KEY (`invoice_id`) REFERENCES `store`.`invoices` (`invoice_id`),
CONSTRAINT `products_fk_invoice_products` FOREIGN KEY (`prod_id`) REFERENCES `store`.`products` (`prod_id`)
);

-- Sample Customers
INSERT INTO customers (first_name, last_name, email, address, phone)
VALUES ('James', 'Tucker', 'jt@notstore.com', '42 Wallaby Way Sidney', '867-5309');
INSERT INTO customers (first_name, last_name, email, address, phone)
VALUES ('Mary', 'Gable', 'mgable@notstore.com', '9 Highway Drive', '111-1111');
INSERT INTO customers (first_name, last_name, email, address, phone)
VALUES ('Tim', 'Lawrence', 'timothylawrence@notastore.com', NULL, '420-6969');
INSERT INTO customers (first_name, last_name, email, address, phone)
VALUES ('Lily', 'Currie', 'lily.currie92@notthestore.com', '23 Apple Blossom Lane', '555-5555');
INSERT INTO customers (first_name, last_name, email, phone)
VALUES ('Jeff', 'Currie', 'jeff.currie91@notthestore.com', '555-5555');

-- Sample Vendors
INSERT INTO vendors (vendor_name)
VALUES ('Bethesda Softworks');
INSERT INTO vendors (vendor_name)
VALUES ('Bandai Namco Entertainment');
INSERT INTO vendors (vendor_name)
VALUES ('Electronic Arts');
INSERT INTO vendors (vendor_name)
VALUES ('SEGA');

-- Sample Products
INSERT INTO products (prod_name, genre, developer, release_date, price, inventory, vendor_id)
VALUES ('The Elder Scrolls V: Skyrim', 'RPG', 'Bethesda Game Studios', '2011-11-11', 59.99, 200, 1);
INSERT INTO products (prod_name, genre, developer, release_date, price, inventory, vendor_id)
VALUES ('The Elder Scrolls IV: Oblivion', 'RPG', 'Bethesda Game Studios', '2007-09-11', 59.99, 150, 1);
INSERT INTO products (prod_name, genre, developer, release_date, price, inventory, vendor_id)
VALUES ('Elden Ring', 'RPG', 'FromSoftware Inc', '2022-02-24', 59.99, 100, 2);
INSERT INTO products (prod_name, genre, developer, release_date, price, inventory, vendor_id)
VALUES ('Digimon World: Next Order', 'JRPG', 'HYDE, Inc', '2023-02-21', 59.99, 50, 2);
INSERT INTO products (prod_name, genre, developer, release_date, price, inventory, vendor_id)
VALUES ('Need For Speed: Unbound', 'Racing', 'Criterion Games', '2022-12-02', 69.99, 24, 3);
INSERT INTO products (prod_name, genre, developer, release_date, price, inventory, vendor_id)
VALUES ('Yakuza: Like a Dragon', 'Action', 'Ryu Ga Gotoku Studio', '2020-11-10', 59.99, 49, 4);

-- Sample Invoices
INSERT INTO invoices (customer_id, time_of_sale)
VALUES (1, '2023-03-27 18:30:24');
INSERT INTO invoices (customer_id, time_of_sale)
VALUES (2, Now());
INSERT INTO invoices (customer_id, time_of_sale)
VALUES (3, Now());
INSERT INTO invoices (customer_id, time_of_sale)
VALUES (4, Now());
INSERT INTO invoices (customer_id, time_of_sale)
VALUES (1, Now());

-- Sample Invoice Products
INSERT INTO invoice_products (invoice_id, prod_id, quantity)
VALUES (1, 1, 2);
INSERT INTO invoice_products (invoice_id, prod_id, quantity)
VALUES (1, 2, 1);
INSERT INTO invoice_products (invoice_id, prod_id, quantity)
VALUES (1, 3, 2);
INSERT INTO invoice_products (invoice_id, prod_id, quantity)
VALUES (2, 4, 6);
INSERT INTO invoice_products (invoice_id, prod_id, quantity)
VALUES (3, 5, 1);
INSERT INTO invoice_products (invoice_id, prod_id, quantity)
VALUES (3, 6, 1);
INSERT INTO invoice_products (invoice_id, prod_id, quantity)
VALUES (4, 1, 1);
INSERT INTO invoice_products (invoice_id, prod_id, quantity)
VALUES (4, 2, 1);
INSERT INTO invoice_products (invoice_id, prod_id, quantity)
VALUES (5, 5, 1);


SELECT * FROM customers;
SELECT * FROM vendors;
SELECT * FROM products;
SELECT * FROM invoices;
SELECT * FROM invoice_products;

SELECT i.invoice_id AS 'Invoice Number', SUM(p.price*ip.quantity) AS 'Invoice Total' FROM products AS p JOIN invoice_products AS ip USING(prod_id) JOIN invoices AS i USING(invoice_id) GROUP BY i.invoice_id;