use store;

CALL customer_list();
CALL vendor_list();
CALL product_list();
CALL out_of_stock();
CALL customer_full_info_by_id(2);
CALL customer_info_invoice_by_id(1);
CALL prod_invoice_by_id(4);
CALL prod_full_info_by_id(3);
CALL vendor_by_id(3);
CALL add_customer_with_address('Lisa', 'Franks', 'lfranks@thisisntmystore.com', '123 abc st', '420-6996');
CALL add_customer_without_address('Nina', 'Tucker', 'NTucker88@whyamihere.net', '234-8765');
CALL add_vendor('Annapurna Interactive');
CALL add_product('Stray', 'Adventure', 'BlueTwelve Studios', '2022-07-19', 29.99, 0, 5);
CALL create_invoice(2);
CALL add_invoice_product(6, 7, 5);

SELECT * FROM customers;
SELECT * FROM vendors;
SELECT * FROM products;
SELECT * FROM invoices;
SELECT * FROM invoice_products;