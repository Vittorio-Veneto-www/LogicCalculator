# 插件文件中需要包含两个变量，TYPE和NAME
# TYPE为一个字符串，有三种可能的取值，分别是Text,List和Table，三种取值对应了三种不同的返回结果类型
# 如果TYPE为Text，只需返回一个字符串；为List时，需要返回一个由字符串构成的列表
# 为Table时需要返回一个三元组，三元组依次为横向表头，纵向表头和一个由字符串构成的二维表格
# 注意表格的形状需要与表头匹配
# NAME为一个字符串，代表了计算器中显示的选项卡名

TYPE = "Text"
NAME = "example"

# 插件中需要包含一个exec方法，需要有三个参数
# 依次为一个列表，代表表达式；一个字典，代表表达式中的变量的出现序号；一个函数，用来将表达式列表转换为后缀表达式
# 返回值的要求在上面已经说明

def exec(expressions, variablepos, PostfixExpression):
    return " ".join(expressions)