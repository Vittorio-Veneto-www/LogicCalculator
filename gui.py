# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\VSCode\Python\LogicCalculator\./gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(523, 578)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(523, 578))
        MainWindow.setMaximumSize(QtCore.QSize(523, 578))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.fast_a = QtWidgets.QPushButton(self.centralwidget)
        self.fast_a.setGeometry(QtCore.QRect(10, 80, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.fast_a.setFont(font)
        self.fast_a.setObjectName("fast_a")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 501, 61))
        self.textBrowser.setObjectName("textBrowser")
        self.disjunction = QtWidgets.QPushButton(self.centralwidget)
        self.disjunction.setGeometry(QtCore.QRect(470, 80, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.disjunction.setFont(font)
        self.disjunction.setObjectName("disjunction")
        self.leftbracket = QtWidgets.QPushButton(self.centralwidget)
        self.leftbracket.setGeometry(QtCore.QRect(320, 80, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.leftbracket.setFont(font)
        self.leftbracket.setObjectName("leftbracket")
        self.conjunction = QtWidgets.QPushButton(self.centralwidget)
        self.conjunction.setGeometry(QtCore.QRect(420, 80, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.conjunction.setFont(font)
        self.conjunction.setObjectName("conjunction")
        self.implication = QtWidgets.QPushButton(self.centralwidget)
        self.implication.setGeometry(QtCore.QRect(470, 130, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.implication.setFont(font)
        self.implication.setObjectName("implication")
        self.fast_b = QtWidgets.QPushButton(self.centralwidget)
        self.fast_b.setGeometry(QtCore.QRect(60, 80, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.fast_b.setFont(font)
        self.fast_b.setObjectName("fast_b")
        self.fast_p = QtWidgets.QPushButton(self.centralwidget)
        self.fast_p.setGeometry(QtCore.QRect(10, 130, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.fast_p.setFont(font)
        self.fast_p.setObjectName("fast_p")
        self.negative = QtWidgets.QPushButton(self.centralwidget)
        self.negative.setGeometry(QtCore.QRect(370, 130, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.negative.setFont(font)
        self.negative.setObjectName("negative")
        self.fast_r = QtWidgets.QPushButton(self.centralwidget)
        self.fast_r.setGeometry(QtCore.QRect(110, 130, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.fast_r.setFont(font)
        self.fast_r.setObjectName("fast_r")
        self.fast_q = QtWidgets.QPushButton(self.centralwidget)
        self.fast_q.setGeometry(QtCore.QRect(60, 130, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.fast_q.setFont(font)
        self.fast_q.setObjectName("fast_q")
        self.biconditional = QtWidgets.QPushButton(self.centralwidget)
        self.biconditional.setGeometry(QtCore.QRect(420, 130, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.biconditional.setFont(font)
        self.biconditional.setObjectName("biconditional")
        self.rightbracket = QtWidgets.QPushButton(self.centralwidget)
        self.rightbracket.setGeometry(QtCore.QRect(370, 80, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.rightbracket.setFont(font)
        self.rightbracket.setObjectName("rightbracket")
        self.fast_c = QtWidgets.QPushButton(self.centralwidget)
        self.fast_c.setGeometry(QtCore.QRect(110, 80, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.fast_c.setFont(font)
        self.fast_c.setObjectName("fast_c")
        self.varinput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.varinput.setGeometry(QtCore.QRect(210, 80, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.varinput.setFont(font)
        self.varinput.setObjectName("varinput")
        self.confirm = QtWidgets.QPushButton(self.centralwidget)
        self.confirm.setGeometry(QtCore.QRect(210, 130, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.confirm.setFont(font)
        self.confirm.setObjectName("confirm")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 180, 501, 361))
        self.tabWidget.setObjectName("tabWidget")
        self.fast_0 = QtWidgets.QPushButton(self.centralwidget)
        self.fast_0.setGeometry(QtCore.QRect(160, 80, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.fast_0.setFont(font)
        self.fast_0.setObjectName("fast_0")
        self.fast_1 = QtWidgets.QPushButton(self.centralwidget)
        self.fast_1.setGeometry(QtCore.QRect(160, 130, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.fast_1.setFont(font)
        self.fast_1.setObjectName("fast_1")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 523, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.mode1 = QtWidgets.QAction(MainWindow)
        self.mode1.setCheckable(False)
        self.mode1.setShortcut("")
        self.mode1.setObjectName("mode1")
        self.mode2 = QtWidgets.QAction(MainWindow)
        self.mode2.setObjectName("mode2")
        self.mode3 = QtWidgets.QAction(MainWindow)
        self.mode3.setObjectName("mode3")
        self.mode4 = QtWidgets.QAction(MainWindow)
        self.mode4.setObjectName("mode4")
        self.undo = QtWidgets.QAction(MainWindow)
        self.undo.setObjectName("undo")
        self.redo = QtWidgets.QAction(MainWindow)
        self.redo.setObjectName("redo")
        self.instruction = QtWidgets.QAction(MainWindow)
        self.instruction.setObjectName("instruction")
        self.backspace = QtWidgets.QAction(MainWindow)
        self.backspace.setObjectName("backspace")
        self.menu.addAction(self.undo)
        self.menu.addAction(self.redo)
        self.menu.addSeparator()
        self.menu.addAction(self.backspace)
        self.menu_2.addAction(self.instruction)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LogicCalculator"))
        self.fast_a.setText(_translate("MainWindow", "a"))
        self.disjunction.setText(_translate("MainWindow", "∨"))
        self.leftbracket.setText(_translate("MainWindow", "("))
        self.conjunction.setText(_translate("MainWindow", "∧"))
        self.implication.setText(_translate("MainWindow", "→"))
        self.fast_b.setText(_translate("MainWindow", "b"))
        self.fast_p.setText(_translate("MainWindow", "p"))
        self.negative.setText(_translate("MainWindow", "¬"))
        self.fast_r.setText(_translate("MainWindow", "r"))
        self.fast_q.setText(_translate("MainWindow", "q"))
        self.biconditional.setText(_translate("MainWindow", "↔"))
        self.rightbracket.setText(_translate("MainWindow", ")"))
        self.fast_c.setText(_translate("MainWindow", "c"))
        self.confirm.setText(_translate("MainWindow", "确定"))
        self.fast_0.setText(_translate("MainWindow", "0"))
        self.fast_1.setText(_translate("MainWindow", "1"))
        self.menu.setTitle(_translate("MainWindow", "编辑"))
        self.menu_2.setTitle(_translate("MainWindow", "帮助"))
        self.mode1.setText(_translate("MainWindow", "真值表"))
        self.mode2.setText(_translate("MainWindow", "主析取范式"))
        self.mode3.setText(_translate("MainWindow", "主合取范式"))
        self.mode4.setText(_translate("MainWindow", "化简表达式"))
        self.undo.setText(_translate("MainWindow", "撤销"))
        self.undo.setShortcut(_translate("MainWindow", "Ctrl+Z"))
        self.redo.setText(_translate("MainWindow", "重做"))
        self.redo.setShortcut(_translate("MainWindow", "Ctrl+Shift+Z"))
        self.instruction.setText(_translate("MainWindow", "说明"))
        self.backspace.setText(_translate("MainWindow", "退格"))
        self.backspace.setShortcut(_translate("MainWindow", "Backspace"))
