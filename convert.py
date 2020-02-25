import dis


"""parser: 根据字符串解析出codeobject
Keyword arguments:
argument 源代码字符串
Return: 包含codeobject属性的字典
"""

def parser(source):
    bytecode = dis.Bytecode(source)
    instructions = list(bytecode)

    codeobject = bytecode.codeobj
    # 获取常量表和变量名表
    consts = codeobject.co_consts
    names = codeobject.co_names

    codeinfo = {
        "consts": consts,
        "names": names,
        "instructions": instructions
    }

    return codeinfo




if __name__ == "__main__":
    source = """
a = 1
b = 2
c = a + b
    """
    res = parser(source)
    print(res)