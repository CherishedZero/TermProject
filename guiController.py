from sqltesting import *
import sys
from random import randint

from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        """
        Initializes the main window of the application and sets up the UI, widgets,git
        as well as initializes data for the information being displayed.
        """
        super().__init__()
        uic.loadUi('videoGameStore.ui', self)
        self.newInvoiceWidgetSetup()
        self.addCustomerWidgetSetup()
        self.editCustomerWidgetSetup()
        self.addProductWidgetSetup()
        self.manageInventoryWidgetSetup()
        self.addVendorWidgetSetup()
        self.editVendorWidgetSetup()
        self.shipmentWidgetSetup()
        self.viewWidgetSetup()
        self.items = {}
        self.table_key = {}

    def newInvoiceWidgetSetup(self):
        self.nameComboBoxNewInvoiceTab = self.findChild(QComboBox, 'nameComboBoxNewInvoiceTab')
        self.emailLineEditNewInvoiceTab = self.findChild(QLineEdit, 'emailLineEditNewInvoiceTab')
        self.idLineEditNewInvoiceTab = self.findChild(QLineEdit, 'idLineEditNewInvoiceTab')
        self.productComboBoxNewInvoiceTab = self.findChild(QComboBox, 'productComboBoxNewInvoiceTab')
        self.productNumberSpinBoxNewInvoiceTab = self.findChild(QSpinBox, 'productNumberSpinBoxNewInvoiceTab')
        self.invoiceTotalLineEditNewInvoiceTab = self.findChild(QLineEdit, 'invoiceTotalLineEditNewInvoiceTab')
        self.invoiceListTableWidgetNewInvoiceTab = self.findChild(QTableWidget, 'invoiceListTableWidgetNewInvoiceTab')
        self.feedbackLabelNewInvoiceTab = self.findChild(QLabel, 'feedbackLabelNewInvoiceTab')
        self.addProductButtonNewInvoiceTab = self.findChild(QPushButton, 'addProductButtonNewInvoiceTab')
        self.addProductButtonNewInvoiceTab.clicked.connect(self.addProductButtonNewInvoiceTabClickHandler)
        self.removeProductButtonNewInvoiceTab = self.findChild(QPushButton, 'removeProductButtonNewInvoiceTab')
        self.removeProductButtonNewInvoiceTab.clicked.connect(self.removeProductButtonNewInvoiceTabClickHandler)
        self.purchaseButtonNewInvoiceTab = self.findChild(QPushButton, 'purchaseButtonNewInvoiceTab')
        self.purchaseButtonNewInvoiceTab.clicked.connect(self.purchaseButtonNewInvoiceTabClickHandler)
        customers = getCustomerNames()
        self.emailLineEditNewInvoiceTab.setText(customers[0][2])
        self.idLineEditNewInvoiceTab.setText(str(customers[0][0]))
        games = getProducts()
        for row in customers:
            self.nameComboBoxNewInvoiceTab.addItem(row[1], userData=[row[0], row[2]])
        self.nameComboBoxNewInvoiceTab.currentIndexChanged.connect(self.nameComboBoxNewInvoiceTabCurrentIndexChangedHandler)
        for game in games:
            self.productComboBoxNewInvoiceTab.addItem(str(game[1]))



    def nameComboBoxNewInvoiceTabCurrentIndexChangedHandler(self):
        try:
            customerId = self.nameComboBoxNewInvoiceTab.currentData()[0]
            customerEmail = self.nameComboBoxNewInvoiceTab.currentData()[1]
            self.emailLineEditNewInvoiceTab.setText(customerEmail)
            self.idLineEditNewInvoiceTab.setText(str(customerId))
        except Exception as e:
            self.feedbackLabelNewInvoiceTab.setText(str(e))

    def addProductButtonNewInvoiceTabClickHandler(self):
        try:
            prodName = self.productComboBoxNewInvoiceTab.currentText()
            colNames, info = getGameInfoByName(prodName)
            self.displayGameInfoInTable(colNames, [info], self.invoiceListTableWidgetNewInvoiceTab)
            self.getTotal()
        except Exception as e:
            self.feedbackLabelNewInvoiceTab.setText(e)

    def displayGameInfoInTable(self, columns, rows, table:QTableWidget):
        try:
            num_rows = table.rowCount()
            table.setColumnCount(len(columns))
            quantity = self.productNumberSpinBoxNewInvoiceTab.value()
            for row in rows:
                keys = list(row.keys())
                values = list(row.values())
                item_key = values[0]
                item_info = {keys[1]: values[1], keys[2]: values[2]}
                self.items = row
                if item_key in self.table_key:
                    self.table_key[item_key]['quantity'] += quantity
                    current_price = self.table_key[item_key]['price']
                    updated_price = round(current_price * self.table_key[item_key]['quantity'], 2)
                    for i in range(num_rows):
                        if table.item(i, 0).text() == str(item_key):
                            row_index = i
                            break
                    current_quantity = int(table.item(row_index, 2).text())
                    new_quantity = quantity + current_quantity
                    table.item(row_index, 2).setText(str(new_quantity))
                    table.item(row_index, 3).setText(str(updated_price))
                else:
                    self.table_key[item_key] = {'prod_name': item_info['prod_name'], 'price': item_info['price'], 'quantity': quantity}
                    table.setRowCount(num_rows + 1)
                    i = num_rows
                    item_row = []
                    for j in range(len(columns)):
                        if j == 0:
                            item = QTableWidgetItem(str(row['prod_id']))
                        elif j == 1:
                            item = QTableWidgetItem(row['prod_name'])
                        elif j == 2:
                            item = QTableWidgetItem(str(quantity))
                        elif j == 3:
                            base_price = float(self.items['price'])
                            modified_price = base_price * quantity
                            item = QTableWidgetItem(str(round(modified_price,2)))
                        item_row.append(item)
                        table.setItem(i, j, item)
            for i in range(table.columnCount()):
                table.setHorizontalHeaderItem(i, QTableWidgetItem(f'{columns[i]}'))
        except Exception as e:
            self.feedbackLabelNewInvoiceTab.setText(e)

    def removeProductButtonNewInvoiceTabClickHandler(self):
        try:
            selected_row = self.invoiceListTableWidgetNewInvoiceTab.currentRow()
            quantity = self.productNumberSpinBoxNewInvoiceTab.value()
            if selected_row >= 0:
                prod_id = int(self.invoiceListTableWidgetNewInvoiceTab.item(selected_row, 0).text())
                current_quantity = int(self.invoiceListTableWidgetNewInvoiceTab.item(selected_row, 2).text())
                if current_quantity > quantity:
                    current_price = float(self.invoiceListTableWidgetNewInvoiceTab.item(selected_row, 3).text())
                    base_price = current_price / current_quantity
                    new_quantity = current_quantity - quantity
                    new_price = round(base_price * new_quantity, 2)
                    self.invoiceListTableWidgetNewInvoiceTab.item(selected_row, 2).setText(str(new_quantity))
                    self.invoiceListTableWidgetNewInvoiceTab.item(selected_row, 3).setText(str(new_price))
                    self.getTotal()
                else:
                    self.invoiceListTableWidgetNewInvoiceTab.removeRow(selected_row)
                    del self.table_key[prod_id]
                    self.getTotal()
        except Exception as e:
            self.feedbackLabelNewInvoiceTab.setText(e)

    def getTotal(self):
        try:
            total = 0.0
            for row in range(self.invoiceListTableWidgetNewInvoiceTab.rowCount()):
                try:
                    price_cell = self.invoiceListTableWidgetNewInvoiceTab.item(row, 3)
                    quantity_cell = self.invoiceListTableWidgetNewInvoiceTab.item(row,2)
                    if price_cell is not None and quantity_cell is not None:
                        price = float(price_cell.text())
                        total += price
                except ValueError:
                    pass
            self.invoiceTotalLineEditNewInvoiceTab.setText('$' + "{:.2f}".format(total))
        except Exception as e:
            self.feedbackLabelNewInvoiceTab.setText(e)

    def purchaseButtonNewInvoiceTabClickHandler(self):
        cust_id = int(self.idLineEditNewInvoiceTab.text())
        for row in range(self.invoiceListTableWidgetNewInvoiceTab.rowCount()):
            try:
                prod_id = int(self.invoiceListTableWidgetNewInvoiceTab.item(row, 0).text())
                quantity = int(self.invoiceListTableWidgetNewInvoiceTab.item(row, 2).text())
                if quantity - checkStock(prod_id)[0][0] > 0:
                    self.feedbackLabelNewInvoiceTab.setText(f'The Quantity of {self.productComboBoxNewInvoiceTab.currentText()}\n would be below 0 if purchase was completed')
                else:
                    createInvoice(cust_id, prod_id, quantity)
                    self.invoiceListTableWidgetNewInvoiceTab.setRowCount(0)
                    self.refreshProductTables()
            except Exception as e:
                self.feedbackLabelNewInvoiceTab.setText(e)
        self.getTotal()

    def addCustomerWidgetSetup(self):
        self.firstNameLineEditAddCustomerTab = self.findChild(QLineEdit, 'firstNameLineEditAddCustomerTab')
        self.lastNameLineEditAddCustomerTab = self.findChild(QLineEdit, 'lastNameLineEditAddCustomerTab')
        self.emailLineEditAddCustomerTab = self.findChild(QLineEdit, 'emailLineEditAddCustomerTab')
        self.addressLineEditAddCustomerTab = self.findChild(QLineEdit, 'addressLineEditAddCustomerTab')
        self.phoneLineEditAddCustomerTab = self.findChild(QLineEdit, 'phoneLineEditAddCustomerTab')
        self.feedbackLabelAddCustomerTab = self.findChild(QLabel, 'feedbackLabelAddCustomerTab')
        self.addCustomerButtonAddCustomerTab = self.findChild(QPushButton, 'addCustomerButtonAddCustomerTab')
        self.addCustomerButtonAddCustomerTab.clicked.connect(self.addCustomerButtonAddCustomerTabClickHandler)

    def addCustomerButtonAddCustomerTabClickHandler(self):
        try:
            fname = self.firstNameLineEditAddCustomerTab.text()
            lname = self.lastNameLineEditAddCustomerTab.text()
            email = self.emailLineEditAddCustomerTab.text()
            address = self.addressLineEditAddCustomerTab.text()
            phone = self.phoneLineEditAddCustomerTab.text()
            assert all(field != '' for field in [fname, lname, email, phone]), 'Only Address can be left empty'
            if address != '':
                addCustomer(fname, lname, email, address, phone)
            else:
                addCustomerNoAddress(fname,lname, email, phone)
            self.newInvoiceWidgetSetup()
            self.editCustomerWidgetSetup()
            self.clearAddCustomerFields()
            self.editCustomerClear()
            self.invoiceCustomerClear()
            self.refreshCustomersComboBoxes()
        except Exception as e:
            self.feedbackLabelAddCustomerTab.setText(str(e))

    def clearAddCustomerFields(self):
        self.feedbackLabelAddCustomerTab.setText(f"{self.firstNameLineEditAddCustomerTab.text()} successfully added to customer database")
        self.firstNameLineEditAddCustomerTab.clear()
        self.lastNameLineEditAddCustomerTab.clear()
        self.emailLineEditAddCustomerTab.clear()
        self.addressLineEditAddCustomerTab.clear()
        self.phoneLineEditAddCustomerTab.clear()

    def editCustomerWidgetSetup(self):
        self.nameComboBoxEditCustomerTab = self.findChild(QComboBox, 'nameComboBoxEditCustomerTab')
        self.idNameLineEditEditCustomerTab = self.findChild(QLineEdit, 'idNameLineEditEditCustomerTab')
        self.emailLineEditEditCustomerTab = self.findChild(QLineEdit, 'emailLineEditEditCustomerTab')
        self.addressLineEditEditCustomerTab = self.findChild(QLineEdit, 'addressLineEditEditCustomerTab')
        self.phoneLineEditEditCustomerTab = self.findChild(QLineEdit, 'phoneLineEditEditCustomerTab')
        self.firstNameLineEditCustomerTab = self.findChild(QLineEdit, 'firstNameLineEditCustomerTab')
        self.lastNameLineEditEditCustomerTab = self.findChild(QLineEdit, 'lastNameLineEditEditCustomerTab')
        self.feedbackLabelEditCustomerTab = self.findChild(QLabel, 'feedbackLabelEditCustomerTab')
        self.saveChangesButton = self.findChild(QPushButton, 'saveChangesButton')
        self.saveChangesButton.clicked.connect(self.saveChangesButtonClickHandler)
        customers = getCustomer()
        self.idNameLineEditEditCustomerTab.setText(str(customers[0][0]))
        self.emailLineEditEditCustomerTab.setText(customers[0][4])
        self.addressLineEditEditCustomerTab.setText(customers[0][5])
        self.phoneLineEditEditCustomerTab.setText(customers[0][6])
        self.firstNameLineEditCustomerTab.setText(customers[0][2])
        self.lastNameLineEditEditCustomerTab.setText(customers[0][3])
        for row in customers:
            self.nameComboBoxEditCustomerTab.addItem(str(row[1]), userData=[row[1], row[0], row[2], row[3], row[4], row[5], row[6]])
        self.nameComboBoxEditCustomerTab.currentIndexChanged.connect(self.idComboBoxEditCustomerTabCurrentIndexChangedHandler)

    def idComboBoxEditCustomerTabCurrentIndexChangedHandler(self):
        try:
            row = self.nameComboBoxEditCustomerTab.currentData()
            if row is None:
                self.idNameLineEditEditCustomerTab.setText('')
                self.firstNameLineEditCustomerTab.setText('')
                self.lastNameLineEditEditCustomerTab.setText('')
                self.emailLineEditEditCustomerTab.setText('')
                self.addressLineEditEditCustomerTab.setText('')
                self.phoneLineEditEditCustomerTab.setText('')
            else:
                self.idNameLineEditEditCustomerTab.setText(str(row[1]))
                self.firstNameLineEditCustomerTab.setText(row[2])
                self.lastNameLineEditEditCustomerTab.setText(row[3])
                self.emailLineEditEditCustomerTab.setText(row[4])
                self.addressLineEditEditCustomerTab.setText(row[5] or '')
                self.phoneLineEditEditCustomerTab.setText(row[6])
        except Exception as e:
            self.feedbackLabelEditCustomerTab.setText(str(e))
            self.feedbackLabelAddCustomerTab.setText(str(e))

    def saveChangesButtonClickHandler(self):
        try:
            id = self.idNameLineEditEditCustomerTab.text()
            email = self.emailLineEditEditCustomerTab.text()
            address = self.addressLineEditEditCustomerTab.text()
            phone = self.phoneLineEditEditCustomerTab.text()
            fname = self.firstNameLineEditCustomerTab.text()
            lname = self.lastNameLineEditEditCustomerTab.text()
            assert all(field != '' for field in [fname, lname, email, phone]), 'Only address can be empty'
            if address != '':
                updateCustomerInfo(id, email, address, phone, fname, lname)
                self.editCustomerClear()
                self.invoiceCustomerClear()
            else:
                updateCustomerInfoBlankAddress(id, email, phone, fname, lname)
                self.editCustomerClear()
                self.invoiceCustomerClear()
            self.refreshCustomersComboBoxes()
        except Exception as e:
            self.feedbackLabelEditCustomerTab.setText(str(e))

    def editCustomerClear(self):
        self.feedbackLabelEditCustomerTab.setText(f"Customer information successfully edited")
        self.nameComboBoxEditCustomerTab.clear()
        self.idNameLineEditEditCustomerTab.clear()
        self.emailLineEditEditCustomerTab.clear()
        self.addressLineEditEditCustomerTab.clear()
        self.phoneLineEditEditCustomerTab.clear()
        self.firstNameLineEditCustomerTab.clear()
        self.lastNameLineEditEditCustomerTab.clear()

    def invoiceCustomerClear(self):
        self.emailLineEditNewInvoiceTab.clear()
        self.idLineEditNewInvoiceTab.clear()
        self.nameComboBoxNewInvoiceTab.clear()


    def refreshCustomersComboBoxes(self):
        self.refreshProductTables()
        try:
            customers = getCustomer()
            for row in customers:
                print(row)
                self.nameComboBoxEditCustomerTab.addItem(str(row[1]), userData=[row[1], row[0], row[2], row[3], row[4], row[5], row[6]])
            self.nameComboBoxEditCustomerTab.currentIndexChanged.connect(self.idComboBoxEditCustomerTabCurrentIndexChangedHandler)
            customers = getCustomerNames()
            for row in customers:
                self.nameComboBoxNewInvoiceTab.addItem(row[1], userData=[row[0], row[2]])
            self.nameComboBoxNewInvoiceTab.currentIndexChanged.connect(self.nameComboBoxNewInvoiceTabCurrentIndexChangedHandler)
        except Exception as e:
            self.feedbackLabelEditCustomerTab.setText(e)

    def addProductWidgetSetup(self):
        self.productNameLineEditAddProductTab = self.findChild(QLineEdit, 'productNameLineEditAddProductTab')
        self.productGenreLineEditAddProductTab = self.findChild(QLineEdit, 'productGenreLineEditAddProductTab')
        self.productDeveloperLineEditAddProductTab = self.findChild(QLineEdit, 'productDeveloperLineEditAddProductTab')
        self.productReleaseDateAddProductTab = self.findChild(QDateEdit, 'productReleaseDateAddProductTab')
        self.productPriceLineEditAddProductTab = self.findChild(QLineEdit, 'productPriceLineEditAddProductTab')
        self.vendorNameComboBoxAddProductTab = self.findChild(QComboBox, 'vendorNameComboBoxAddProductTab')
        self.vendorIdLineEditAddProductTab = self.findChild(QLineEdit, 'vendorIdLineEditAddProductTab')
        self.feedbackLabelAddProductTab = self.findChild(QLineEdit, 'feedbackLabelAddProductTab')
        self.addProductButtonAddProductTab = self.findChild(QPushButton, 'addProductButtonAddProductTab')
        self.addProductButtonAddProductTab.clicked.connect(self.addProductButtonAddProductTabClickHandler)
        vendors = getAllVendors()
        for row in vendors:
            self.vendorNameComboBoxAddProductTab.addItem(row[1], userData=[row[0]])
        self.vendorNameComboBoxAddProductTab.currentIndexChanged.connect(self.vendorNameComboBoxAddProductTabCurrentIndexChangedHandler)

    def vendorNameComboBoxAddProductTabCurrentIndexChangedHandler(self):
        try:
            vendorId = self.vendorNameComboBoxAddProductTab.currentData()[0]
            self.vendorIdLineEditAddProductTab.setText(str(vendorId))
        except Exception as e:
            print(e)

    def addProductButtonAddProductTabClickHandler(self):
        try:
            prod_name = self.productNameLineEditAddProductTab.text()
            genre = self.productGenreLineEditAddProductTab.text()
            dev = self.productDeveloperLineEditAddProductTab.text()
            release = self.productReleaseDateAddProductTab.date().toString('yyyy-MM-dd')
            try:
                price = self.productPriceLineEditAddProductTab.text()
                price_float = float(price)
            except ValueError:
                self.feedbackLabelAddProductTab.setText(str(e))
            vendor_id = self.vendorIdLineEditAddProductTab.text()
            assert all(field != '' for field in [prod_name, genre, dev, release, price_float, vendor_id])

            addProduct(prod_name, genre, dev, release, float(price), int(vendor_id))
            self.refreshProducts()
        except Exception as e:
            self.feedbackLabelAddProductTab.setText(str(e))

    def manageInventoryWidgetSetup(self):
        self.productNameComboBoxEditInventoryTab = self.findChild(QComboBox, 'productNameComboBoxEditInventoryTab')
        self.newProductNameLineEditManageInventoryTab = self.findChild(QLineEdit, 'newProductNameLineEditManageInventoryTab')
        self.newProductGenreLineEditManageInventoryTab = self.findChild(QLineEdit, 'newProductGenreLineEditManageInventoryTab')
        self.newProductDeveloperLineEditManageInventoryTab = self.findChild(QLineEdit, 'newProductDeveloperLineEditManageInventoryTab')
        self.newProductReleaseDateManageInventoryTab = self.findChild(QDateEdit, 'newProductReleaseDateManageInventoryTab')
        self.newProductPriceLineEditManageInventoryTab = self.findChild(QLineEdit, 'newProductPriceLineEditManageInventoryTab')
        self.newVendorNameComboBoxManageInventoryTab = self.findChild(QComboBox, 'newVendorNameComboBoxManageInventoryTab')
        self.vendorIdLineEditManageInventoryTab = self.findChild(QLineEdit, 'vendorIdLineEditManageInventoryTab')
        self.productIdLineEditManageInventoryTab = self.findChild(QLineEdit, 'productIdLineEditManageInventoryTab')
        self.currentInventoryLineEditManageInventoryTab = self.findChild(QLineEdit, 'currentInventoryLineEditManageInventoryTab')
        self.saveChangesButtonManageInventoryTab = self.findChild(QPushButton, 'saveChangesButtonManageInventoryTab')
        self.saveChangesButtonManageInventoryTab.clicked.connect(self.saveChangesButtonManageInventoryTabClickHandler)
        products = getProductss()
        for row in products:
            self.productNameComboBoxEditInventoryTab.addItem(str(row[1]), userData=[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
        self.productNameComboBoxEditInventoryTab.currentIndexChanged.connect(self.productNameComboBoxEditInventoryTabCurrentIndexHandler)
        vendors = getAllVendors()
        for row in vendors:
            self.newVendorNameComboBoxManageInventoryTab.addItem(str(row[1]), userData=[row[0], row[1]])
        self.newVendorNameComboBoxManageInventoryTab.currentIndexChanged.connect(self.newVendorNameComboBoxManageInventoryTabCurrentIndexHandler)

    def productNameComboBoxEditInventoryTabCurrentIndexHandler(self):
        try:
            row = self.productNameComboBoxEditInventoryTab.currentData()
            self.productIdLineEditManageInventoryTab.setText(str(row[0]))
            self.newProductNameLineEditManageInventoryTab.setText(row[1])
            self.newProductGenreLineEditManageInventoryTab.setText(row[2])
            self.newProductDeveloperLineEditManageInventoryTab.setText(row[3])
            # self.newProductReleaseDateManageInventoryTab.setText(row[4])
            self.newProductPriceLineEditManageInventoryTab.setText(str(row[5]))
            self.currentInventoryLineEditManageInventoryTab.setText(str(row[6]))
        except Exception as e:
            print(e)

    def newVendorNameComboBoxManageInventoryTabCurrentIndexHandler(self):
        try:
            vendorId = self.newVendorNameComboBoxManageInventoryTab.currentData()[0]
            self.vendorIdLineEditManageInventoryTab.setText(str(vendorId))
        except Exception as e:
            print(e)

    def saveChangesButtonManageInventoryTabClickHandler(self):
        prod_id = self.productIdLineEditManageInventoryTab.text()
        name = self.newProductNameLineEditManageInventoryTab.text()
        genre = self.newProductGenreLineEditManageInventoryTab.text()
        dev = self.newProductDeveloperLineEditManageInventoryTab.text()
        date = self.newProductReleaseDateManageInventoryTab.text()
        price = self.newProductPriceLineEditManageInventoryTab.text()
        vendor = self.vendorIdLineEditManageInventoryTab.text()
        updateProduct(prod_id, name, genre, dev, date, price, vendor)
        self.refreshProducts()

    def addVendorWidgetSetup(self):
        self.vendorNameLineEditAddVendorTab = self.findChild(QLineEdit, 'vendorNameLineEditAddVendorTab')
        self.addVendorButtonAddVendorTab = self.findChild(QPushButton, 'addVendorButtonAddVendorTab')
        self.addVendorButtonAddVendorTab.clicked.connect(self.addVendorButtonAddVendorTabClickHandler)
        self.feedbackLabelAddVendorTab = self.findChild(QLabel, 'feedbackLabelAddVendorTab')

    def addVendorButtonAddVendorTabClickHandler(self):
        try:
            vendor_name = self.vendorNameLineEditAddVendorTab.text()
            assert vendor_name != '', 'Name cannot be empty'
            addVendor(vendor_name)
            self.refreshVendors()
        except Exception as e:
            self.feedbackLabelAddVendorTab.setText(e)

    def editVendorWidgetSetup(self):
        self.vendorNameComboBoxEditVendorTab = self.findChild(QComboBox, 'vendorNameComboBoxEditVendorTab')
        self.newVendorNameLineEditEditVendorTab = self.findChild(QLineEdit, 'newVendorNameLineEditEditVendorTab')
        self.vendorIdLineEditEditVendorTab = self.findChild(QLineEdit, 'vendorIdLineEditEditVendorTab')
        self.saveChangesButtonEditVendorTab = self.findChild(QPushButton, 'saveChangesButtonEditVendorTab')
        self.saveChangesButtonEditVendorTab.clicked.connect(self.saveChangesButtonEditVendorTabClickHandler)
        vendors = getAllVendors()
        for row in vendors:
            self.vendorNameComboBoxEditVendorTab.addItem(str(row[1]), userData=[row[0], row[1]])
        self.vendorNameComboBoxEditVendorTab.currentIndexChanged.connect(
            self.vendorNameComboBoxEditVendorTabCurrentIndexChangedHandler)

    def vendorNameComboBoxEditVendorTabCurrentIndexChangedHandler(self):
        try:
            vendorId = self.vendorNameComboBoxEditVendorTab.currentData()[0]
            self.vendorIdLineEditEditVendorTab.setText(str(vendorId))
        except Exception as e:
            print(e)

    def saveChangesButtonEditVendorTabClickHandler(self):
        vendor_name = self.newVendorNameLineEditEditVendorTab.text()
        vendor_id = int(self.vendorIdLineEditEditVendorTab.text())
        updateVendor(vendor_id, vendor_name)
        self.refreshVendors()

    def refreshVendors(self):
        self.newVendorNameLineEditEditVendorTab.clear()
        self.vendorIdLineEditEditVendorTab.clear()
        self.vendorNameComboBoxEditVendorTab.clear()
        self.vendorNameComboBoxAddProductTab.clear()
        self.newVendorNameComboBoxManageInventoryTab.clear()
        vendors = getAllVendors()
        for row in vendors:
            self.vendorNameComboBoxEditVendorTab.addItem(str(row[1]), userData=[row[0], row[1]])
        vendors = getAllVendors()
        for row in vendors:
            self.newVendorNameComboBoxManageInventoryTab.addItem(str(row[1]), userData=[row[0], row[1]])
        self.newVendorNameComboBoxManageInventoryTab.currentIndexChanged.connect(self.newVendorNameComboBoxManageInventoryTabCurrentIndexHandler)
        vendors = getAllVendors()
        for row in vendors:
            self.vendorNameComboBoxAddProductTab.addItem(row[1], userData=[row[0]])
        self.vendorNameComboBoxAddProductTab.currentIndexChanged.connect(
            self.vendorNameComboBoxAddProductTabCurrentIndexChangedHandler)

    def refreshProducts(self):
        self.productNameComboBoxEditInventoryTab.clear()
        self.productComboBoxNewInvoiceTab.clear()
        games = getProducts()
        for game in games:
            self.productComboBoxNewInvoiceTab.addItem(str(game[1]))
        products = getProductss()
        for row in products:
            self.productNameComboBoxEditInventoryTab.addItem(str(row[1]),
                                                             userData=[row[0], row[1], row[2], row[3], row[4], row[5],
                                                                       row[6], row[7]])
        self.productNameComboBoxEditInventoryTab.currentIndexChanged.connect(
            self.productNameComboBoxEditInventoryTabCurrentIndexHandler)

    def shipmentWidgetSetup(self):
        self.productComboBoxShipmentsTab = self.findChild(QComboBox, 'productComboBoxShipmentsTab')
        self.productSpinBoxShipmentsTab = self.findChild(QSpinBox, 'productSpinBoxShipmentsTab')
        self.addProductButtonShipmentsTab = self.findChild(QPushButton, 'addProductButtonShipmentsTab')
        self.addProductButtonShipmentsTab.clicked.connect(self.addProductButtonShipmentsTabClickHandler)
        self.removeProductButtonShipmentsTab = self.findChild(QPushButton, 'removeProductButtonShipmentsTab')
        self.removeProductButtonShipmentsTab.clicked.connect(self.removeProductButtonShipmentsTabClickHandler)
        self.submitButtonShipmentsTab = self.findChild(QPushButton, 'submitButtonShipmentsTab')
        self.submitButtonShipmentsTab.clicked.connect(self.submitButtonShipmentsTabClickHandler)
        self.randomShipmentButtonShipmentsTab = self.findChild(QPushButton, 'randomShipmentButtonShipmentsTab')
        self.randomShipmentButtonShipmentsTab.clicked.connect(self.randomShipmentButtonShipmentsTabClickHandler)
        self.shipmentListTableWidgetShipmentsTab = self.findChild(QTableWidget, 'shipmentListTableWidgetShipmentsTab')
        self.feedbackLabelShipmentsTab = self.findChild(QLabel, 'feedbackLabelShipmentsTab')
        games = getProductss()
        for row in games:
            self.productComboBoxShipmentsTab.addItem(row[1], userData=[row[0], row[2]])
        self.shipmentList = {}

    def addProductButtonShipmentsTabClickHandler(self):
        try:
            prodName = self.productComboBoxShipmentsTab.currentText()
            prodID = self.productComboBoxShipmentsTab.currentData()[0]
            amount = self.productSpinBoxShipmentsTab.value()
            if prodID in self.shipmentList.keys():
                self.shipmentList[prodID][1] += amount
            else:
                self.shipmentList[prodID] = [prodName, amount]
            self.displayShipmentList()
        except Exception as e:
            self.feedbackLabelNewInvoiceTab.setText(e)

    def removeProductButtonShipmentsTabClickHandler(self):
        try:
            prodID = self.productComboBoxShipmentsTab.currentData()[0]
            amount = self.productSpinBoxShipmentsTab.value()
            if prodID in self.shipmentList.keys():
                self.shipmentList[prodID][1] -= amount
                if self.shipmentList[prodID][1] <= 0:
                    del self.shipmentList[prodID]
            self.displayShipmentList()
        except Exception as e:
            self.feedbackLabelNewInvoiceTab.setText(e)

    def displayShipmentList(self):
        try:
            columns = ["Product ID", "Product Name", "Quantity"]
            self.shipmentListTableWidgetShipmentsTab.setColumnCount(3)
            self.shipmentListTableWidgetShipmentsTab.setRowCount(len(self.shipmentList))
            for i in range(3):
                self.shipmentListTableWidgetShipmentsTab.setHorizontalHeaderItem(i, QTableWidgetItem(f'{columns[i]}'))
            for numRow in range(len(self.shipmentList)):
                curKey = list(self.shipmentList.keys())[numRow]
                for numColumn in range(3):
                    if numColumn == 0:
                        cellData = QTableWidgetItem(str(curKey))
                        self.shipmentListTableWidgetShipmentsTab.setItem(numRow, numColumn, cellData)
                    else:
                        cellData = QTableWidgetItem(str(self.shipmentList[curKey][numColumn-1]))
                        self.shipmentListTableWidgetShipmentsTab.setItem(numRow, numColumn, cellData)
        except Exception as e:
            print(e)

    def submitButtonShipmentsTabClickHandler(self):
        try:
            for productID, productInfo in self.shipmentList.items():
                adjustStock(productID, productInfo[1])
            self.shipmentList = {}
            self.displayShipmentList()
        except Exception as e:
            print(e)

    def randomShipmentButtonShipmentsTabClickHandler(self):
        try:
            product_list = getProductss()
            attempts = randint(1, len(product_list)*randint(1, 2))
            for products in range(attempts):
                list_id = randint(0, len(product_list)-1)
                product_id = list_id+1
                if product_id in self.shipmentList.keys():
                    self.shipmentList[product_id][1] += randint(1, 200)
                else:
                    self.shipmentList[product_id] = [product_list[list_id][1], randint(1, 200)]
            self.displayShipmentList()
            self.refreshProductTables()
        except Exception as e:
            print(e)

    def viewWidgetSetup(self):
        self.viewSelectionComboBoxViewTab = self.findChild(QComboBox, 'viewSelectionComboBoxViewTab')
        self.viewTableWidgetViewTab = self.findChild(QTableWidget, 'viewTableWidgetViewTab')
        colNames, data = getAllInventory()
        self.displayInView(colNames, data)
        self.viewSelectionComboBoxViewTab.currentIndexChanged.connect(self.viewSelectionComboBoxViewTabCurrentIndexChangedHandler)

    def viewSelectionComboBoxViewTabCurrentIndexChangedHandler(self):
        self.viewTableWidgetViewTab.clear()
        currently = self.viewSelectionComboBoxViewTab.currentText()
        if currently == 'Inventory':
            colNames, data = getAllInventory()
        elif currently == 'Out Of Stock':
            colNames, data = outOfStock()
        elif currently == 'Vendors':
            colNames, data = getAllVendorsForTable()
        elif currently == 'Customers':
            colNames, data = getAllCustomers()
        elif currently == 'Recent Customers':
            colNames, data = getRecentCustomers()
        self.displayInView(colNames, data)

    def refreshProductTables(self):
        self.viewTableWidgetViewTab.clear()

    def displayInView(self, columns, rows):
        try:
            self.viewTableWidgetViewTab.setRowCount(len(rows))
            self.viewTableWidgetViewTab.setColumnCount(len(columns))
            for i in range(len(rows)):
                row = rows[i]
                for j in range(len(row)):
                    self.viewTableWidgetViewTab.setItem(i, j, QTableWidgetItem(str(row[j])))
            for i in range(self.viewTableWidgetViewTab.columnCount()):
                self.viewTableWidgetViewTab.setHorizontalHeaderItem(i, QTableWidgetItem(f'{columns[i]}'))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()