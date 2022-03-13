import os, sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

ops = {'¬':3, '∧':2, '∨':2, '→':1, '↔':1, '(':0, ')':0, '()':0}
valid_ops = {'¬', '∧', '∨', '→', '↔', '('}
pluginModules = []
displays = []

def BrowsePlugins():
    os.startfile(os.path.join(os.path.dirname(__file__), "plugins"))

def LoadPlugins():
    PATH = os.path.join(os.path.dirname(__file__), "plugins")
    if not os.path.exists(PATH):
        return
    pluginList = []
    for f in os.listdir(PATH):
        if os.path.isfile(os.path.join(PATH, f)) and f.endswith(".py"):
            pluginList.append(os.path.join(PATH, f))
    import importlib.util
    for pluginPath in pluginList:
        spec = importlib.util.spec_from_file_location("plugins", pluginPath)
        plugin = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plugin)
        if plugin.TYPE == "Text":
            displays.append(QTextBrowser())
        elif plugin.TYPE == "List":
            displays.append(QListView())
            displays[-1].setModel(QStandardItemModel())
        elif plugin.TYPE == "Table":
            displays.append(QTableView())
            displays[-1].setModel(QStandardItemModel())
        ui.tabWidget.addTab(displays[-1], plugin.NAME)
        pluginModules.append(plugin)

def Update():
    if not pluginModules:
        return
    index = ui.tabWidget.currentIndex()
    result = pluginModules[index].exec(data.expressions, data.variablepos, PostfixExpression)
    if pluginModules[index].TYPE == "Text":
        displays[index].setText(result)
    elif pluginModules[index].TYPE == "List":
        model = QStandardItemModel()
        for row in range(len(result)):
            model.setItem(row, 0, QStandardItem(" ".join(result[row])))
        displays[index].setModel(model)
    elif pluginModules[index].TYPE == "Table":
        hLabels, vLabels, table = result
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(hLabels)
        model.setVerticalHeaderLabels(vLabels)
        for row in range(len(vLabels)):
            for col in range(len(hLabels)):
                model.setItem(row, col, QStandardItem(table[row][col]))
                model.item(row, col).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = QFont()
                font.setPointSize(10)
                model.item(row, col).setFont(font)
        displays[index].setModel(model)
        displays[index].horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        displays[index].show()

def SetText(text):
    ui.textBrowser.setText(text)

def CheckButtonState(data):
    ui.undo.setEnabled(data.undoFlag)
    ui.backspace.setEnabled(data.backspaceFlag)
    ui.redo.setEnabled(data.redoFlag)

def PostfixExpression(revexp):
    revexp = revexp.copy()
    revexp.reverse()
    convert_list, op_stack = [], []
    for exp in revexp:
        if exp in ops:
            if exp == ')':
                op_stack.append(exp)
            elif exp == '(':
                while True:
                    op = op_stack.pop()
                    if op ==')':
                        break
                    convert_list.append(op)
                convert_list.append('()')
            elif exp == '¬':
                convert_list.append(exp)
            else:
                while op_stack and ops[op_stack[-1]] > ops[exp]:
                    convert_list.append(op_stack.pop())
                op_stack.append(exp)
        else:
            convert_list.append(exp)
    while op_stack:
        convert_list.append(op_stack.pop())
    return convert_list

