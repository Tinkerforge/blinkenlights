# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/text.ui'
#
# Created: Tue Nov 19 18:33:46 2013
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Text(object):
    def setupUi(self, Text):
        Text.setObjectName(_fromUtf8("Text"))
        Text.resize(541, 275)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Text)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Text)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.line = QtGui.QFrame(Text)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_4 = QtGui.QLabel(Text)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_4.addWidget(self.label_4)
        self.radio_rainbow = QtGui.QRadioButton(Text)
        self.radio_rainbow.setChecked(True)
        self.radio_rainbow.setObjectName(_fromUtf8("radio_rainbow"))
        self.horizontalLayout_4.addWidget(self.radio_rainbow)
        self.radio_color = QtGui.QRadioButton(Text)
        self.radio_color.setObjectName(_fromUtf8("radio_color"))
        self.horizontalLayout_4.addWidget(self.radio_color)
        self.label_color = QtGui.QLabel(Text)
        self.label_color.setObjectName(_fromUtf8("label_color"))
        self.horizontalLayout_4.addWidget(self.label_color)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.button_pick = QtGui.QPushButton(Text)
        self.button_pick.setObjectName(_fromUtf8("button_pick"))
        self.horizontalLayout_4.addWidget(self.button_pick)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(Text)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.slider_speed = QtGui.QSlider(Text)
        self.slider_speed.setMinimum(10)
        self.slider_speed.setMaximum(100)
        self.slider_speed.setProperty("value", 40)
        self.slider_speed.setTracking(True)
        self.slider_speed.setOrientation(QtCore.Qt.Horizontal)
        self.slider_speed.setObjectName(_fromUtf8("slider_speed"))
        self.horizontalLayout_3.addWidget(self.slider_speed)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtGui.QLabel(Text)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.edit_text = QtGui.QLineEdit(Text)
        self.edit_text.setObjectName(_fromUtf8("edit_text"))
        self.horizontalLayout.addWidget(self.edit_text)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Text)
        QtCore.QMetaObject.connectSlotsByName(Text)

    def retranslateUi(self, Text):
        Text.setWindowTitle(_translate("Text", "Form", None))
        self.label.setText(_translate("Text", "Einführungstext", None))
        self.label_4.setText(_translate("Text", "Color:", None))
        self.radio_rainbow.setText(_translate("Text", "Rainbow", None))
        self.radio_color.setText(_translate("Text", "Color", None))
        self.label_color.setText(_translate("Text", "(255, 0, 0)", None))
        self.button_pick.setText(_translate("Text", "Pick Color", None))
        self.label_2.setText(_translate("Text", "Speed:", None))
        self.label_3.setText(_translate("Text", "Text:", None))
        self.edit_text.setText(_translate("Text", "Starter Kit: Blinkenlights", None))

