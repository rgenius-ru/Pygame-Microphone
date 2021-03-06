# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Modules/ui/results.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(640, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialog.sizePolicy().hasHeightForWidth())
        dialog.setSizePolicy(sizePolicy)
        dialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(dialog)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.text_top_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(76)
        font.setBold(False)
        font.setWeight(50)
        self.text_top_label.setFont(font)
        self.text_top_label.setStyleSheet("color: rgb(239, 41, 41);")
        self.text_top_label.setAlignment(QtCore.Qt.AlignCenter)
        self.text_top_label.setWordWrap(True)
        self.text_top_label.setObjectName("text_top_label")
        self.verticalLayout_2.addWidget(self.text_top_label)
        self.score_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(85)
        font.setBold(False)
        font.setWeight(50)
        self.score_label.setFont(font)
        self.score_label.setStyleSheet("color: rgb(239, 41, 41);")
        self.score_label.setAlignment(QtCore.Qt.AlignCenter)
        self.score_label.setWordWrap(True)
        self.score_label.setObjectName("score_label")
        self.verticalLayout_2.addWidget(self.score_label)
        self.text_bottom_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(76)
        font.setBold(False)
        font.setWeight(50)
        self.text_bottom_label.setFont(font)
        self.text_bottom_label.setStyleSheet("color: rgb(239, 41, 41);")
        self.text_bottom_label.setAlignment(QtCore.Qt.AlignCenter)
        self.text_bottom_label.setWordWrap(True)
        self.text_bottom_label.setObjectName("text_bottom_label")
        self.verticalLayout_2.addWidget(self.text_bottom_label)
        self.verticalLayout.addWidget(self.widget)
        self.dialogButtonBox = QtWidgets.QDialogButtonBox(dialog)
        self.dialogButtonBox.setMinimumSize(QtCore.QSize(0, 120))
        self.dialogButtonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.dialogButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.dialogButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.dialogButtonBox.setCenterButtons(True)
        self.dialogButtonBox.setObjectName("dialogButtonBox")
        self.verticalLayout.addWidget(self.dialogButtonBox)

        self.retranslateUi(dialog)
        self.dialogButtonBox.accepted.connect(dialog.accept)
        self.dialogButtonBox.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "??????????!"))
        self.text_top_label.setText(_translate("dialog", "???? ??????????????"))
        self.score_label.setText(_translate("dialog", "0"))
        self.text_bottom_label.setText(_translate("dialog", "????????????!"))
