import sys 
from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6 import QtTest
# from controller import *

class MainWindow(QMainWindow):
    def __init__(self):
        '''Initializer for the main window'''
        super().__init__()
        uic.loadUi('videoGameStore.ui', self)
        self.newInvoiceWidgetsSetup()

    def newInvoiceWidgetsSetup(self):
        self.nameComboBoxNewInvoiceTab = self.findChild(QComboBox, 'nameComboBoxNewInvoiceTab')
        self.emailLineEditNewInvoiceTab = self.findChild(QLineEdit, 'emailLineEditNewInvoiceTab')
        self.idLineEditNewInvoiceTab = self.findChild(QLineEdit, 'idLineEditNewInvoiceTab')
        self.productComboBoxNewInvoiceTab = self.findChild(QComboBox, 'productComboBoxNewInvoiceTab')
        self.productNumberSpinBoxNewInvoiceTab = self.findChild(QSpinBox, 'productNumberSpinBoxNewInvoiceTab')
        self.addProductButtonNewInvoiceTab = self.findChild(QPushButton, 'addProductButtonNewInvoiceTab')
        self.removeProductButtonNewInvoiceTab = self.findChild(QPushButton, 'removeProductButtonNewInvoiceTab')
        self.purchaseButtonNewInvoiceTab = self.findChild(QPushButton, 'purchaseButtonNewInvoiceTab')
        self.invoiceListTableWidgetNewInvoiceTab = self.findChild(QTableWidget, 'invoiceListTableWidgetNewInvoiceTab')
        self.invoiceTotalLineEditNewInvoiceTab = self.findChild(QLineEdit, 'invoiceTotalLineEditNewInvoiceTab')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

