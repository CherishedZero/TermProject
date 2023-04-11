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
        self.purchaseButtonNewInvoiceTab = self.findChild(QPushButton, 'purchasebutton')
        #self.purchaseButtonNewInvoiceTab.clicked.connect(purchaseButtonNewInvoiceTabClickHandler)
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
                    quantity = int(quantity_cell.text())
                    total += price
            except ValueError:
                pass
        self.invoiceTotalLineEditNewInvoiceTab.setText('$' + "{:.2f}".format(total))


    def addCustomerWidgetSetup(self):
        self.firstNameLineEditAddCustomerTab = self.findChild(QLineEdit, 'firstNameLineEditAddCustomerTab')
        self.lastNameLineEditAddCustomerTab = self.findChild(QLineEdit, 'lastNameLineEditAddCustomerTab')
        self.emailLineEditAddCustomerTab = self.findChild(QLineEdit, 'emailLineEditAddCustomerTab')
        self.addressLineEditAddCustomerTab = self.findChild(QLineEdit, 'addressLineEditAddCustomerTab')
        self.phoneLineEditAddCustomerTab = self.findChild(QLineEdit, 'phoneLineEditAddCustomerTab')
        self.addCustomerButtonAddCustomerTab = self.findChild(QPushButton, 'addCustomerButtonAddCustomerTab')
        self.addCustomerButtonAddCustomerTab.clicked.connect(self.addCustomerButtonAddCustomerTabClickHandler)

    def addCustomerButtonAddCustomerTabClickHandler(self):
        try:
            fname = self.firstNameLineEditAddCustomerTab.text()
            lname = self.lastNameLineEditAddCustomerTab.text()
            email = self.emailLineEditAddCustomerTab.text()
            address = self.addressLineEditAddCustomerTab.text()
            phone = self.phoneLineEditAddCustomerTab.text()
            assert all(field != '' for field in [fname, lname, email, phone]), 'All fields must have an entry'
            if address != '':
                addCustomer(fname, lname, email, address, phone)
            else:
                addCustomerNoAddress(fname,lname, email, phone)
        except Exception as e:
            print(e)

    def editCustomerWidgetSetup(self):
        self.nameComboBoxEditCustomerTab = self.findChild(QComboBox, 'nameComboBoxEditCustomerTab')
        self.idNameLineEditEditCustomerTab = self.findChild(QLineEdit, 'idNameLineEditEditCustomerTab')
        self.emailLineEditEditCustomerTab = self.findChild(QLineEdit, 'emailLineEditEditCustomerTab')
        self.addressLineEditEditCustomerTab = self.findChild(QLineEdit, 'addressLineEditEditCustomerTab')
        self.phoneLineEditEditCustomerTab = self.findChild(QLineEdit, 'phoneLineEditEditCustomerTab')
        self.firstNameLineEditCustomerTab = self.findChild(QLineEdit, 'firstNameLineEditCustomerTab')
        self.lastNameLineEditEditCustomerTab = self.findChild(QLineEdit, 'lastNameLineEditEditCustomerTab')
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
            print(e)

    def saveChangesButtonClickHandler(self):
        try:
            id = self.idNameLineEditEditCustomerTab.text()
            email = self.emailLineEditEditCustomerTab.text()
            address = self.addressLineEditEditCustomerTab.text()
            phone = self.phoneLineEditEditCustomerTab.text()
            fname = self.firstNameLineEditCustomerTab.text()
            lname = self.lastNameLineEditEditCustomerTab.text()
            if address != '':
                updateCustomerInfo(id, email, address, phone, fname, lname)
            else:
                updateCustomerInfoBlankAddress(id, email, phone, fname, lname)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
