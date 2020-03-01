# frame

class Frame(object):
    def __init__(self, codeinfo, prev=None, funcname="", globals={}):
        self.codeinfo = codeinfo
        self.prev     = prev
        
        self.funcname = funcname
        self.stack    = []
        self.block_stack = []

        self.pc = 0
        self.instructions = self.codeinfo.get("instructions")
        self.consts = self.codeinfo.get("consts")
        self.names  = self.codeinfo.get("names")
        self.varnames = self.codeinfo.get("varnames")           # 局部变量名
        self.locals = {}                                    # 局部变量-值
        self.globals = globals
    
    def push(self, arg):
        self.stack.append(arg)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        raise Exception("vm pop error!")

    def popn(self, n):
        args = []
        for _ in range(n):
            args.append(self.pop())
        return args[-1:]
        
    def set_locals(self, locals):
        self.locals = locals
    
    def notfinish(self):
        return self.pc < len(self.instructions)
    
    def incpc(self, inc=1):
        self.pc += inc
    
    def jmpc(self, target):
        self.pc = target



    def __str__(self):
        return f"<Frame: {self.funcname}>"
    
    __repr__ = __str__
