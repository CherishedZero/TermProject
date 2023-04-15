from sqltesting import *
import sys
from random import randint

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

    def newInvoiceWidgetSetup(self):
        """
            Sets up the widgets and connections for the new invoice tab.

            Initializes and assigns values to several widgets including:
                - nameComboBoxNewInvoiceTab: a combobox for selecting a customer's name
                - emailLineEditNewInvoiceTab: a line edit for displaying a customer's email
                - idLineEditNewInvoiceTab: a line edit for displaying a customer's id
                - productComboBoxNewInvoiceTab: a combobox for selecting a product
                - productNumberSpinBoxNewInvoiceTab: a spin box for selecting the number of products to purchase
                - invoiceTotalLineEditNewInvoiceTab: a line edit for displaying the total cost of the invoice
                - invoiceListTableWidgetNewInvoiceTab: a table widget for displaying the items in the invoice
                - feedbackLabelNewInvoiceTab: a label for displaying feedback to the user
                - addProductButtonNewInvoiceTab: a button for adding a product to the invoice list
                - removeProductButtonNewInvoiceTab: a button for removing a product from the invoice list
                - purchaseButtonNewInvoiceTab: a button for finalizing the purchase and creating the invoice

            Sets up the initial values for the nameComboBoxNewInvoiceTab, emailLineEditNewInvoiceTab, and idLineEditNewInvoiceTab
            by getting the list of customers and selecting the first one by default. Sets up the initial values for the
            productComboBoxNewInvoiceTab by getting the list of products.

            Connects several signals to slots including:
                - addProductButtonNewInvoiceTab.clicked: connects to addProductButtonNewInvoiceTabClickHandler
                - removeProductButtonNewInvoiceTab.clicked: connects to removeProductButtonNewInvoiceTabClickHandler
                - purchaseButtonNewInvoiceTab.clicked: connects to purchaseButtonNewInvoiceTabClickHandler

        """
        self.table_dict = {}
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
        print(games)
        for row in customers:
            self.nameComboBoxNewInvoiceTab.addItem(row[1], userData=[row[0], row[2]])
        self.nameComboBoxNewInvoiceTab.currentIndexChanged.connect(self.nameComboBoxNewInvoiceTabCurrentIndexChangedHandler)
        self.invoiceList = {}
        for game in games:
            self.productComboBoxNewInvoiceTab.addItem(game[1], userData=[game[0], game[1], game[5]])

    def nameComboBoxNewInvoiceTabCurrentIndexChangedHandler(self):
        """
            Handles the currentIndexChanged event of the nameComboBoxNewInvoiceTab ComboBox in the New Invoice tab.
            Updates the email address and customer ID line edits when the user selects a different customer name from the ComboBox.
        """
        try:
            customerId = self.nameComboBoxNewInvoiceTab.currentData()[0]
            customerEmail = self.nameComboBoxNewInvoiceTab.currentData()[1]
            self.emailLineEditNewInvoiceTab.setText(customerEmail)
            self.idLineEditNewInvoiceTab.setText(str(customerId))
        except Exception as e:
            self.feedbackLabelNewInvoiceTab.setText(str(e))

    def addProductButtonNewInvoiceTabClickHandler(self):
        """
            Add a new product to the invoice list when the "Add Product" button is clicked.

            Retrieves the selected product name, ID, price, and quantity from the corresponding widgets in the
            new invoice tab. If the product is already in the invoice list, its quantity is updated; otherwise,
            a new entry is added to the invoice list. Then, the updated invoice list is displayed in the table
            widget.

            Raises:
                Exception: If any error occurs while retrieving or updating the product information.

        """
        try:
            prodName = self.productComboBoxNewInvoiceTab.currentText()
            prodID = self.productComboBoxNewInvoiceTab.currentData()[0]
            prodPrice = self.productComboBoxNewInvoiceTab.currentData()[2]
            quantity = self.productNumberSpinBoxNewInvoiceTab.value()
            if prodID in self.invoiceList.keys():
                self.invoiceList[prodID][1] += quantity
            else:
                self.invoiceList[prodID] = [prodName, quantity, prodPrice]
            self.displayGameInfoInTable()
        except Exception as e:
            self.feedbackLabelNewInvoiceTab.setText(str(e))


    def displayGameInfoInTable(self):
        """
            Update the invoice list table with the information about the games being added to the invoice.
            The method retrieves the data from the `self.invoiceList` dictionary and sets the data in the
            `self.invoiceListTableWidgetNewInvoiceTab` table widget.

            Raises:
                Exception: If an error occurs while setting the data in the table widget.

        """
        try:
            colNames = ['ID', 'Game', 'Quantity', 'Price($)']
            self.invoiceListTableWidgetNewInvoiceTab.setColumnCount(4)
            self.invoiceListTableWidgetNewInvoiceTab.setRowCount(len(self.invoiceList))
            for i in range(4):
                self.invoiceListTableWidgetNewInvoiceTab.setHorizontalHeaderItem(i, QTableWidgetItem(f"{colNames[i]}"))
            for numRow in range(len(self.invoiceList)):
                key = list(self.invoiceList.keys())[numRow]
                for numColumn in range(4):
                    if numColumn == 0:
                        cellData = QTableWidgetItem(str(key))
                        self.invoiceListTableWidgetNewInvoiceTab.setItem(numRow, numColumn, cellData)
                    elif numColumn == 1:
                        cellData = QTableWidgetItem(str(self.invoiceList[key][0]))
                        self.invoiceListTableWidgetNewInvoiceTab.setItem(numRow, numColumn, cellData)
                    elif numColumn == 2:
                        cellData = QTableWidgetItem(str(self.invoiceList[key][1]))
                        self.invoiceListTableWidgetNewInvoiceTab.setItem(numRow, numColumn, cellData)
                    else:
                        line_total = float(self.invoiceList[key][2]) * float(self.invoiceList[key][1])
                        cellData = QTableWidgetItem("{:.2f}".format(line_total))
                        self.invoiceListTableWidgetNewInvoiceTab.setItem(numRow, numColumn, cellData)
                        self.getTotal()
        except Exception as e:
            print(e)

    def removeProductButtonNewInvoiceTabClickHandler(self):
        """
                Removes the selected product from the invoice list in the new invoice tab.
                The method first retrieves the product ID and quantity from the corresponding
                widgets. If the product ID is found in the invoice list, the method decrements
                the product quantity by the selected quantity. If the resulting quantity is
                zero or negative, the method removes the product from the invoice list. Finally,
                the method updates the invoice list table widget by calling the displayGameInfoInTable
                method.

                Raises:
                    Exception: If an error occurs while retrieving or updating the data in the
                               widgets, the error message is displayed in the feedback label widget.
        """
        try:
            prodID = self.productComboBoxNewInvoiceTab.currentData()[0]
            quantity = self.productNumberSpinBoxNewInvoiceTab.value()
            if prodID in self.invoiceList.keys():
                self.invoiceList[prodID][1] -= quantity
                if self.invoiceList[prodID][1] <= 0:
                    del self.invoiceList[prodID]
            self.displayGameInfoInTable()
            self.getTotal()
        except Exception as e:
            self.feedbackLabelNewInvoiceTab.setText(e)


    def getTotal(self):
        """
            Calculates and displays the total price of all products in the invoice table.

            This method loops through all the rows in the invoice table and extracts the
            price and quantity of each product. It then calculates the total price of all
            the products and displays it in the invoice total line edit field.

            Raises:
                Exception: If there is an error while calculating the total price or updating
                    the invoice total line edit field.
        """
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
        """
            Handle the click of the 'Purchase' button on the 'New Invoice' tab.

            Loop through the invoiceList and check the stock quantity of each product against the quantity requested.
            If there is insufficient stock, set feedbackLabelNewInvoiceTab to an error message and break the loop.
            If all products have sufficient stock, create a new invoice, update the UI, and clear the invoiceList.
        """
        break_condition = False
        for key, value in self.invoiceList.items():
            print(key, value)
            try:
                prod_id = int(key)
                prod_name = value[0]
                quantity = value[1]
                stocked = checkStock(prod_id)
                print(prod_id, prod_name, quantity, stocked)
                if stocked[0][0] - quantity < 0:
                    self.feedbackLabelNewInvoiceTab.setText(f'The quantity of {prod_name}\n is {stocked[0][0]}. Please remove some.')
                    break_condition = True
                    break
            except Exception as e:
                print(e)
        if not break_condition:
            createInvoice(self.idLineEditNewInvoiceTab.text(), self.invoiceList)
            self.invoiceListTableWidgetNewInvoiceTab.clearContents()
            self.invoiceListTableWidgetNewInvoiceTab.setRowCount(0)
            self.refreshProductTables()
            self.invoiceList.clear()
            self.refreshInvoiceTab()
            self.getTotal()
            self.table_dict.clear()

    def refreshInvoiceTab(self):
        """
            Reset the invoice tab to its initial state.

            This function resets the customer and product combo boxes, and clears the product quantity spin box. It is
            intended to be called when the user wants to start a new invoice.

        """
        self.nameComboBoxNewInvoiceTab.setCurrentIndex(0)
        self.productComboBoxNewInvoiceTab.setCurrentIndex(0)
        self.productNumberSpinBoxNewInvoiceTab.clear()

    def addCustomerWidgetSetup(self):
        """
            Sets up the widgets and connections for the Add Customer tab.

            Initializes and assigns values to several widgets including:
            - firstNameLineEditAddCustomerTab: a line edit for entering the customer's first name
            - lastNameLineEditAddCustomerTab: a line edit for entering the customer's last name
            - emailLineEditAddCustomerTab: a line edit for entering the customer's email
            - addressLineEditAddCustomerTab: a line edit for entering the customer's address
            - phoneLineEditAddCustomerTab: a line edit for entering the customer's phone number
            - feedbackLabelAddCustomerTab: a label for displaying feedback to the user
            - addCustomerButtonAddCustomerTab: a button for adding the customer to the database

            Connects the addCustomerButtonAddCustomerTab.clicked signal to the
            addCustomerButtonAddCustomerTabClickHandler slot.

            Returns:
                None
        """
        self.firstNameLineEditAddCustomerTab = self.findChild(QLineEdit, 'firstNameLineEditAddCustomerTab')
        self.lastNameLineEditAddCustomerTab = self.findChild(QLineEdit, 'lastNameLineEditAddCustomerTab')
        self.emailLineEditAddCustomerTab = self.findChild(QLineEdit, 'emailLineEditAddCustomerTab')
        self.addressLineEditAddCustomerTab = self.findChild(QLineEdit, 'addressLineEditAddCustomerTab')
        self.phoneLineEditAddCustomerTab = self.findChild(QLineEdit, 'phoneLineEditAddCustomerTab')
        self.feedbackLabelAddCustomerTab = self.findChild(QLabel, 'feedbackLabelAddCustomerTab')
        self.addCustomerButtonAddCustomerTab = self.findChild(QPushButton, 'addCustomerButtonAddCustomerTab')
        self.addCustomerButtonAddCustomerTab.clicked.connect(self.addCustomerButtonAddCustomerTabClickHandler)

    def addCustomerButtonAddCustomerTabClickHandler(self):
        """
            Handles the click of the add customer button in the add customer tab.

            Gets the input values from the various QLineEdit fields in the add customer tab and
            passes them to the addCustomer function which attempts to add the customer to the database.
            If successful, the add customer, edit customer, and new invoice tabs are refreshed and the
            add customer fields are cleared.

            If the address field is left blank, the addCustomerNoAddress function is called instead.

            If an exception is raised during the addCustomer function call or the input fields are
            not properly filled, an error message is displayed in the feedbackLabelAddCustomerTab.

        """
        try:
            fname = self.firstNameLineEditAddCustomerTab.text()
            lname = self.lastNameLineEditAddCustomerTab.text()
            email = self.emailLineEditAddCustomerTab.text()
            address = self.addressLineEditAddCustomerTab.text()
            phone = self.phoneLineEditAddCustomerTab.text()
            assert all(field != '' for field in [fname, lname, email, phone]), 'Only Address can be left empty'
            if address != '':
                addCustomer(fname, lname, email, address, phone)
                self.newInvoiceWidgetSetup()
                self.editCustomerWidgetSetup()
                self.clearAddCustomerFields()
                self.editCustomerClear()
                self.invoiceCustomerClear()
                self.refreshCustomersComboBoxes()
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
        """
          Clears the input fields in the "Add Customer" tab and sets a feedback message to indicate that
          the customer has been successfully added to the database.

          Clears the following fields:
             - firstNameLineEditAddCustomerTab
             - lastNameLineEditAddCustomerTab
             - emailLineEditAddCustomerTab
             - addressLineEditAddCustomerTab
             - phoneLineEditAddCustomerTab

            Sets the feedbackLabelAddCustomerTab to display a success message, including the first name of the
            customer that was just added.
        """
        self.feedbackLabelAddCustomerTab.setText(f"{self.firstNameLineEditAddCustomerTab.text()} successfully added to customer database")
        self.firstNameLineEditAddCustomerTab.clear()
        self.lastNameLineEditAddCustomerTab.clear()
        self.emailLineEditAddCustomerTab.clear()
        self.addressLineEditAddCustomerTab.clear()
        self.phoneLineEditAddCustomerTab.clear()

    def editCustomerWidgetSetup(self):
        """
        Sets up the widgets and connections for the edit customer tab.

        Initializes and assigns values to several widgets including:
            - nameComboBoxEditCustomerTab: a combobox for selecting a customer to edit
            - idNameLineEditEditCustomerTab: a line edit for displaying a customer's id
            - emailLineEditEditCustomerTab: a line edit for displaying/editing a customer's email
            - addressLineEditEditCustomerTab: a line edit for displaying/editing a customer's address
            - phoneLineEditEditCustomerTab: a line edit for displaying/editing a customer's phone number
            - firstNameLineEditCustomerTab: a line edit for displaying/editing a customer's first name
            - lastNameLineEditEditCustomerTab: a line edit for displaying/editing a customer's last name
            - feedbackLabelEditCustomerTab: a label for displaying feedback to the user
            - saveChangesButton: a button for saving changes made to the customer's information

        Sets up the initial values for the widgets by getting the first customer in the list of customers and
        populating the combobox with all customers.

        Connects the saveChangesButton.clicked signal to the saveChangesButtonClickHandler method.
        Connects the nameComboBoxEditCustomerTab.currentIndexChanged signal to the
        idComboBoxEditCustomerTabCurrentIndexChangedHandler method.

        """
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
        """
            Handler for when the index of the nameComboBoxEditCustomerTab is changed.
            Updates the values of several QLineEdit widgets based on the current selection in the nameComboBoxEditCustomerTab.
            If the currentData of the nameComboBoxEditCustomerTab is None, clears the values of the idNameLineEditEditCustomerTab,
            firstNameLineEditCustomerTab, lastNameLineEditEditCustomerTab, emailLineEditEditCustomerTab, addressLineEditEditCustomerTab,
            and phoneLineEditEditCustomerTab. Otherwise, sets the values of these QLineEdit widgets based on the corresponding
            data from the currentData of the nameComboBoxEditCustomerTab.

            If an exception occurs, sets the text of the feedbackLabelEditCustomerTab and feedbackLabelAddCustomerTab to the error message.

        """
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
        """
        Handles the "Save Changes" button click event for the Edit Customer tab.

        Attempts to save the changes made to the customer's information by retrieving the input values from the respective
        widgets. Validates that the required fields (first name, last name, email, and phone) are not empty. If the address is
        empty, calls the 'updateCustomerInfoBlankAddress' function, which updates the customer's information without an address.
        Otherwise, calls the 'updateCustomerInfo' function, which updates the customer's information with the provided address.

        Clears the input fields for both the Edit Customer and New Invoice tabs, refreshes the customer comboboxes, and updates
        the feedback label with any error messages.

        """

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
        """
            This method clears the input fields in the Edit Customer tab after successfully editing customer information.

            It clears the nameComboBoxEditCustomerTab, idNameLineEditEditCustomerTab, emailLineEditEditCustomerTab,
            addressLineEditEditCustomerTab, phoneLineEditEditCustomerTab, firstNameLineEditCustomerTab,
            and lastNameLineEditEditCustomerTab.

            It also sets the feedback label in the Edit Customer tab to indicate that customer information has been
            successfully edited.

        """
        self.feedbackLabelEditCustomerTab.setText(f"Customer information successfully edited")
        self.nameComboBoxEditCustomerTab.clear()
        self.idNameLineEditEditCustomerTab.clear()
        self.emailLineEditEditCustomerTab.clear()
        self.addressLineEditEditCustomerTab.clear()
        self.phoneLineEditEditCustomerTab.clear()
        self.firstNameLineEditCustomerTab.clear()
        self.lastNameLineEditEditCustomerTab.clear()

    def invoiceCustomerClear(self):
        """
            Clears the invoice customer information by resetting the values of the following widgets:
            - emailLineEditNewInvoiceTab: a line edit for displaying a customer's email
            - idLineEditNewInvoiceTab: a line edit for displaying a customer's id
            - nameComboBoxNewInvoiceTab: a combobox for selecting a customer's name

            If the nameComboBoxNewInvoiceTab widget exists and has focus, it clears the focus and sets the current index to -1.
            Otherwise, it simply clears the widget.

        """
        self.emailLineEditNewInvoiceTab.clear()
        self.idLineEditNewInvoiceTab.clear()
        print("Before check:", self.nameComboBoxNewInvoiceTab)
        if self.nameComboBoxNewInvoiceTab is not None:
            print("After check:", self.nameComboBoxNewInvoiceTab)
            if self.nameComboBoxNewInvoiceTab.hasFocus():
                self.nameComboBoxNewInvoiceTab.clearFocus()
            self.nameComboBoxNewInvoiceTab.setCurrentIndex(-1)
            self.nameComboBoxNewInvoiceTab.clear()
        else:
            self.nameComboBoxNewInvoiceTab.clear()


    def refreshCustomersComboBoxes(self):
        """
        Refreshes the customer combo boxes by fetching the customer information from the database and updating the
        appropriate combo boxes with the retrieved information. Also connects the appropriate signals to the
        corresponding slots.
        """

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
        """
            Sets up the widgets and connections for the add product tab.

            Initializes and assigns values to several widgets including:
                - productNameLineEditAddProductTab: a line edit for entering the name of the product
                - productGenreLineEditAddProductTab: a line edit for entering the genre of the product
                - productDeveloperLineEditAddProductTab: a line edit for entering the developer of the product
                - productReleaseDateAddProductTab: a date edit for entering the release date of the product
                - productPriceLineEditAddProductTab: a line edit for entering the price of the product
                - vendorNameComboBoxAddProductTab: a combobox for selecting the vendor name of the product
                - vendorIdLineEditAddProductTab: a line edit for displaying the ID of the vendor
                - feedbackLabelAddProductTab: a label for displaying feedback to the user
                - addProductButtonAddProductTab: a button for adding a product to the database

            Sets up the initial values for the vendorNameComboBoxAddProductTab by getting the list of vendors.

            Connects the addProductButtonAddProductTab.clicked signal to addProductButtonAddProductTabClickHandler.

            Returns:
                None
            """
        self.productNameLineEditAddProductTab = self.findChild(QLineEdit, 'productNameLineEditAddProductTab')
        self.productGenreLineEditAddProductTab = self.findChild(QLineEdit, 'productGenreLineEditAddProductTab')
        self.productDeveloperLineEditAddProductTab = self.findChild(QLineEdit, 'productDeveloperLineEditAddProductTab')
        self.productReleaseDateAddProductTab = self.findChild(QDateEdit, 'productReleaseDateAddProductTab')
        self.productPriceLineEditAddProductTab = self.findChild(QLineEdit, 'productPriceLineEditAddProductTab')
        self.startingInventorySpinBoxAddproductTab = self.findChild(QSpinBox, 'startingInventorySpinBoxAddproductTab')
        self.vendorNameComboBoxAddProductTab = self.findChild(QComboBox, 'vendorNameComboBoxAddProductTab')
        self.vendorIdLineEditAddProductTab = self.findChild(QLineEdit, 'vendorIdLineEditAddProductTab')
        self.feedbackLabelAddProductTab = self.findChild(QLabel, 'feedbackLabelAddProductTab')
        self.addProductButtonAddProductTab = self.findChild(QPushButton, 'addProductButtonAddProductTab')
        self.addProductButtonAddProductTab.clicked.connect(self.addProductButtonAddProductTabClickHandler)
        vendors = getAllVendors()
        self.vendorIdLineEditAddProductTab.setText(str(vendors[0][0]))
        for row in vendors:
            self.vendorNameComboBoxAddProductTab.addItem(row[1], userData=[row[0]])
        self.vendorNameComboBoxAddProductTab.currentIndexChanged.connect(self.vendorNameComboBoxAddProductTabCurrentIndexChangedHandler)

    def vendorNameComboBoxAddProductTabCurrentIndexChangedHandler(self):
        """
            Event handler for the vendorNameComboBoxAddProductTab combobox's currentIndexChanged signal.

            Gets the selected vendor's id from the combobox's userData and sets it to the vendorIdLineEditAddProductTab line edit.

            """
        try:
            vendorId = self.vendorNameComboBoxAddProductTab.currentData()[0]
            self.vendorIdLineEditAddProductTab.setText(str(vendorId))
        except Exception as e:
            print(e)

    def addProductButtonAddProductTabClickHandler(self):
        """
            Handles the event when the user clicks the 'Add Product' button in the 'Add Product' tab.

            Retrieves the values of the product name, genre, developer, release date, price, and vendor ID from their respective
            widgets in the UI. Converts the price to a float, and then checks that all fields are non-empty. If any of these
            operations fail, the error message is displayed in the feedback label.

            If all fields are valid, the `addProduct` function is called with the retrieved values, and a success message is
            displayed in the feedback label. The 'Add Product' tab is then cleared, and the list of products in the 'View
            Products' tab is refreshed.

        """
        try:
            prod_name = self.productNameLineEditAddProductTab.text()
            genre = self.productGenreLineEditAddProductTab.text()
            dev = self.productDeveloperLineEditAddProductTab.text()
            release = self.productReleaseDateAddProductTab.date().toString('yyyy-MM-dd')
            inventory = self.startingInventorySpinBoxAddproductTab.text()
            try:
                price = self.productPriceLineEditAddProductTab.text()
                price_float = float(price)
            except ValueError:
                self.feedbackLabelAddProductTab.setText(str(e))
            vendor_id = self.vendorIdLineEditAddProductTab.text()
            assert all(field != '' for field in [prod_name, genre, dev, release, price_float, vendor_id, inventory])

            addProduct(prod_name, genre, dev, release, float(price), int(inventory), int(vendor_id) )
            self.feedbackLabelAddProductTab.setText(f"{prod_name} successfully added")
            self.clearAddProducts()
            self.refreshProducts()
        except Exception as e:
            print(str(e))
            self.feedbackLabelAddProductTab.setText(str(e))

    def clearAddProducts(self):
        """
            Clears the text fields in the Add Product tab.

            Clears the following text fields:
                - productNameLineEditAddProductTab
                - productGenreLineEditAddProductTab
                - productDeveloperLineEditAddProductTab
                - productPriceLineEditAddProductTab

        """
        self.productNameLineEditAddProductTab.clear()
        self.productGenreLineEditAddProductTab.clear()
        self.productDeveloperLineEditAddProductTab.clear()
        self.productPriceLineEditAddProductTab.clear()
