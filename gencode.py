def gencode_argtype():
    argtypes = ["hascompare", "hasconst", "hasfree",
               "hasname", "hasjrel", "hasjabs", "haslocal"]

    # 字节码类型
    print("import dis")
    ARGTYPES = """ARGTYPE_{} = {}"""
    for index, argtype in enumerate(argtypes):
        print(ARGTYPES.format(argtype[3:].upper(), index))
    print(ARGTYPES.format("OTHER", len(argtypes)))

    # 产生字节码类型判断函数
    init = """
def {}(bytecode):
    bytecode = bytecode if isinstance(bytecode, int) else dis.opmap.get(bytecode)
    return bytecode in dis.{}
    """
    for argtype in argtypes:
        print(init.format("is"+argtype[3:], argtype)) 

    funcname = "what_the_fuck_are_args"
    whatareyou = """
def {}(bytecode):
        {}
    """
    temp = """
    if is{}(bytecode):
        return ARGTYPE_{}
    """
    body = ""
    for argtype in argtypes:
        body += temp.format(argtype[3:], argtype[3:].upper())
    body += "return ARGTYPE_OTHER"
    print(whatareyou.format(funcname, body))

if __name__ == "__main__":
    import sys
    with open("./instype.py", "w", encoding="utf8") as f:
        sys.stdout = f
        gencode_argtype()