class data_struct():
    def __init__(self, expressions = []):
        self.expressions = expressions
        self.variabledict = {}
        self.variablepos = {}
        for exp in expressions:
            if not exp in ops and exp != '0' and exp != '1':
                if exp in self.variabledict:
                    self.variabledict[exp] += 1
                else:
                    self.variabledict[exp] = 1
                    self.variablepos[exp] = len(self.variablepos)
        self.cursor = len(self.expressions)
        self.table = []
        self.expressions.insert(self.cursor, '_')
        self.ExpressionToText()
        self.expressions.pop(self.cursor)
        self.undoFlag = expressions != []
        self.backspaceFlag = expressions != []
        self.redoFlag = False
        CheckButtonState(self)
        self.redolist = []
    
    def ExpressionToText(self):
        SetText(" ".join(self.expressions))
    
    def add_exp(self, exp, flag = True):
        self.undoFlag = True
        self.backspaceFlag = True
        if flag:
            self.redoFlag = True
            self.redolist = []
        CheckButtonState(self)
        if self.expressions:
            if exp == '(':
                if self.expressions[self.cursor - 1] in valid_ops:
                    self.expressions.insert(self.cursor, ')')
                    self.expressions.insert(self.cursor, '(')
                    self.cursor += 1
            elif exp == ')':
                if self.cursor < len(self.expressions) and self.expressions[self.cursor - 1] != '(':
                    self.cursor += 1
            elif exp == '¬':
                if self.expressions[self.cursor - 1] in valid_ops:
                    self.expressions.insert(self.cursor, exp)
                    self.cursor += 1
            elif exp in ops:
                if not (self.expressions[self.cursor - 1] in valid_ops):
                    self.expressions.insert(self.cursor, exp)
                    self.cursor += 1
            else:
                if self.expressions[self.cursor - 1] in valid_ops:
                    if exp != '0' and exp != '1':
                        if exp in self.variabledict:
                            self.variabledict[exp] += 1
                        else:
                            self.variabledict[exp] = 1
                            self.variablepos[exp] = len(self.variablepos)
                    self.expressions.insert(self.cursor, exp)
                    self.cursor += 1
                    Update()
        else:
            if exp == '(':
                self.expressions.insert(self.cursor, ')')
                self.expressions.insert(self.cursor, '(')
                self.cursor += 1
            elif exp == ')':
                pass
            elif exp == '¬':
                self.expressions.insert(self.cursor, exp)
                self.cursor += 1
            elif exp in ops:
                pass
            else:
                if exp != '0' and exp != '1':
                    if exp in self.variabledict:
                        self.variabledict[exp] += 1
                    else:
                        self.variabledict[exp] = 1
                        self.variablepos[exp] = len(self.variablepos)
                self.expressions.insert(self.cursor, exp)
                self.cursor += 1
                Update()
        self.expressions.insert(self.cursor, '_')
        self.ExpressionToText()
        self.expressions.pop(self.cursor)
    
    def undo(self):
        if self.expressions:
            self.cursor -= 1
            exp = self.expressions[self.cursor]
            if exp != ')':
                self.expressions.pop(self.cursor)
            if exp == '(':
                self.expressions.pop(self.cursor)
            if not (exp in ops or exp == '0' or exp == '1'):
                self.variabledict[exp] -= 1
                if not self.variabledict[exp]:
                    del(self.variabledict[exp])
                    del(self.variablepos[exp])
            if self.cursor:
                if not (self.expressions[self.cursor - 1] in valid_ops):
                    Update()
            else:
                Update()
        
        self.expressions.insert(self.cursor, '_')
        self.ExpressionToText()
        self.expressions.pop(self.cursor)
        self.redoFlag = True
        self.redolist.append(exp)
        CheckButtonState(self)
    
    def redo(self):
        self.add_exp(self.redolist.pop(), False)
        self.redoFlag = self.redolist != []
        CheckButtonState(self)

def ui_setup():
    Update()
    ui.tabWidget.currentChanged.connect(Update)

    def confirm_input():
        var = ui.varinput.toPlainText()
        data.add_exp(var)
    
    class inputmedia():
        def __init__(self, exp):
            self.exp = exp
        
        def input(self):
            data.add_exp(self.exp)

    medias = []
    ui.confirm.clicked.connect(confirm_input)
    medias.append(inputmedia("∧"))
    ui.conjunction.clicked.connect(medias[-1].input)
    medias.append(inputmedia("∨"))
    ui.disjunction.clicked.connect(medias[-1].input)
    medias.append(inputmedia("¬"))
    ui.negative.clicked.connect(medias[-1].input)
    medias.append(inputmedia("→"))
    ui.implication.clicked.connect(medias[-1].input)
    medias.append(inputmedia("↔"))
    ui.biconditional.clicked.connect(medias[-1].input)
    medias.append(inputmedia("("))
    ui.leftbracket.clicked.connect(medias[-1].input)
    medias.append(inputmedia(")"))
    ui.rightbracket.clicked.connect(medias[-1].input)
    medias.append(inputmedia("0"))
    ui.fast_0.clicked.connect(medias[-1].input)
    medias.append(inputmedia("1"))
    ui.fast_1.clicked.connect(medias[-1].input)
    medias.append(inputmedia("a"))
    ui.fast_a.clicked.connect(medias[-1].input)
    medias.append(inputmedia("b"))
    ui.fast_b.clicked.connect(medias[-1].input)
    medias.append(inputmedia("c"))
    ui.fast_c.clicked.connect(medias[-1].input)
    medias.append(inputmedia("p"))
    ui.fast_p.clicked.connect(medias[-1].input)
    medias.append(inputmedia("q"))
    ui.fast_q.clicked.connect(medias[-1].input)
    medias.append(inputmedia("r"))
    ui.fast_r.clicked.connect(medias[-1].input)
    ui.undo.triggered.connect(data.undo)
    ui.redo.triggered.connect(data.redo)
    ui.backspace.triggered.connect(data.undo)

    def instruction():
        x = QWidget()
        QMessageBox.information(x, "", "使用指南:\n本计算器可以实现计算逻辑表达式的真值表，主析取/合取范式" +
            "以及自动化简\n为了保证逻辑运算式的正确性，只能通过提供的键盘进行输入，下划线为光标，代表表达式当" +
            "前的输入位置；点击abcpqr可以快速输入对应自由变量，也可以通过输入框输入任意字符串作为自由变量；" +
            "此外还提供逻辑运算符的快速输入\n请注意本程序没有对表达式的编辑功能，若想修改请使用撤销、" +
            "重做和退格进行编辑操作", QMessageBox.Yes)
    ui.instruction.triggered.connect(instruction)

    MainWindow.show()
    sys.exit(app.exec_())

def run():
    global app, MainWindow, ui, data
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    # import compileUi
    import gui
    ui = gui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    LoadPlugins()
    
    initalList = ['(', 'a', '→', 'b', '∨', 'b', ')' ,'∧', 'c']
    data = data_struct(initalList)

    ui_setup()

if __name__ == '__main__':
    run()