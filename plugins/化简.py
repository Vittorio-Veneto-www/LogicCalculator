TYPE = "List"
NAME = "化简"

def braket(x):
    return x if len(x) == 1 else ['('] + x + [')']

variablep = None

def convert(expressions):
    exp = expressions.pop()
    if exp == '0' or exp == '1':
        return ([exp],)
    elif exp in variablep:
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
    exp = expressions.pop()
    if exp == '0' or exp == '1':
        return ([exp],)
    elif exp in variablep:
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

def exec(expressions, variablepos, PostfixExpression):
    if not expressions:
        return []
    global variablep
    variablep = variablepos
    result1 = convert(PostfixExpression(expressions).copy())
    result2 = convert1(PostfixExpression(result1[0].copy()))
    return [result1[0], result2[0]]