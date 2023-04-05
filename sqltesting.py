from testingmysql_func import *

def getCustomerNames():
    sql = f"SELECT CONCAT(first_name, ' ', last_name) FROM store.customers;"
    rows = executeQueryAndReturnResult(sql)[1]
    names = [row[0] for row in rows]
    return names

def getProductNames():
    sql = f"SELECT prod_name FROM store.products;"
    rows = executeQueryAndReturnResult(sql)[1]
    names = [row[0] for row in rows]
    return names

def getGameInfoByName(name):
    sql = f"SELECT"

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