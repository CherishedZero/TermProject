from SQLConnector import *

def getCustomerNames():
    sql = f"CALL `store`.`customer_info_invoice`();"
    rows = execute_and_return(sql)[1]
    return rows

def getProducts():
    sql = f"CALL `store`.`product_list`();"
    rows = execute_and_return(sql)[1]
    names = [row[0:2]+row[5:6] for row in rows]
    return names

def getGameInfoByName(name):
    sql = f"SELECT prod_id, prod_name, price FROM store.products WHERE prod_name = '{name}';"
    try:
        result_set = execute_and_return(sql)[1]
        if result_set is None or len(result_set) == 0:
            return None
        gameInfo = result_set[0]
        data = {'prod_id': gameInfo[0], 'prod_name': gameInfo[1], 'price': float(gameInfo[2])}
        print(['ID', 'Game', 'Quantity', 'Price($)'], data)
        return ['ID', 'Game', 'Quantity', 'Price($)'], data
    except Exception as e:
        print(e)
        return None

def getCustByName(name):
    sql = f"SELECT email, customer_id FROM store.customers WHERE '{name}' = CONCAT(first_name, ' ', last_name);"
    try:
        result_set = execute_and_return(sql)[1]
        if result_set is None or len(result_set) == 0:
            return None
        custInfo = result_set[0]
        data = {'email': custInfo[0], 'customer_id': custInfo[1]}
    except Exception as e:
        print(e)
    else:
        return data

def addCustomer(fname, lname, email, address, phone):
    sql = f"CALL `store`.`add_customer_with_address`('{fname}','{lname}','{email}','{address}','{phone}');"
    execute_and_commit(sql)

def addCustomerNoAddress(fname, lname, email, phone):
    sql = f"CALL `store`.`add_customer_without_address`('{fname}','{lname}','{email}','{phone}');"
    execute_and_commit(sql)

def getCustomer():
    sql = f"SELECT customer_id, CONCAT(first_name, ' ', last_name), email, address, phone, first_name, last_name FROM customers;"
    rows = execute_and_return(sql)[1]
    return rows

def getCustById(id):
    sql = f"CALL `store`.`customer_full_info_by_id`([{id});"
    try:
        result_set = execute_and_return(sql)[1]
        if result_set is None or len(result_set) == 0:
            return None
        custInfo = result_set[0]
        data = {'fname': custInfo[0], 'lname': custInfo[1], 'address': custInfo[2], 'phone': custInfo[3]}
    except Exception as e:
        print(e)
    else:
        return data

def updateCustomerInfo(id, email, address, phone, fname, lname):
    sql = f"CALL `store`.`update_customer_address_true`({id},'{fname}','{lname}','{email}','{address}','{phone}');"
    execute_and_commit(sql)

def updateCustomerInfoBlankAddress(id, email, phone, fname, lname):
    sql = f"CALL `store`.`update_customer_address_false`({id},'{fname}','{lname}','{email}','{phone}');"
    execute_and_commit(sql)


def createInvoice(custId, prodId, quantity):
    sql1 = f"CALL `store`.`create_invoice`({custId});"
    execute_and_commit(sql1)
    sql2 = f"SELECT MAX(invoice_id) FROM `store`.`invoices`;"
    rows = list(execute_and_return(sql2))
    invoice_id = rows[1][0]
    sql3 = f"CALL `store`.`add_invoice_product`({invoice_id[0]}, {prodId}, {quantity});"
    execute_and_commit(sql3)
    sql4 = f"UPDATE `store`.`products` SET inventory = inventory - {quantity} WHERE prod_id = {prodId};"
    execute_and_commit(sql4)