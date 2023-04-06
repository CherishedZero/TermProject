use store;

CALL customer_list;
CALL vendor_list;
CALL product_list;
CALL out_of_stock;
CALL customer_full_info_by_id(2);
CALL customer_info_invoice_by_id(1);
CALL prod_invoice_by_id(4);
CALL prod_full_info_by_id(3);
CALL vendor_by_id(3);
CALL add_customer_with_address('Lisa', 'Franks', 'lfranks@thisisntmystore.com', '123 def st', '420-6996');
CALL add_customer_without_address('Nino', 'Tocker', 'ntocker88@whyamihere.net', '134-8765');
CALL add_vendor('Annapurnas Interactive');
CALL add_product('Striy', 'Adventure', 'BlurTwelve Studios', '2022-06-19', 29.95, 5, 2);
CALL create_invoice(7);
CALL add_invoice_product(6, 7, 2);

SELECT * FROM customers;
SELECT * FROM vendors;
SELECT * FROM products;
SELECT * FROM invoices;
SELECT * FROM invoice_products;
CALL out_of_stock;
CALL recent_customers;

CALL update_customer_address_true(6, 'Lisa', 'Franks', 'lfranks@thisisntmystore.com', '123 abc st', '420-6996');
CALL update_customer_address_false(7, 'Nina', 'Tucker', 'ntucker88@whyamihere.net', '234-8765');
CALL update_vendor(5, 'Annapurna Interactive');
CALL update_product(7, 'Stray', 'Adventure', 'BlueTwelve Studios', '2022-07-19', 29.99, 0, 5);
CALL adjust_stock(1, -100);
CALL adjust_stock(2, 25);
CALL update_invoice_products(6, 7, 5);

SELECT * FROM customers;
SELECT * FROM vendors;
SELECT * FROM products;
SELECT * FROM invoices;
SELECT * FROM invoice_products;
CALL out_of_stock;