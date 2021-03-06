import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class data_struct():

    global ui

    def __init__(self, expressions = []):
        self.ops = {'¬':3, '∧':2, '∨':2, '→':1, '↔':1, '(':0, ')':0, '()':0}
        self.expressions = expressions
        self.variabledict = {}
        self.variablepos = {}
        for exp in expressions:
            if not exp in self.ops and exp != '0' and exp != '1':
                if exp in self.variabledict:
                    self.variabledict[exp] += 1
                else:
                    self.variabledict[exp] = 1
                    self.variablepos[exp] = len(self.variablepos)
        self.cursor = len(self.expressions)
        self.table = []
        self.expressions.insert(self.cursor, '_')
        ui.textBrowser.setText(" ".join(self.expressions))
        self.expressions.pop(self.cursor)
        ui.undo.setEnabled(expressions != [])
        ui.backspace.setEnabled(expressions != [])
        ui.redo.setEnabled(False)
        self.redolist = []
        ui.display1.setModel(QStandardItemModel())
        ui.display2.clear()
        ui.display3.clear()
        ui.display4.setModel(QStandardItemModel())
        if self.expressions:
            self.tablecalc()
    
    def add_exp(self, exp, flag = True):
        ui.undo.setEnabled(True)
        ui.backspace.setEnabled(True)
        if flag:
            ui.redo.setEnabled(False)
            self.redolist = []
        valid_ops = {'¬', '∧', '∨', '→', '↔', '('}
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
            elif exp in self.ops:
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
                    self.tablecalc()
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
            elif exp in self.ops:
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
                self.tablecalc()
        self.expressions.insert(self.cursor, '_')
        ui.textBrowser.setText(" ".join(self.expressions))
        self.expressions.pop(self.cursor)
    
    def undo(self):
        valid_ops = {'¬', '∧', '∨', '→', '↔', '('}
        if self.expressions:
            self.cursor -= 1
            exp = self.expressions[self.cursor]
            if exp != ')':
                self.expressions.pop(self.cursor)
            if exp == '(':
                self.expressions.pop(self.cursor)
            if not (exp in self.ops or exp == '0' or exp == '1'):
                self.variabledict[exp] -= 1
                if not self.variabledict[exp]:
                    del(self.variabledict[exp])
                    del(self.variablepos[exp])
            if self.cursor:
                if not (self.expressions[self.cursor - 1] in valid_ops):
                    self.tablecalc()
            else:
                lst = self.redolist
                self.__init__()
                ui.redo.setEnabled(True)
                self.redolist = lst
        
        self.expressions.insert(self.cursor, '_')
        ui.textBrowser.setText(" ".join(self.expressions))
        self.expressions.pop(self.cursor)
        ui.redo.setEnabled(True)
        self.redolist.append(exp)
    
    def redo(self):
        self.add_exp(self.redolist.pop(), False)
        ui.redo.setEnabled(self.redolist != [])

    def tablecalc(self):

        def reverse_calc(revexp):
            revexp.reverse()
            convert_list, op_stack = [], []
            for exp in revexp:
                if exp in self.ops:
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
                        while op_stack and self.ops[op_stack[-1]] > self.ops[exp]:
                            convert_list.append(op_stack.pop())
                        op_stack.append(exp)
                else:
                    convert_list.append(exp)
            while op_stack:
                convert_list.append(op_stack.pop())
            return convert_list
        
        convert_list = reverse_calc(self.expressions.copy())
        
        def calc(expressions):
            
            nonlocal self

            def printans(x):
                self.table.append(x)
                return x

            exp = expressions.pop()
            if exp == '0' or exp == '1':
                return [exp], [exp == '1' for _ in range(2 ** len(self.variablepos))]
            elif exp in self.variablepos:
                return [exp], [_ & 1 << (len(self.variablepos) - self.variablepos[exp] - 1)\
                    for _ in range(2 ** len(self.variablepos))]
            else:
                if exp == '¬':
                    return printans((lambda x:([exp] + x[0], [not _ for _ in x[1]]))(calc(expressions)))
                elif exp == '()':
                    return (lambda x:(['('] + x[0] + [')'], x[1]))(calc(expressions))
                elif exp == '∧':
                    return printans((lambda x, y:(x[0] + [exp] + y[0], [x[1][_] and y[1][_]\
                        for _ in range(len(x[1]))]))(calc(expressions), calc(expressions)))
                elif exp == '∨':
                    return printans((lambda x, y:(x[0] + [exp] + y[0], [x[1][_] or y[1][_] \
                        for _ in range(len(x[1]))]))(calc(expressions), calc(expressions)))
                elif exp == '→':
                    return printans((lambda x, y:(x[0] + [exp] + y[0], [not x[1][_] or y[1][_]\
                        for _ in range(len(x[1]))]))(calc(expressions), calc(expressions)))
                elif exp == '↔':
                    return printans((lambda x, y:(x[0] + [exp] + y[0], [(not x[1][_] or y[1][_]) and (x[1][_] or not y[1][_])\
                        for _ in range(len(x[1]))]))(calc(expressions), calc(expressions)))

        self.table = []
        for exp in self.variablepos.keys():
            self.table.append(([exp], [_ & 1 << (len(self.variablepos) - self.variablepos[exp] - 1)\
                for _ in range(2 ** len(self.variablepos))]))
        calc(convert_list.copy())
        model=QStandardItemModel()
        model.setHorizontalHeaderLabels([(lambda x:" ".join(x[0]))(_) for _ in self.table])
        model.setVerticalHeaderLabels(["m" + str(_) for _ in range(2 ** len(self.variabledict))])
        for row in range(2 ** len(self.variabledict)):
            for col in range(len(self.table)):
                model.setItem(row, col, QStandardItem("1" if self.table[col][1][row] else "0"))
                model.item(row, col).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = QFont()
                font.setPointSize(10)
                model.item(row, col).setFont(font)
        ui.display1.setModel(model)
        ui.display1.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        ui.display1.show()
        lst = []
        for _ in range(2 ** len(self.variablepos)):
            if self.table[-1][1][_]:
                lst.append("m" + str(_))
        ui.display2.setText(" ∨ ".join(lst))
        lst = []
        for _ in range(2 ** len(self.variablepos)):
            if not self.table[-1][1][_]:
                lst.append("m" + str(_))
        ui.display3.setText(" ∧ ".join(lst))
        
        def braket(x):
            return x if len(x) == 1 else ['('] + x + [')']

        def convert(expressions):
            
            nonlocal self

            exp = expressions.pop()
            if exp == '0' or exp == '1':
                return ([exp],)
            elif exp in self.variablepos:
                return ([exp],)
            else:
                if exp == '¬':
                    return (lambda x:([exp] + x[0],))(convert(expressions))
                elif exp == '()':
                    return (lambda x:(braket(x[0]),))(convert(expressions))
                elif exp == '∧':
                    return (lambda x, y:(braket(x[0]) + [exp] + braket(y[0]),))(convert(expressions), convert(expressions))
                elif exp == '∨':
                    return (lambda x, y:(braket(x[0]) + [exp] + braket(y[0]),))(convert(expressions), convert(expressions))
                elif exp == '→':
                    return (lambda x, y:(['¬'] + braket(x[0]) + ['∨'] + braket(y[0]),))\
                        (convert(expressions), convert(expressions))
                elif exp == '↔':
                    return (lambda x, y:(braket(['¬'] + braket(x[0]) + ['∨'] + braket(y[0])) + ['∧']\
                          + braket(braket(x[0]) + ['∨', '¬'] + braket(y[0])),))(convert(expressions),\
                              convert(expressions))

        def convert1(expressions):
            
            nonlocal self

            exp = expressions.pop()
            if exp == '0' or exp == '1':
                return ([exp],)
            elif exp in self.variablepos:
                return ([exp],)
            else:
                if exp == '¬':
                    return (lambda x:([exp] + x[0],))(convert1(expressions))
                elif exp == '()':
                    return (lambda x:(braket(x[0]),))(convert1(expressions))
                elif exp == '∧':
                    return (lambda x, y:(braket(x[0]) + [exp] + braket(y[0]),))(convert1(expressions), convert1(expressions))
                elif exp == '∨':
                    return (lambda x, y:(['¬'] + braket(['¬'] + braket(x[0]) + ['∧', '¬'] + braket(y[0])),))(convert1(expressions), convert1(expressions))

        result1 = convert(convert_list.copy())
        result2 = convert1(reverse_calc(result1[0].copy()))
        model1=QStandardItemModel()
        model1.setItem(0, 0, QStandardItem(" ".join(result1[0])))
        model1.setItem(1, 0, QStandardItem(" ".join(result2[0])))
        ui.display4.setModel(model1)

class mywindow(QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__(None)

def ui_setup(lst = []):
    global ui
    
    import gui
    app = QApplication(sys.argv)
    MainWindow = mywindow()
    ui = gui.Ui_MainWindow()
    ui.setupUi(MainWindow)

    data = data_struct(lst)

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

if __name__ == '__main__':
    import compileUi
    ui_setup(['(', 'a', '→', 'b', '∨', 'b', ')' ,'∧', 'c'])