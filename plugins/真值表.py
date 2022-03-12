TYPE = "Table"
NAME = "真值表"

def TableCalc(variablepos, convert_list):        
    def calc(expressions):

        def printans(x):
            table.append(x)
            return x

        exp = expressions.pop()
        if exp == '0' or exp == '1':
            return [exp], [exp == '1' for _ in range(2 ** len(variablepos))]
        elif exp in variablepos:
            return [exp], [_ & 1 << (len(variablepos) - variablepos[exp] - 1)\
                for _ in range(2 ** len(variablepos))]
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

    table = []
    for exp in variablepos.keys():
        table.append(([exp], [_ & 1 << (len(variablepos) - variablepos[exp] - 1)\
            for _ in range(2 ** len(variablepos))]))
    calc(convert_list)
    return table

def exec(expressions, variablepos, PostfixExpression):
    table = TableCalc(variablepos, PostfixExpression(expressions))
    hLabels, vLabels = [" ".join(_[0]) for _ in table], ["m" + str(_) for _ in range(len(table[0][1]))]
    table = [_[1] for _ in table]
    table1 = [["1" if _[__] else "0" for _ in table] for __ in range(len(vLabels))]
    return (hLabels, vLabels, table1)