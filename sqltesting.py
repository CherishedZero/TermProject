from SQLConnector import *

def getCustomerNames():
    sql = f"CALL store.customer_info_invoice;"
    rows = ExecuteAndReturn(sql)[1]
    return rows

# Phase out following 2 functions
def getGameInfoByName(name):
    sql = f"SELECT prod_id, prod_name, price FROM store.products WHERE prod_name = '{name}';"
    try:
        result_set = ExecuteAndReturn(sql)[1]
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
        result_set = ExecuteAndReturn(sql)[1]
        if result_set is None or len(result_set) == 0:
            return None
        custInfo = result_set[0]
        data = {'email': custInfo[0], 'customer_id': custInfo[1]}
    except Exception as e:
        print(e)
    else:
        return data

def addCustomer(fname, lname, email, address, phone):
    sql = f"CALL store.add_customer_with_address('{fname}','{lname}','{email}','{address}','{phone}');"
    ExecuteAndCommit(sql)

def addCustomerNoAddress(fname, lname, email, phone):
    sql = f"CALL store.add_customer_without_address('{fname}','{lname}','{email}','{phone}');"
    ExecuteAndCommit(sql)

def getCustomer():
    sql = f"CALL store.customer_full_info;"
    rows = ExecuteAndReturn(sql)[1]
    return rows

def getCustById(id):
    sql = f"CALL store.customer_full_info_by_id([{id});"
    try:
        result_set = ExecuteAndReturn(sql)[1]
        if result_set is None or len(result_set) == 0:
            return None
        custInfo = result_set[0]
        data = {'fname': custInfo[0], 'lname': custInfo[1], 'address': custInfo[2], 'phone': custInfo[3]}
    except Exception as e:
        print(e)
    else:
        return data

def updateCustomerInfo(id, email, address, phone, fname, lname):
    sql = f"CALL store.update_customer_address_true({id},'{fname}','{lname}','{email}','{address}','{phone}');"
    ExecuteAndCommit(sql)

def updateCustomerInfoBlankAddress(id, email, phone, fname, lname):
    sql = f"CALL store.update_customer_address_false({id},'{fname}','{lname}','{email}','{phone}');"
    ExecuteAndCommit(sql)


# Following function needs a rewrite
def createInvoice(custId, prodId, quantity):
    sql1 = f"CALL store.create_invoice({custId});"
    ExecuteAndCommit(sql1)
    sql2 = f"SELECT MAX(invoice_id) FROM `store`.`invoices`;"
    rows = list(ExecuteAndReturn(sql2))
    invoice_id = rows[1][0]
    sql3 = f"CALL `store`.`add_invoice_product`({invoice_id[0]}, {prodId}, {quantity});"
    ExecuteAndCommit(sql3)
    sql4 = f"UPDATE `store`.`products` SET inventory = inventory - {quantity} WHERE prod_id = {prodId};"
    ExecuteAndCommit(sql4)

def checkStock(prodId, purQuantity):
    sql = f"CALL store.current_stock_by_id({prodId})"
    curStock = ExecuteAndReturn(sql)
    if purQuantity > curStock:
        return False
    return True

def addProduct(prod_name, genre, dev, release, price, vendor_id):
    sql = f"CALL store.add_product('{prod_name}', '{genre}', '{dev}', '{release}', {price}, 0, {vendor_id});"
    ExecuteAndCommit(sql)

def addVendor(name):
    sql = f"CALL store.add_vendor('{name}');"
    ExecuteAndCommit(sql)

def getAllInventory():
    sql = f"CALL store.product_list;"
    return ExecuteAndReturn(sql)


def outOfStock():
    sql = f"CALL store.out_of_stock;"
    return ExecuteAndReturn(sql)

def getAllVendors():
    sql = f"CALL store.vendor_list;"
    return ExecuteAndReturn(sql)[1]

def getAllVendorsForTable():
    sql = f"CALL store.vendor_list;"
    return ExecuteAndReturn(sql)

def updateVendor(id, name):
    sql = f"CALL store.update_vendor({id},'{name}');"
    ExecuteAndCommit(sql)


def getAllCustomers():
    sql = f"CALL store.customer_list;"
    return ExecuteAndReturn(sql)

def getRecentCustomers():
    sql = f"CALL store.recent_customers;"
    return ExecuteAndReturn(sql)

def getProducts():
    sql = f"CALL store.prod_full_info;"
    return ExecuteAndReturn(sql)[1]

def updateVendor(vendor_id, vendor_name):
    sql_query = f"CALL store.update_vendor({vendor_id}, '{vendor_name}');"
    ExecuteAndCommit(sql_query)

def adjustStock(product_id, quantity):
    sql_query = f"CALL store.adjust_stock({product_id}, '{quantity}');"
    ExecuteAndCommit(sql_query)


def updateProduct(prod_id, name, genre, dev, date, price, stock, vendor):
    sql_query = f'CALL store.update_product({prod_id}, "{name}", "{genre}", "{dev}", "{date}", {price}, {stock}, {vendor})'
    ExecuteAndCommit(sql_query)
