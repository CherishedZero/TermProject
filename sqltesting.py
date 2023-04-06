from testingmysql_func import *

def getCustomerNames():
    sql = f"SELECT customer_id, CONCAT(first_name, ' ', last_name), email FROM customers;"
    rows = executeQueryAndReturnResult(sql)[1]
    return rows

def getProductNames():
    sql = f"SELECT prod_name FROM store.products;"
    rows = executeQueryAndReturnResult(sql)[1]
    names = [row[0] for row in rows]
    return names

def getGameInfoByName(name):
    sql = f"SELECT prod_name, price FROM store.products WHERE prod_name = '{name}';"
    try:
        result_set = executeQueryAndReturnResult(sql)[1]
        if result_set is None or len(result_set) == 0:
            return None
        gameInfo = result_set[0]
        data = {'prod_name': gameInfo[0], 'price': float(gameInfo[1])}
        return ['Game', 'Price($)'], data
    except Exception as e:
        print(e)
        return None

def getCustByName(name):
    sql = f"SELECT email, customer_id FROM store.customers WHERE '{name}' = CONCAT(first_name, ' ', last_name);"
    try:
        result_set = executeQueryAndReturnResult(sql)[1]
        if result_set is None or len(result_set) == 0:
            return None
        custInfo = result_set[0]
        data = {'email': custInfo[0], 'customer_id': custInfo[1]}
    except Exception as e:
        print(e)
    else:
        return data

def addCustomer(fname, lname, email, address, phone):
    sql = f"INSERT INTO store.customers (first_name, last_name, email, address, phone) VALUES('{fname}','{lname}','{email}','{address}','{phone}');"
    print(sql)
    return executeQueryAndCommit(sql)

def getCustomer():
    sql = f"SELECT CONCAT(first_name, ' ', last_name), customer_id, email, address, phone, first_name, last_name FROM customers;"
    rows = executeQueryAndReturnResult(sql)[1]
    return rows

def getCustById(id):
    sql = f"SELECT first_name, last_name, address, phone FROM store.customers;"
    try:
        result_set = executeQueryAndReturnResult(sql)[1]
        if result_set is None or len(result_set) == 0:
            return None
        custInfo = result_set[0]
        data = {'fname': custInfo[0], 'lname': custInfo[1], 'address': custInfo[2], 'phone': custInfo[3]}
    except Exception as e:
        print(e)
    else:
        return data

def updateCustomerInfo(id, email, address, phone, fname, lname):
    sql = f"UPDATE store.customers SET email = '{email}', address = '{address}', phone = '{phone}', first_name = '{fname}', last_name = '{lname}' WHERE customer_id = {id};"
    return executeQueryAndCommit(sql)