# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Modules/ui/rang.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 480)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.team_1_tableWidget = QtWidgets.QTableWidget(self.widget)
        self.team_1_tableWidget.setObjectName("team_1_tableWidget")
        self.team_1_tableWidget.setColumnCount(0)
        self.team_1_tableWidget.setRowCount(0)
        self.horizontalLayout.addWidget(self.team_1_tableWidget)
        self.team_2_tableWidget = QtWidgets.QTableWidget(self.widget)
        self.team_2_tableWidget.setObjectName("team_2_tableWidget")
        self.team_2_tableWidget.setColumnCount(0)
        self.team_2_tableWidget.setRowCount(0)
        self.horizontalLayout.addWidget(self.team_2_tableWidget)
        self.verticalLayout.addWidget(self.widget)
        self.win_name_label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.win_name_label.setFont(font)
        self.win_name_label.setStyleSheet("color: rgb(239, 41, 41);")
        self.win_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.win_name_label.setObjectName("win_name_label")
        self.verticalLayout.addWidget(self.win_name_label)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Ранги"))
        self.win_name_label.setText(_translate("Dialog", "Победитель"))
