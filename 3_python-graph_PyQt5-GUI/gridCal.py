'''
	Embedded Communication System
	201701722 KangJunYeong
	2021-03-17 15:36
'''

import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QCoreApplication

formClass = uic.loadUiType("gridCal.ui")[0]

class MainWindow(QtWidgets.QMainWindow, formClass):

    gridbool = 0

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

	# Exit Button
        self.pushExitButton.clicked.connect(QCoreApplication.instance().quit)

	# Label text
        self.testlabel.setText("This represents today's date, month and year!!")

	#text edit
        self.textEdit.setText("Calander")

	# Choose Grid or not
        self.pushGridButton.setText("Grid")
        self.pushGridButton.clicked.connect(self.pushGrid)

    def pushGrid(self):
        if MainWindow.gridbool: # if grid on -> grid off
            MainWindow.gridbool = 0
            self.calendarWidget.setGridVisible(MainWindow.gridbool)
        else: # if grid off -> grid on
            MainWindow.gridbool = 1
            self.calendarWidget.setGridVisible(MainWindow.gridbool)

app = QtWidgets.QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec()
