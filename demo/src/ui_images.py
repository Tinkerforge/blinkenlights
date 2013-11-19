# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/images.ui'
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

class Ui_Images(object):
    def setupUi(self, Images):
        Images.setObjectName(_fromUtf8("Images"))
        Images.resize(541, 275)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Images)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Images)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.line = QtGui.QFrame(Images)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.button_choose = QtGui.QPushButton(Images)
        self.button_choose.setObjectName(_fromUtf8("button_choose"))
        self.verticalLayout_2.addWidget(self.button_choose)
        self.button_show = QtGui.QPushButton(Images)
        self.button_show.setObjectName(_fromUtf8("button_show"))
        self.verticalLayout_2.addWidget(self.button_show)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.text_edit_files = QtGui.QTextEdit(Images)
        self.text_edit_files.setObjectName(_fromUtf8("text_edit_files"))
        self.horizontalLayout.addWidget(self.text_edit_files)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(Images)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.slider_speed = QtGui.QSlider(Images)
        self.slider_speed.setMinimum(10)
        self.slider_speed.setMaximum(10000)
        self.slider_speed.setProperty("value", 1000)
        self.slider_speed.setTracking(True)
        self.slider_speed.setOrientation(QtCore.Qt.Horizontal)
        self.slider_speed.setObjectName(_fromUtf8("slider_speed"))
        self.horizontalLayout_3.addWidget(self.slider_speed)
        self.spinbox_speed = QtGui.QSpinBox(Images)
        self.spinbox_speed.setMinimum(10)
        self.spinbox_speed.setMaximum(10000)
        self.spinbox_speed.setProperty("value", 1000)
        self.spinbox_speed.setObjectName(_fromUtf8("spinbox_speed"))
        self.horizontalLayout_3.addWidget(self.spinbox_speed)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Images)
        QtCore.QMetaObject.connectSlotsByName(Images)

    def retranslateUi(self, Images):
        Images.setWindowTitle(_translate("Images", "Form", None))
        self.label.setText(_translate("Images", "Einführungstext", None))
        self.button_choose.setText(_translate("Images", "Choose images...", None))
        self.button_show.setText(_translate("Images", "Show images", None))
        self.label_2.setText(_translate("Images", "Speed (ms):", None))