##########################################################################################################################


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
        self.quantitySpinBoxManageInventoryTab = self.findChild(QSpinBox, 'quantitySpinBoxManageInventoryTab')
        self.saveChangesButtonManageInventoryTab = self.findChild(QPushButton, 'saveChangesButtonManageInventoryTab')
        self.saveChangesButtonManageInventoryTab.clicked.connect(self.saveChangesButtonManageInventoryTabClickHandler)
        products = getProducts()
        self.newProductNameLineEditManageInventoryTab.setText(products[0][1])
        self.newProductGenreLineEditManageInventoryTab.setText(products[0][2])
        self.newProductDeveloperLineEditManageInventoryTab.setText(products[0][3])
        self.newProductReleaseDateManageInventoryTab.setDate(products[0][4])
        self.newProductPriceLineEditManageInventoryTab.setText(str(products[0][5]))
        self.productIdLineEditManageInventoryTab.setText(str(products[0][0]))
        self.quantitySpinBoxManageInventoryTab.setValue(products[0][6])
        for row in products:
            self.productNameComboBoxEditInventoryTab.addItem(str(row[1]), userData=[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
        self.productNameComboBoxEditInventoryTab.currentIndexChanged.connect(self.productNameComboBoxEditInventoryTabCurrentIndexHandler)
        vendors = getAllVendors()
        self.vendorIdLineEditManageInventoryTab.setText(str(vendors[0][0]))
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
            self.newProductPriceLineEditManageInventoryTab.setText(str(row[5]))
            self.quantitySpinBoxManageInventoryTab.setValue(row[6])
        except Exception as e:
            print(e)

    def newVendorNameComboBoxManageInventoryTabCurrentIndexHandler(self):
        try:
            vendorId = self.newVendorNameComboBoxManageInventoryTab.currentData()[0]
            self.vendorIdLineEditManageInventoryTab.setText(str(vendorId))
        except Exception as e:
            print(e)

    def saveChangesButtonManageInventoryTabClickHandler(self):
        try:
            prod_id = self.productIdLineEditManageInventoryTab.text()
            name = self.newProductNameLineEditManageInventoryTab.text()
            genre = self.newProductGenreLineEditManageInventoryTab.text()
            dev = self.newProductDeveloperLineEditManageInventoryTab.text()
            date = self.newProductReleaseDateManageInventoryTab.date()
            release_date = f"{date.year()}-{date.month()}-{date.day()}"
            price = self.newProductPriceLineEditManageInventoryTab.text()
            vendor = self.vendorIdLineEditManageInventoryTab.text()
            inventory = self.quantitySpinBoxManageInventoryTab.value()
            updateProduct(prod_id, name, genre, dev, release_date, price, inventory, vendor)
            self.refreshProducts()
        except Exception as e:
            print(e)

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
            self.feedbackLabelAddVendorTab.setText(f"{vendor_name} successfully added")
            self.vendorNameLineEditAddVendorTab.clear()
        except Exception as e:
            self.feedbackLabelAddVendorTab.setText(e)

    def editVendorWidgetSetup(self):
        self.vendorNameComboBoxEditVendorTab = self.findChild(QComboBox, 'vendorNameComboBoxEditVendorTab')
        self.newVendorNameLineEditEditVendorTab = self.findChild(QLineEdit, 'newVendorNameLineEditEditVendorTab')
        self.vendorIdLineEditEditVendorTab = self.findChild(QLineEdit, 'vendorIdLineEditEditVendorTab')
        self.feedbackLabelEditVendorTab = self.findChild(QLabel, 'feedbackLabelEditVendorTab')
        self.saveChangesButtonEditVendorTab = self.findChild(QPushButton, 'saveChangesButtonEditVendorTab')
        self.saveChangesButtonEditVendorTab.clicked.connect(self.saveChangesButtonEditVendorTabClickHandler)
        vendors = getAllVendors()
        self.newVendorNameLineEditEditVendorTab.setText(vendors[0][1])
        self.vendorIdLineEditEditVendorTab.setText(str(vendors[0][0]))
        for row in vendors:
            self.vendorNameComboBoxEditVendorTab.addItem(str(row[1]), userData=[row[0], row[1]])
        self.vendorNameComboBoxEditVendorTab.currentIndexChanged.connect(
            self.vendorNameComboBoxEditVendorTabCurrentIndexChangedHandler)

    def vendorNameComboBoxEditVendorTabCurrentIndexChangedHandler(self):
        try:
            self.newVendorNameLineEditEditVendorTab.setText(self.vendorNameComboBoxEditVendorTab.currentData()[1])
            self.vendorIdLineEditEditVendorTab.setText(str(self.vendorNameComboBoxEditVendorTab.currentData()[0]))
        except Exception as e:
            print(e)

    def saveChangesButtonEditVendorTabClickHandler(self):
        vendor_name = self.newVendorNameLineEditEditVendorTab.text()
        vendor_id = int(self.vendorIdLineEditEditVendorTab.text())
        updateVendor(vendor_id, vendor_name)
        self.feedbackLabelEditVendorTab.setText(f"{vendor_name} successfully edited")
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
        products = getProducts()
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
        games = getProducts()
        for row in games:
            self.productComboBoxShipmentsTab.addItem(row[1], userData=[row[0], row[5]])
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
            self.feedbackLabelShipmentsTab.clear()
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
                        cellData = QTableWidgetItem(str(self.shipmentList[curKey][numColumn - 1]))
                        self.shipmentListTableWidgetShipmentsTab.setItem(numRow, numColumn, cellData)
        except Exception as e:
            print(e)

    def submitButtonShipmentsTabClickHandler(self):
        try:
            for productID, productInfo in self.shipmentList.items():
                adjustStock(productID, productInfo[1])
            self.shipmentList = {}
            self.displayShipmentList()
            self.refreshProductTables()
            self.feedbackLabelShipmentsTab.setText("Shipment Received!")
        except Exception as e:
            print(e)

    def randomShipmentButtonShipmentsTabClickHandler(self):
        try:
            product_list = getProducts()
            attempts = randint(1, len(product_list) * randint(1, 2))
            for products in range(attempts):
                list_id = randint(0, len(product_list) - 1)
                product_id = list_id + 1
                if product_id in self.shipmentList.keys():
                    self.shipmentList[product_id][1] += randint(1, 200)
                else:
                    self.shipmentList[product_id] = [product_list[list_id][1], randint(1, 200)]
            self.displayShipmentList()
        except Exception as e:
            print(e)
    def viewWidgetSetup(self):
        self.viewSelectionComboBoxViewTab = self.findChild(QComboBox, 'viewSelectionComboBoxViewTab')
        self.viewTableWidgetViewTab = self.findChild(QTableWidget, 'viewTableWidgetViewTab')
        self.viewResetToDefault()
        self.viewSelectionComboBoxViewTab.currentIndexChanged.connect(
            self.viewSelectionComboBoxViewTabCurrentIndexChangedHandler)

    def viewResetToDefault(self):
        colNames, data = getAllInventory()
        self.displayInView(colNames, data)

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
        self.viewResetToDefault()

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