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
VALUES ('Digimon World: Next Order', 'JRPG', 'HYDE, Inc', '2023-02-21', 59.99, 0, 2);
INSERT INTO products (prod_name, genre, developer, release_date, price, inventory, vendor_id)
VALUES ('Need For Speed: Unbound', 'Racing', 'Criterion Games', '2022-12-02', 69.99, 24, 3);
INSERT INTO products (prod_name, genre, developer, release_date, price, inventory, vendor_id)
VALUES ('Yakuza: Like a Dragon', 'Action', 'Ryu Ga Gotoku Studio', '2020-11-10', 59.99, 49, 4);

-- Sample Invoices
INSERT INTO invoices (customer_id, time_of_sale)
VALUES (1, '2023-03-27 18:30:24');
INSERT INTO invoices (customer_id, time_of_sale)
VALUES (2, '2023-02-27 12:46:03');
INSERT INTO invoices (customer_id, time_of_sale)
VALUES (3, '2022-03-27 09:24:56');
INSERT INTO invoices (customer_id, time_of_sale)
VALUES (4, '2023-04-05 11:35:12');
INSERT INTO invoices (customer_id)
VALUES (1);

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

-- Creating Stored Procedures for ComboBoxes
DELIMITER //
CREATE PROCEDURE `prod_invoice` ()
BEGIN
	SELECT prod_id, prod_name, price FROM products;
END
//
DELIMITER //
CREATE PROCEDURE `prod_full_info` ()
BEGIN
	SELECT prod_id, prod_name, genre, developer, release_date, price, inventory, vendor_id FROM products;
END
//
DELIMITER //
CREATE PROCEDURE `vendor_by_id` (IN vend_id INT)
BEGIN
	SELECT vendor_id, vendor_name FROM vendors WHERE vendor_id = vend_id;
END
//
DELIMITER //
CREATE PROCEDURE `customer_info_invoice` ()
BEGIN
	SELECT customer_id, CONCAT(first_name, ' ', last_name), email FROM customers;
END
//
DELIMITER //
CREATE PROCEDURE `customer_full_info` ()
BEGIN
	SELECT customer_id, CONCAT(first_name, ' ', last_name), first_name, last_name, email, address, phone FROM customers;
END
//

-- Creating Stored Procedures for Views
DELIMITER //
CREATE PROCEDURE `customer_list` ()
BEGIN
	SELECT customer_id AS 'ID', CONCAT(first_name, ' ', last_name) AS 'Name', email as 'Email', address AS 'Home Address', phone AS 'Phone Number' FROM customers;
END
//
DELIMITER //
CREATE PROCEDURE `recent_customers` ()
BEGIN
	SELECT DISTINCT c.customer_id AS 'ID', CONCAT(c.first_name, ' ', c.last_name) AS 'Name', c.email as 'Email', c.address AS 'Home Address', c.phone AS 'Phone Number' FROM customers AS c JOIN invoices AS i USING(customer_id) WHERE i.time_of_sale >= DATE_ADD(NOW(), INTERVAL -1 MONTH) ORDER BY c.customer_id;
END
//
DELIMITER //
CREATE PROCEDURE `vendor_list` ()
BEGIN
	SELECT vendor_id AS 'ID', vendor_name AS 'Vendor' FROM vendors;
END
//
DELIMITER //
CREATE PROCEDURE `product_list` ()
BEGIN
	SELECT p.prod_id AS 'ID', p.prod_name AS 'Product Name', p.genre AS 'Genre', p.developer AS 'Developer', p.release_date AS 'Date of Release', p.price AS 'Price', p.inventory AS 'Stock', v.vendor_name AS 'Publisher' FROM products AS p JOIN vendors AS v USING(vendor_id);
END
//
DELIMITER //
CREATE PROCEDURE `out_of_stock` ()
BEGIN
	SELECT p.prod_id AS 'ID', p.prod_name AS 'Product Name', p.genre AS 'Genre', p.developer AS 'Developer', p.release_date AS 'Date of Release', p.price AS 'Price', p.inventory AS 'Stock', v.vendor_name AS 'Publisher' FROM products AS p JOIN vendors AS v USING(vendor_id) WHERE inventory = 0;
END
//

-- Creating Stored Procedures for Inserting to Tables
DELIMITER //
CREATE PROCEDURE `add_customer_with_address` (IN fname VARCHAR(50), IN lname VARCHAR(50), IN email_address VARCHAR(50), IN home_address VARCHAR(100), IN phone_number VARCHAR(50))
BEGIN
	INSERT INTO customers (first_name, last_name, email, address, phone)
    VALUES (fname, lname, email_address, home_address, phone_number);
