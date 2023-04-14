from SQLConnector import *

# add new customer

def addCustomer(first_name, last_name, email, address, phone):
    sql_query = f"CALL store.add_customer_with_address('{first_name}', '{last_name}', '{email}', '{address}', '{phone}');"
    execute_and_commit(sql_query)


# get customer names

def getCustomerNames():
    sql_query = f"SELECT concat(first_name, ' ', last_name) FROM store.customers;"
    rows = execute_and_return(sql_query)[1]
    cust_names = [row[0] for row in rows]
    return cust_names


# get customer info from name

def getCustByName(cust_name):
    sql_query = f"SELECT email, customer_id FROM store.customers WHERE '{cust_name}' = concat(first_name, ' ', last_name);"
    try:
        x = execute_and_return(sql_query)[1]
        if x is None or len(x) == 0:
            return None
        customer_info = x[0]
        info = {'email': customer_info[0], 'customer_id': customer_info[1]}
    except Exception as y:
        print(y)
    else:
        return info


# get customer info from id

def getCustById(id):
    sql_query = f"CALL `store`.`customer_full_info_by_id`([{id});"
    try:
        x = execute_and_return(sql_query)[1]
        if x is None or len(x) == 0:
            return None
        customer_info = x[0]
        info = {'fname': customer_info[0], 'lname': customer_info[1], 'address': customer_info[2], 'phone': customer_info[3]}
    except Exception as y:
        print(y)
    else:
        return info


# update customer info

def updateCustomerInfo(id, email, address, phone, first_name, last_name):
    sql_query = f"CALL `store`.`update_customer_address_true`({id},'{first_name}','{last_name}','{email}','{address}','{phone}');"
    execute_and_commit(sql_query)


# update customer info where address in NULL

def updateCustomerInfoBlankAddress(id, email, phone, first_name, last_name):
    sql_query = f"CALL `store`.`update_customer_address_false`({id},'{first_name}','{last_name}','{email}','{phone}');"
    execute_and_commit(sql_query)


# add customer where address is NULL

def addCustomerNoAddress(first_name, last_name, email, phone):
    sql_query = f"CALL store.add_customer_without_address('{first_name}','{last_name}','{email}','{phone}');"
    execute_and_commit(sql_query)


# get customers table with first and last name

def getCustomer():
    sql_query = f"SELECT customer_id, concat(first_name, ' ', last_name), email, address, phone, first_name, last_name FROM customers;"
    table = execute_and_return(sql_query)[1]
    return table


# add new product

def addProduct(prod_name, genre, dev, date, price, vendor, inventory=0):
    sql_query = f"CALL store.add_product('{prod_name}', '{genre}', '{dev}', '{date}', {price}, {inventory}, {vendor})"
    return execute_and_commit(sql_query)


# get product name from products table

def getProductNames():
    sql_query = f"SELECT prod_name FROM store.products;"
    rows = execute_and_return(sql_query)[1]
    names = [row[0] for row in rows]
    return names


# get game info from game name

def getGameInfoByName(game_name):
    sql_query = f"SELECT prod_id, prod_name, price FROM store.products WHERE prod_name = '{game_name}';"
    try:
        x = execute_and_return(sql_query)[1]
        if x is None or len(x) == 0:
            return None
        game_info = x[0]
        info = {'prod_id': game_info[0], 'prod_name': game_info[1], 'price': float(game_info[2])}
        return ['ID', 'Game', 'Price($)', 'Quantity'], info
    except Exception as y:
        print(y)
        return None


# gets products

def getProducts():
    sql_query = f"CALL store.product_list();"
    table = execute_and_return(sql_query)[1]
    return table


# adds new Vendor

def addVendor(vendor_name):
    sql_query = f"CALL store.add_vendor('{vendor_name}');"
    execute_and_commit(sql_query)


# gets vendors table

def getVendors():
    sql_query = f"SELECT vendor_id, vendor_name FROM vendors;"
    table = execute_and_return(sql_query)[1]
    return table


def createInvoice(custId, prodId, quantity):
    sql1 = f"CALL store.create_invoice({custId});"
    execute_and_commit(sql1)
    sql2 = f"SELECT MAX(invoice_id) FROM store.invoices;"
    rows = list(execute_and_return(sql2))
    invoice_id = rows[1][0]
    sql3 = f"CALL store.add_invoice_product({invoice_id[0]}, {prodId}, {quantity});"
    execute_and_commit(sql3)
    sql4 = f"UPDATE store.products SET inventory = inventory - {quantity} WHERE prod_id = {prodId};"
    execute_and_commit(sql4)


def updateVendor(vendor_id, vendor_name):
    sql_query = f"CALL store.update_vendor({vendor_id}, '{vendor_name}');"
    execute_and_commit(sql_query)


def updateProduct(prod_id, name, genre, dev, date, price, vendor, stock=100):
    sql_query = f"CALL store.update_product({prod_id}, '{name}', '{genre}', '{dev}', '{date}', {price}, {stock}, {vendor})"
    execute_and_commit(sql_query)

