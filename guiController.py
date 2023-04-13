from sqltesting import *
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        """
        Initializes the main window of the application and sets up the UI, widgets,
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
        self.emailLineNewInvoiceTab = self.findChild(QLineEdit, 'emailLineEditNewInvoiceTab')
        self.idLineEditNewInvoiceTab = self.findChild(QLineEdit, 'idLineEditNewInvoiceTab')
        self.productComboBoxNewInvoiceTab = self.findChild(QComboBox, 'productComboBoxNewInvoiceTab')
        self.productNumberSpinBoxNewInvoiceTab = self.findChild(QSpinBox, 'productNumberSpinBoxNewInvoiceTab')
        self.invoiceTotalLineEditNewInvoiceTab = self.findChild(QLineEdit, 'invoiceTotalLineEditNewInvoiceTab')
        self.invoiceListTableWidgetNewInvoiceTab = self.findChild(QTableWidget, 'invoiceListTableWidgetNewInvoiceTab')
        self.addProductButtonNewInvoiceTab = self.findChild(QPushButton, 'addProductButtonNewInvoiceTab')
        self.addProductButtonNewInvoiceTab.clicked.connect(self.addProductButtonNewInvoiceTabClickHandler)
        self.removeProductButtonNewInvoiceTab = self.findChild(QPushButton, 'removeProductButtonNewInvoiceTab')
        self.removeProductButtonNewInvoiceTab.clicked.connect(self.removeProductButtonNewInvoiceTabClickHandler)
        self.purchaseButtonNewInvoiceTab = self.findChild(QPushButton, 'purchaseButtonNewInvoiceTab')
        self.purchaseButtonNewInvoiceTab.clicked.connect(self.purchaseButtonNewInvoiceTabClickHandler)
        customers = getCustomerNames()
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
            self.emailLineNewInvoiceTab.setText(customerEmail)
            self.idLineEditNewInvoiceTab.setText(str(customerId))
        except Exception as e:
            print(e)

    def addProductButtonNewInvoiceTabClickHandler(self):
        prodName = self.productComboBoxNewInvoiceTab.currentText()
        colNames, info = getGameInfoByName(prodName)
        self.displayGameInfoInTable(colNames, [info], self.invoiceListTableWidgetNewInvoiceTab)
        self.getTotal()

    def displayGameInfoInTable(self, columns, rows, table:QTableWidget):
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
                self.table_key[item_key] = {'prod_name': item_info['prod_name'],
                                            'price': item_info['price'],
                                            'quantity': quantity}
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

    def removeProductButtonNewInvoiceTabClickHandler(self):
        selected_row = self.invoiceListTableWidgetNewInvoiceTab.currentRow()
        quantity = self.productNumberSpinBoxNewInvoiceTab.value()
        if selected_row >= 0:
            prod_id = int(self.invoiceListTableWidgetNewInvoiceTab.item(selected_row, 0).text())
            current_quantity = int(self.invoiceListTableWidgetNewInvoiceTab.item(selected_row, 2).text())

            if current_quantity > quantity:
                # Update the quantity and price of the product
                current_price = float(self.invoiceListTableWidgetNewInvoiceTab.item(selected_row, 3).text())
                base_price = current_price / current_quantity
                new_quantity = current_quantity - quantity
                new_price = round(base_price * new_quantity, 2)

                # Update the table with the new quantity and price
                self.invoiceListTableWidgetNewInvoiceTab.item(selected_row, 2).setText(str(new_quantity))
                self.invoiceListTableWidgetNewInvoiceTab.item(selected_row, 3).setText(str(new_price))
                self.getTotal()
            else:
                # Remove the entire row from the table
                self.invoiceListTableWidgetNewInvoiceTab.removeRow(selected_row)
                del self.table_key[prod_id]
                self.getTotal()

    def getTotal(self):
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

    def purchaseButtonNewInvoiceTabClickHandler(self):
        cust_id = int(self.idLineEditNewInvoiceTab.text())

        for row in range(self.invoiceListTableWidgetNewInvoiceTab.rowCount()):
            try:
                prod_id = int(self.invoiceListTableWidgetNewInvoiceTab.item(row, 0).text())
                quantity = int(self.invoiceListTableWidgetNewInvoiceTab.item(row, 2).text())
                createInvoice(cust_id, prod_id, quantity)
            except ValueError:
                pass

        # Clear the invoice list table and reset the invoice total
        self.invoiceListTableWidgetNewInvoiceTab.setRowCount(0)
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
                self.nameComboBoxEditCustomerTab.clear()
                self.nameComboBoxNewInvoiceTab.clear()
                self.newInvoiceWidgetSetup()
                self.editCustomerWidgetSetup()
                self.clearAddCustomerFields()
            else:
                addCustomerNoAddress(fname,lname, email, phone)
                self.nameComboBoxEditCustomerTab.clear()
                self.nameComboBoxNewInvoiceTab.clear()
                self.newInvoiceWidgetSetup()
                self.editCustomerWidgetSetup()
                self.clearAddCustomerFields()
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
        for row in customers:
            self.nameComboBoxEditCustomerTab.addItem(str(row[1]), userData=[row[1], row[0], row[2], row[3], row[4], row[5], row[6]])
        self.nameComboBoxEditCustomerTab.currentIndexChanged.connect(self.idComboBoxEditCustomerTabCurrentIndexChangedHandler)

    def idComboBoxEditCustomerTabCurrentIndexChangedHandler(self):
        try:
            # Get the selected row from the combo box
            row = self.nameComboBoxEditCustomerTab.currentData()
            if row is None:
                # If there is no selected row, clear the line edit boxes
                self.idNameLineEditEditCustomerTab.setText('')
                self.firstNameLineEditCustomerTab.setText('')
                self.lastNameLineEditEditCustomerTab.setText('')
                self.emailLineEditEditCustomerTab.setText('')
                self.addressLineEditEditCustomerTab.setText('')
                self.phoneLineEditEditCustomerTab.setText('')
            else:
                # Populate the line edit boxes with the values from the selected row
                self.idNameLineEditEditCustomerTab.setText(str(row[1]))
                self.firstNameLineEditCustomerTab.setText(row[5])
                self.lastNameLineEditEditCustomerTab.setText(row[6])
                self.emailLineEditEditCustomerTab.setText(row[2])
                self.addressLineEditEditCustomerTab.setText(row[3] or '')
                self.phoneLineEditEditCustomerTab.setText(row[4])
        except Exception as e:
            self.feedbackLabelEditCustomerTab.setText(str(e))

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
            else:
                updateCustomerInfoBlankAddress(id, email, phone, fname, lname)
                self.editCustomerClear()
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
        self.nameComboBoxNewInvoiceTab.clear()
        self.emailLineNewInvoiceTab.clear()
        self.idLineEditNewInvoiceTab.clear()



    def refreshCustomersComboBoxes(self):
        self.editCustomerClear()
        self.invoiceCustomerClear()
        try:
            customers = getCustomer()
            for row in customers:
                self.nameComboBoxEditCustomerTab.addItem(str(row[1]), userData=[row[1], row[0], row[2], row[3], row[4], row[5], row[6]])
            self.nameComboBoxEditCustomerTab.currentIndexChanged.connect(self.idComboBoxEditCustomerTabCurrentIndexChangedHandler)
            customers = getCustomerNames()
            for row in customers:
                self.nameComboBoxNewInvoiceTab.addItem(row[1], userData=[row[0], row[2]])
            self.nameComboBoxNewInvoiceTab.currentIndexChanged.connect(self.nameComboBoxNewInvoiceTabCurrentIndexChangedHandler)
        except Exception as e:
            print(e)
###########################################################################################################################
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
        vendors = getVendors()
        for row in vendors:
            print(row[1])
            self.vendorNameComboBoxAddProductTab.addItem(row[1], userData=[row[0]])
        self.vendorNameComboBoxAddProductTab.currentIndexChanged.connect(self.vendorNameComboBoxAddProductTabCurrentIndexChangedHandler)

    def vendorNameComboBoxAddProductTabCurrentIndexChangedHandler(self):
        id = self.vendorNameComboBoxAddProductTab.currentData()[0]
        self.vendorIdLineEditAddProductTab.setText(str(id))

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
        except Exception as e:
            print(e)
            self.feedbackLabelAddProductTab.setText(str(e))

    def manageInventoryWidgetSetup(self):
        self.productNameComboBoxEditInventoryTab = self.findChild(QLineEdit, 'productNameComboBoxEditInventoryTab')
        self.newProductNameLineEditManageInventoryTab = self.findChild(QLineEdit, 'newProductNameLineEditManageInventoryTab')
        self.newProductGenreLineEditManageInventoryTab = self.findChild(QLineEdit, 'newProductGenreLineEditManageInventoryTab')
        self.newProductDeveloperLineEditManageInventoryTab = self.findChild(QLineEdit, 'newProductDeveloperLineEditManageInventoryTab')
        self.newProductReleaseDateManageInventoryTab = self.findChild(QDateEdit, 'newProductReleaseDateManageInventoryTab')
        self.newProductPriceLineEditManageInventoryTab = self.findChild(QLineEdit, 'newProductPriceLineEditManageInventoryTab')
        self.newVendorNameComboBoxManageInventoryTab = self.findChild(QComboBox, 'newVendorNameComboBoxManageInventoryTab')
        self.productIdLineEditManageInventoryTab = self.findChild(QLineEdit, 'productIdLineEditManageInventoryTab')
        self.currentInventoryLineEditManageInventoryTab = self.findChild(QLineEdit, 'currentInventoryLineEditManageInventoryTab')
        self.quantitySpinBoxManageInventoryTab = self.findChild(QSpinBox, 'quantitySpinBoxManageInventoryTab')
        self.addQuantityButtonManageInventoryTab = self.findChild(QComboBox, 'addQuantityButtonManageInventoryTab')
        self.removeQuantityButtonManageInventoryTab = self.findChild(QLineEdit, 'removeQuantityButtonManageInventoryTab')
        self.saveChangesButtonManageInventoryTab = self.findChild(QLineEdit, 'saveChangesButtonManageInventoryTab')
        self.feedbackLabelManageInventoryTab = self.findChild(QLabel, 'feedbackLabelManageInventoryTab')

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
        except Exception as e:
            print(e)
            self.feedbackLabelAddVendorTab.setText(e)

    def editVendorWidgetSetup(self):
        self.vendorNameComboBoxEditVendorTab = self.findChild(QComboBox, 'vendorNameComboBoxEditVendorTab')
        self.newVendorNameLineEditEditVendorTab = self.findChild(QLineEdit, 'newVendorNameLineEditEditVendorTab')
        self.vendorIdLineEditEditVendorTab = self.findChild(QLineEdit, 'vendorIdLineEditEditVendorTab')
        self.saveChangesButtonEditVendorTab = self.findChild(QPushButton, 'saveChangesButtonEditVendorTab')
        self.feedbackLabelEditVendorTab = self.findChild(QLabel, 'feedbackLabelEditVendorTab')

    def shipmentWidgetSetup(self):
        self.productComboBoxShipmentsTab = self.findChild(QComboBox, 'productComboBoxShipmentsTab')
        self.productSpinBoxShipmentsTab = self.findChild(QSpinBox, 'productSpinBoxShipmentsTab')
        self.addProductButtonShipmentsTab = self.findChild(QPushButton, 'addProductButtonShipmentsTab')
        self.removeProductButtonShipmentsTab = self.findChild(QPushButton, 'removeProductButtonShipmentsTab')
        self.submitButtonShipmentsTab = self.findChild(QPushButton, 'submitButtonShipmentsTab')
        self.randomShipmentButtonShipmentsTab = self.findChild(QPushButton, 'randomShipmentButtonShipmentsTab')
        self.shipmentListTableWidgetShipmentsTab = self.findChild(QTableWidget, 'shipmentListTableWidgetShipmentsTab')
        self.feedbackLabelShipmentsTab = self.findChild(QLabel, 'feedbackLabelShipmentsTab')

    def viewWidgetSetup(self):
        self.viewSelectionComboBoxViewTab = self.findChild(QComboBox, 'viewSelectionComboBoxViewTab')
        self.viewTableWidgetViewTab = self.findChild(QTableWidget, 'viewTableWidgetViewTab')
        colNames, data = getAllInventory()
        self.displayInventoryInTable(colNames, data, self.viewTableWidgetViewTab)
        self.viewSelectionComboBoxViewTab.currentIndexChanged.connect(self.viewSelectionComboBoxViewTabCurrentIndexChangedHandler)

    def viewSelectionComboBoxViewTabCurrentIndexChangedHandler(self):
        self.viewTableWidgetViewTab.clear()
        currently = self.viewSelectionComboBoxViewTab.currentText()
        if currently == 'Inventory':
            colNames, data = getAllInventory()
            self.displayInventoryInTable(colNames, data, self.viewTableWidgetViewTab)
        elif currently == 'Out Of Stock':
            colNames, data = outOfStock()
            self.displayOutOfStockInTable(colNames, data, self.viewTableWidgetViewTab)
        elif currently == 'Vendors':
            colNames, data = getAllVendors()
            self.displayVendorsInTable(colNames, data, self.viewTableWidgetViewTab)
        elif currently == 'Customers':
            colNames, data = getAllCustomers()
            self.displayCustomersInTable(colNames, data, self.viewTableWidgetViewTab)

    def displayInventoryInTable(self, columns, rows, table:QTableWidget):
        table.setRowCount(len(rows))
        table.setColumnCount(len(columns))
        for i in range(len(rows)):
            row = rows[i]
            for j in range(len(row)):
                table.setItem(i, j, QTableWidgetItem(str(row[j])))
        columns = ['ID', 'Name', 'Genre', 'Developer', 'Release Date', 'Price', 'Stock', 'Publisher']
        for i in range(table.columnCount()):
            table.setHorizontalHeaderItem(i, QTableWidgetItem(f'{columns[i]}'))

    def displayOutOfStockInTable(self, columns, rows, table:QTableWidget):
        table.setRowCount(len(rows))
        table.setColumnCount(len(columns))
        for i in range(len(rows)):
            row = rows[i]
            for j in range(len(row)):
                table.setItem(i, j, QTableWidgetItem(str(row[j])))
        columns = ['ID', 'Name', 'Genre', 'Developer', 'Release Date', 'Price', 'Stock', 'Publisher']
        for i in range(table.columnCount()):
            table.setHorizontalHeaderItem(i, QTableWidgetItem(f'{columns[i]}'))

    def displayVendorsInTable(self, columns, rows, table:QTableWidget):
        table.setRowCount(len(rows))
        table.setColumnCount(len(columns))
        for i in range(len(rows)):
            row = rows[i]
            for j in range(len(row)):
                table.setItem(i, j, QTableWidgetItem(str(row[j])))
        columns = ['ID', 'Name']
        for i in range(table.columnCount()):
            table.setHorizontalHeaderItem(i, QTableWidgetItem(f'{columns[i]}'))

    def displayCustomersInTable(self, columns, rows, table:QTableWidget):
        print('here')
        table.setRowCount(len(rows))
        table.setColumnCount(len(columns))
        for i in range(len(rows)):
            row = rows[i]
            for j in range(len(row)):
                table.setItem(i, j, QTableWidgetItem(str(row[j])))
        columns = ['ID', 'Name', 'Email', 'Home Address', 'Phone Number']
        for i in range(table.columnCount()):
            table.setHorizontalHeaderItem(i, QTableWidgetItem(f'{columns[i]}'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