END
//
DELIMITER //
CREATE PROCEDURE `add_customer_without_address` (IN fname VARCHAR(50), IN lname VARCHAR(50), IN email_address VARCHAR(50), IN phone_number VARCHAR(50))
BEGIN
	INSERT INTO customers (first_name, last_name, email, phone)
    VALUES (fname, lname, email_address, phone_number);
END
//
DELIMITER //
CREATE PROCEDURE `add_vendor` (IN vname VARCHAR(50))
BEGIN
	INSERT INTO vendors (vendor_name)
    VALUES (vname);
END
//
DELIMITER //
CREATE PROCEDURE `create_invoice` (IN cust_id INT)
BEGIN
	INSERT INTO invoices (customer_id)
    VALUES (cust_id);
END
//
DELIMITER //
CREATE PROCEDURE `add_invoice_product` (IN i_id INT, IN p_id INT, IN amount INT)
BEGIN
	INSERT INTO invoice_products (invoice_id, prod_id, quantity)
    VALUES (i_id, p_id, amount);
END
//
DELIMITER //
CREATE PROCEDURE `add_product` (IN product_name VARCHAR(50), pgenre VARCHAR(20), pdeveloper VARCHAR(100), date_of_release DATE, prod_price DECIMAL(9,2), stock INT, publisher_id INT)
BEGIN
	INSERT INTO products (prod_name, genre, developer, release_date, price, inventory, vendor_id)
    VALUES (product_name, pgenre, pdeveloper, date_of_release, prod_price, stock, publisher_id);
END
//


-- Creating Stored Procedures for Updating Tables
DELIMITER //
CREATE PROCEDURE `update_customer_address_false` (IN cust_id INT, IN fname VARCHAR(50), IN lname VARCHAR(50), IN cust_email VARCHAR(50), IN cust_phone VARCHAR(50))
BEGIN
	UPDATE customers
    SET first_name = fname,
		last_name = lname,
        email = cust_email,
		phone = cust_phone
	WHERE customer_id = cust_id;
END
//
DELIMITER //
CREATE PROCEDURE `update_customer_address_true` (IN cust_id INT, IN fname VARCHAR(50), IN lname VARCHAR(50), IN cust_email VARCHAR(50), IN cust_address VARCHAR(100), IN cust_phone VARCHAR(50))
BEGIN
	UPDATE customers
    SET first_name = fname,
		last_name = lname,
        email = cust_email,
        address = cust_address,
		phone = cust_phone
	WHERE customer_id = cust_id;
END
//
DELIMITER //
CREATE PROCEDURE `update_vendor` (IN vend_id INT, IN vname VARCHAR(50))
BEGIN
	UPDATE vendors
    SET vendor_name = vname
	WHERE vendor_id = vend_id;
END
//
DELIMITER //
CREATE PROCEDURE `update_product` (IN product_id INT, IN product_name VARCHAR(50), IN product_genre VARCHAR(20), IN product_developer VARCHAR(100), IN date_of_release DATE, IN product_price DECIMAL(9,2), IN stock INT, IN producer_id INT)
BEGIN
	UPDATE products
    SET prod_name = product_name,
		genre = product_genre,
        developer = product_developer,
        release_date = date_of_release,
        price = product_price,
        inventory = stock,
        vendor_id = producer_id
	WHERE prod_id = product_id;
END
//
DELIMITER //
CREATE PROCEDURE `adjust_stock` (IN product_id INT, IN amount INT)
BEGIN
	DECLARE current_stock INT;
    SELECT inventory INTO current_stock FROM products WHERE prod_id = product_id;
    IF amount < 0 THEN
		SET amount = amount * -1;
		IF amount > current_stock THEN
			SELECT 'Not enough inventory' AS result;
		ELSE
			SET current_stock = current_stock - amount;
			UPDATE products
			SET inventory = current_stock
			WHERE prod_id = product_id;
		END IF;
	ELSE
		SET current_stock = current_stock + amount;
		UPDATE products
		SET inventory = current_stock
		WHERE prod_id = product_id;
	END IF;
END
//
DELIMITER //
CREATE PROCEDURE `update_invoice_products` (IN inv_id INT, IN pro_id INT, IN amount INT)
BEGIN
	UPDATE invoice_products
    SET quantity = amount
	WHERE invoice_id = inv_id AND prod_id = pro_id;
END
//

SELECT * FROM customers;
SELECT * FROM vendors;
SELECT * FROM products;
SELECT * FROM invoices;
SELECT * FROM invoice_products;

SELECT i.invoice_id AS 'Invoice Number', SUM(p.price*ip.quantity) AS 'Invoice Total' FROM products AS p JOIN invoice_products AS ip USING(prod_id) JOIN invoices AS i USING(invoice_id) GROUP BY i.invoice_id;