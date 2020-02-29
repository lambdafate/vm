import instype
import dis

# 字节码

class Instruction(object):
    def __init__(self, opname, arg):
        self.opname = opname
        self.arg      = arg
        self.HAVEARG  = True if dis.opmap.get(opname, -1) >= dis.HAVE_ARGUMENT else False
        # 判断字节码参数类型
        self.argtype  = instype.what_the_fuck_are_args(self.opname)
    def __str__(self):
        return f"<Bytecode: {self.opname}, {self.arg}>"
    __repr__ = __str__