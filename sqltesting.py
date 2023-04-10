from testingmysql_func import *

def getCustomerNames():
    sql = f"SELECT customer_id, CONCAT(first_name, ' ', last_name), email FROM customers;"
    rows = executeQueryAndReturnResult(sql)[1]
    return rows

def getProducts():
    sql = f"CALL `store`.`product_list`();"
    rows = executeQueryAndReturnResult(sql)[1]
    names = [row[0:2]+row[5:6] for row in rows]
    return names

def getGameInfoByName(name):
    sql = f"SELECT prod_id, prod_name, price FROM store.products WHERE prod_name = '{name}';"
    try:
        result_set = executeQueryAndReturnResult(sql)[1]
        if result_set is None or len(result_set) == 0:
            return None
        gameInfo = result_set[0]
        data = {'prod_id': gameInfo[0], 'prod_name': gameInfo[1], 'price': float(gameInfo[2])}
        return ['ID', 'Game', 'Quantity', 'Price($)'], data
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
    sql = f"CALL `store`.`add_customer_with_address`('{fname}','{lname}','{email}','{address}','{phone}');"
    executeQueryAndCommit(sql)

def addCustomerNoAddress(fname, lname, email, phone):
    sql = f"CALL `store`.`add_customer_without_address`('{fname}','{lname}','{email}','{phone}');"
    executeQueryAndCommit(sql)

def getCustomer():
    sql = f"SELECT customer_id, CONCAT(first_name, ' ', last_name), email, address, phone, first_name, last_name FROM customers;"
    rows = executeQueryAndReturnResult(sql)[1]
    return rows

def getCustById(id):
    sql = f"CALL `store`.`customer_full_info_by_id`([{id});"
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
    sql = f"CALL `store`.`update_customer_address_true`({id},'{fname}','{lname}','{email}','{address}','{phone}');"
    executeQueryAndCommit(sql)

def updateCustomerInfoBlankAddress(id, email, phone, fname, lname):
    sql = f"CALL `store`.`update_customer_address_false`({id},'{fname}','{lname}','{email}','{phone}');"
    executeQueryAndCommit(sql)