from sqlConnector import *

def getCustomerNames():
    sql = f"CALL store.customer_info_invoice;"
    rows = ExecuteAndReturn(sql)[1]
    return rows

def getProducts():
    sql = f"CALL `store`.`product_list`();"
    rows = ExecuteAndReturn(sql)[1]
    names = [row[0:2]+row[5:6] for row in rows]
    return names

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

def customerHasAddress(custID):
    sql = f"Call store.customer_has_address_by_id({custID})"
    return bool(ExecuteAndReturn(sql)[1])

def updateCustomerInfo(id, email, address, phone, fname, lname):
    sql = f"CALL store.update_customer_address_true({id},'{fname}','{lname}','{email}','{address}','{phone}');"
    ExecuteAndCommit(sql)

def updateCustomerInfoRemoveAddress(id, email, phone, fname, lname):
    sql = f"CALL store.update_customer_address_true({id},'{fname}','{lname}','{email}', NULL,'{phone}');"
    ExecuteAndCommit(sql)

def updateCustomerInfoBlankAddress(id, email, phone, fname, lname):
    sql = f"CALL store.update_customer_address_false({id},'{fname}','{lname}','{email}','{phone}');"
    ExecuteAndCommit(sql)


def createInvoice(cust_id, invoice):
    sql1 = f"CALL `store`.`create_invoice`({cust_id});"
    ExecuteAndCommit(sql1)
    sql2 = f"CALL `store`.`latest_invoice`;"
    rows = list(ExecuteAndReturn(sql2))
    invoice_id = rows[1][0]
    for key, value in invoice.items():
        sql3 = f"CALL `store`.`add_invoice_product`({invoice_id[0]}, {key}, {value[1]});"
        ExecuteAndCommit(sql3)
        sql4 = f"CALL `store`.`adjust_stock`({key}, -{value[1]});"
        ExecuteAndCommit(sql4)

def checkStock(prodId):
    sql = f"CALL `store`.`current_stock_by_id`({prodId})"
    info = ExecuteAndReturn(sql)
    return(info[1])

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
    sql = f"CALL `store`.`prod_full_info`();"
    return ExecuteAndReturn(sql)[1]

def updateProduct(prod_id, name, genre, dev, date, price, stock, vendor):
    sql_query = f"CALL store.update_product({prod_id}, '{name}', '{genre}', '{dev}', '{date}', {price}, {stock}, {vendor})"
    ExecuteAndCommit(sql_query)

def updateVendor(vendor_id, vendor_name):
    sql_query = f"CALL store.update_vendor({vendor_id}, '{vendor_name}');"
    ExecuteAndCommit(sql_query)

def adjustStock(product_id, quantity):
    sql_query = f"CALL store.adjust_stock({product_id}, '{quantity}');"
    ExecuteAndCommit(sql_query)


def updateProduct(prod_id, name, genre, dev, date, price, stock, vendor):
    sql_query = f'CALL store.update_product({prod_id}, "{name}", "{genre}", "{dev}", "{date}", {price}, {stock}, {vendor})'
    ExecuteAndCommit(sql_query)
