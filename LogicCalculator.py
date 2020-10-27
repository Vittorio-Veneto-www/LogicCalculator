import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class data_struct():

    global ui

    def __init__(self, expressions = []):
        self.ops = {'¬':3, '∧':2, '∨':2, '→':1, '↔':1, '(':0, ')':0, '()':0}
        self.expressions = expressions
        self.variableset = set()
        self.variablepos = {}
        for exp in expressions:
            if not exp in self.ops and not (exp in self.variableset) and exp != '0' and exp != '1':
                self.variableset.add(exp)
                self.variablepos[exp] = len(self.variablepos)
        self.cursor = len(self.expressions)
        self.table = []
        self.expressions.insert(self.cursor, '_')
        ui.textBrowser.setText(" ".join(self.expressions))
        self.expressions.pop(self.cursor)
    
    def add_exp(self, exp):
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
                    if not (exp in self.variableset) and exp != '0' and exp != '1':
                        self.variableset.add(exp)
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
                if not (exp in self.variableset) and exp != '0' and exp != '1':
                    self.variableset.add(exp)
                    self.variablepos[exp] = len(self.variablepos)
                self.expressions.insert(self.cursor, exp)
                self.cursor += 1
                self.tablecalc()
        self.expressions.insert(self.cursor, '_')
        ui.textBrowser.setText(" ".join(self.expressions))
        self.expressions.pop(self.cursor)

    def tablecalc(self):
        revexp = self.expressions.copy()
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
        
        def calc(expressions):
            
            nonlocal self

            def printans(x):
                self.table.append(x)
                return x

            exp = expressions.pop()
            if exp == '0' or exp == '1':
                return [exp], [exp == '1' for _ in range(2 ** len(self.variablepos))], [exp]
            elif exp in self.variablepos:
                return [exp], [_ & 1 << (len(self.variablepos) - self.variablepos[exp] - 1)\
                    for _ in range(2 ** len(self.variablepos))], [exp]
            else:
                if exp == '¬':
                    return printans((lambda x:([exp] + x[0], [not _ for _ in x[1]], [exp] + x[2]))(calc(expressions)))
                elif exp == '()':
                    return (lambda x:(['('] + x[0] + [')'], x[1], ['('] + x[2] + [')']))(calc(expressions))
                elif exp == '∧':
                    return printans((lambda x, y:(x[0] + [exp] + y[0], [x[1][_] and y[1][_]\
                        for _ in range(len(x[1]))], x[2] + [exp] + y[2]))(calc(expressions), calc(expressions)))
                elif exp == '∨':
                    return printans((lambda x, y:(x[0] + [exp] + y[0], [x[1][_] or y[1][_] \
                        for _ in range(len(x[1]))], x[2] + [exp] + y[2]))(calc(expressions), calc(expressions)))
                elif exp == '→':
                    return printans((lambda x, y:(x[0] + [exp] + y[0], [not x[1][_] or y[1][_]\
                        for _ in range(len(x[1]))], ['¬'] + x[2] + ['∨'] + y[2]))(calc(expressions), calc(expressions)))
                elif exp == '↔':
                    return printans((lambda x, y:(x[0] + [exp] + y[0], [(not x[1][_] or y[1][_]) and (x[1][_] or not y[1][_])\
                        for _ in range(len(x[1]))], ['(', '¬'] + x[2] + ['∨'] + y[2] + [')', '∧', '('] + x[2] + ['∨', '¬'] + y[2] + [')']))(calc(expressions), calc(expressions)))

        self.table = []
        for exp in self.variablepos.keys():
            self.table.append(([exp], [_ & 1 << (len(self.variablepos) - self.variablepos[exp] - 1)\
                for _ in range(2 ** len(self.variablepos))]))
        result = calc(convert_list)
        model=QStandardItemModel()
        model.setHorizontalHeaderLabels([(lambda x:" ".join(x[0]))(_) for _ in self.table])
        model.setVerticalHeaderLabels(["m" + str(_) for _ in range(2 ** len(self.variableset))])
        for row in range(2 ** len(self.variableset)):
            for col in range(len(self.table)):
                model.setItem(row, col, QStandardItem("1" if self.table[col][1][row] else "0"))
                model.item(row, col).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = QFont()
                font.setPointSize(10)
                model.item(row, col).setFont(font)
        ui.display1.setModel(model)
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
        model1=QStandardItemModel()
        model1.setItem(0, 0, QStandardItem(" ".join(result[2])))
        ui.display4.setModel(model1)

class mywindow(QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__(None)

def ui_setup():
    global ui
    
    import compileUi
    import gui
    app = QApplication(sys.argv)
    MainWindow = mywindow()
    ui = gui.Ui_MainWindow()
    ui.setupUi(MainWindow)

    data = data_struct(['(', 'a', '→', 'b', '∨', 'b', ')' ,'∧', 'c'])
    data.tablecalc()

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

    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    ui_setup()