from sqltesting import *
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        """
        Initializes the main window of the application and sets up the UI, widgets,
        as well as initializes data for the information being displayed.
        """
        super().__init__()
        uic.loadUi('videoGameStore.ui', self)
        self.newInvoiceWidgetSetup()

    def newInvoiceWidgetSetup(self):
        self.nameComboBoxNewInvoiceTab = self.findChild(QComboBox, 'nameComboBoxNewInvoiceTab')
        self.emailLineNewInvoiceTab = self.findChild(QLineEdit, 'emailLineEditNewInvoiceTab')
        self.idLineEditNewInvoiceTab = self.findChild(QLineEdit, 'idLineEditNewInvoiceTab')
        self.productComboBoxNewInvoiceTab = self.findChild(QComboBox, 'productComboBoxNewInvoiceTab')
        self.productNumberSpinBoxNewInvoiceTab = self.findChild(QSpinBox, 'productNumberSpinBoxNewInvoiceTab')
        self.invoiceTotalLineEditNewInvoiceTab = self.findChild(QLineEdit, 'invoiceTotalLineEditNewInvoiceTab')
        self.invoiceListTableWidgetNewInvoiceTab = self.findChild(QTableWidget, 'invoiceListTableWidgetNewInvoiceTab')
        self.addProductButtonNewInvoiceTab = self.findChild(QPushButton, 'addProductButtonNewInvoiceTab')
       # self.addProductButtonNewInvoiceTab.clicked.connect(self.addProductButtonNewInvoiceTabClickHandler)
        self.removeProductButtonNewInvoiceTab = self.findChild(QPushButton, 'removeProductButtonNewInvoiceTab')
        #self.removeProductButtonNewInvoiceTab.clicked.connect(self.removeProductButtonNewInvoiceTabClickHandler)
        self.purchaseButtonNewInvoiceTab = self.findChild(QPushButton, 'purchasebutton')
        #self.purchaseButtonNewInvoiceTab.clicked.connect(purchaseButtonNewInvoiceTabClickHandler)
        customers = getCustomerNames()
        games = getProductNames()
        for name in customers:
            self.nameComboBoxNewInvoiceTab.addItem(str(name))
        self.nameComboBoxNewInvoiceTab.currentIndexChanged.connect(self.nameComboBoxNewInvoiceTabCurrentIndexChangedHandler)
        for game in games:
            self.productComboBoxNewInvoiceTab.addItem(str(game))


    def nameComboBoxNewInvoiceTabCurrentIndexChangedHandler(self):
        try:
            custName = self.nameComboBoxNewInvoiceTab.currentText()
            info = getCustByName(custName)
            self.emailLineNewInvoiceTab.setText(info['email'])
            self.idLineEditNewInvoiceTab.setText(str(info['customer_id']))
        except Exception as e:
            print(e)

   # def addProductButtonNewInvoiceTabClickHandler(self):
   #     try:
   #         prodName = self.productComboBoxNewInvoiceTab.currentText()
   #         info = getGameInfoByName(prodName)







if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
