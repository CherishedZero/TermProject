from sqlConnector import *

def getCustomerNames():
    """
        Contains an sql statement that calls a stored procedure that will be passed to the execute and return function and returns a list of tuples containing each row
    """
    sql = f"CALL store.customer_info_invoice;"
    rows = ExecuteAndReturn(sql)[1]
    return rows


def addCustomer(fname, lname, email, address, phone):
    """
        Contains an sql statement that calls a stored procedure that will be passed to the execute and commit function
    """
    sql = f"CALL store.add_customer_with_address('{fname}','{lname}','{email}','{address}','{phone}');"
    ExecuteAndCommit(sql)


def addCustomerNoAddress(fname, lname, email, phone):
    """
        Contains an sql statement that calls a stored procedure that will be passed to the execute and commit function
    """
    sql = f"CALL store.add_customer_without_address('{fname}','{lname}','{email}','{phone}');"
    ExecuteAndCommit(sql)


def getCustomer():
    """
        Contains an sql statement that calls a stored procedure that wll be passed to the execute and return function and returns a list of tuples containing each row
    """
    sql = f"CALL store.customer_full_info;"
    rows = ExecuteAndReturn(sql)[1]
    return rows


def getCustById(id):
    """
        Retrieve the full information for a customer with the given id.

        Parameters:
        id (int): The id of the customer to retrieve.

        Returns:
        dict: A dictionary containing the customer's first name, last name, address, and phone number. Returns None if no customer is found with the given id.
    """
    sql = f"CALL store.customer_full_info_by_id({id});"
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
    """
        Contains an sql statement that calls a stored procedure that will be passed to the execute and return function and returns True or False based on the result of the query
    """
    sql = f"Call store.customer_has_address_by_id({custID})"
    return bool(ExecuteAndReturn(sql)[1])


def updateCustomerInfo(id, email, address, phone, fname, lname):
    """
        Contains an sql statement that calls a stored procedure that will be passed to the execute and commit function
    """
    sql = f"CALL store.update_customer_address_true({id},'{fname}','{lname}','{email}','{address}','{phone}');"
    ExecuteAndCommit(sql)


def updateCustomerInfoRemoveAddress(id, email, phone, fname, lname):
    """
        Contains an sql statement that calls a stored procedure that will be passed to the execute and commit function
    """
    sql = f"CALL store.update_customer_address_true({id},'{fname}','{lname}','{email}', NULL,'{phone}');"
    ExecuteAndCommit(sql)


def updateCustomerInfoBlankAddress(id, email, phone, fname, lname):
    """
        Contains an sql statement that calls a stored procedure that will be passed to the execute and commit function
    """
    sql = f"CALL store.update_customer_address_false({id},'{fname}','{lname}','{email}','{phone}');"
    ExecuteAndCommit(sql)


def createInvoice(cust_id, invoice):
    """
        Create a new invoice for a customer and add the products listed in the invoice. First adding the customer invoice
        to the invoice table using create_invoice

        Parameters:
        cust_id (int): The id of the customer to create the invoice for.
        invoice (dict): A dictionary containing the product ids and quantities to add to the invoice.

        Returns:
        None
    """
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
    """
        Contains an sql statement that calls a stored procedure that will be passed to the execute and return function and returns a list of tuples containing each row
    """
    sql = f"CALL `store`.`current_stock_by_id`({prodId})"
    info = ExecuteAndReturn(sql)
    return(info[1])


def addProduct(prod_name, genre, dev, release, price, quantity, vendor_id):
    """
        Contains an sql statement that calls a stored procedure that will be passed to the execute and commit function
    """
    sql = f"CALL store.add_product('{prod_name}', '{genre}', '{dev}', '{release}', {price}, {quantity}, {vendor_id});"
    ExecuteAndCommit(sql)


def addVendor(name):
    """
        Contains an sql statement that calls a stored procedure that will be passed to the execute and commit function
    """
    sql = f"CALL store.add_vendor('{name}');"
    ExecuteAndCommit(sql)


def getAllInventory():
    """
        Contains an sql statement that calls a stored procedure that will be passed to the execute and return function
    """
    sql = f"CALL store.product_list;"
    return ExecuteAndReturn(sql)


def outOfStock():
    """
        Contains an sql statement that calls a stored procedure that will be passed to the execute and return function
    """
    sql = f"CALL store.out_of_stock;"
    return ExecuteAndReturn(sql)


def getAllVendors():
    """
        Contains an sql statement that calls a stored procedure that will be passed to the execute and return function and returns a list of tuples containing each row
    """
    sql = f"CALL store.vendor_list;"
    return ExecuteAndReturn(sql)[1]


def getAllVendorsForTable():
    """
        Contains an sql statement that calls a stored procedure that will be passed to the execute and return function
    """
    sql = f"CALL store.vendor_list;"
    return ExecuteAndReturn(sql)


def updateVendor(id, name):
    """
        Contains an sql statement that calls a stored procedure that will be passed to the execute and commit function
    """
    sql = f"CALL store.update_vendor({id},'{name}');"
    ExecuteAndCommit(sql)


def getAllCustomers():
    """
        Contains an sql statement that calls a stored procedure that will be passed to the execute and return function
    """
    sql = f"CALL store.customer_list;"
    return ExecuteAndReturn(sql)


def getRecentCustomers():
    """
        Contains an sql statement that calls a stored procedure that will be passed to the execute and return function
    """
    sql = f"CALL store.recent_customers;"
    return ExecuteAndReturn(sql)


def getProducts():
    """
        Contains an sql statement that calls a stored procedure that will be passed to the execute and return function and returns a list of tuples containing each row
    """
    sql = f"CALL `store`.`prod_full_info`();"
    return ExecuteAndReturn(sql)[1]


def updateProduct(prod_id, name, genre, dev, date, price, stock, vendor):
    """
        Contains an sql statement that calls a stored procedure that will be passed to the execute and commit function
    """
    sql_query = f"CALL store.update_product({prod_id}, '{name}', '{genre}', '{dev}', '{date}', {price}, {stock}, {vendor})"
    ExecuteAndCommit(sql_query)


def adjustStock(product_id, quantity):
    """
        Contains an sql statement that calls a stored procedure that will be passed to the execute and commit function
    """
    sql_query = f"CALL store.adjust_stock({product_id}, '{quantity}');"
    ExecuteAndCommit(sql_query)


def vendorById(id):
    """
        Retrieve the name of the vendor associated with the given id.

        Parameters:
        id (int): The id of the vendor to retrieve.

        Returns:
        str: The name of the vendor.
    """
    sql = f"CALL store.vendor_by_id({id});"
    return ExecuteAndReturn(sql)[1][0][1]
