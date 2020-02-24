import dis

source = """
a = 3
b = 2
print("Hello", "asdf", a+b)
"""


class VM(object):
    def __init__(self, codeinfo):
        self.consts = codeinfo.get("consts", ())
        self.names = codeinfo.get("names", ())
        self.instructions = codeinfo.get("instructions", [])

        self.envs = {}
        self.stack = []

    # ins: (insname, oparg)
    def getargs(self, ins):
        codenum = dis.opmap.get(ins[0], -1)
        if codenum < 90:
            return None
        if ins[0] in ["LOAD_CONST"]:
            return self.consts[ins[1]]
        elif ins[0] in ["STORE_NAME", "LOAD_NAME"]:
            return self.names[ins[1]]
        elif ins[0] in ["CALL_FUNCTION"]:
            return ins[1]
        return None
        

    def run(self):
        for ins in self.instructions:
            if not hasattr(self, ins[0].lower()):
                raise Exception(f"not found function: {ins[0]}")
                
            func = getattr(self, ins[0].lower())
            # 在每条指令执行之前, 解析出指令参数对应的真实值
            if dis.opmap.get(ins[0], -1) < 90:
                func()
            else:
                arg = self.getargs(ins)
                func(arg)

    def pop_top(self):
        self.stack.pop()

    def binary_add(self):
        arg1 = self.stack.pop()
        arg2 = self.stack.pop()
        self.stack.append(arg1+arg2)

    def return_value(self):
        self.stack.pop()

    def load_const(self, arg):
        self.stack.append(arg)
    
    def store_name(self, arg):
        self.envs[arg] = self.stack.pop()

    def load_name(self, arg):
        self.stack.append(self.envs.get(arg, arg))

    def call_function(self, arg):
        args = []
        for _ in range(arg):
            args.insert(0, self.stack.pop())
        func = self.stack.pop()
        if func == "print":
            for arg in args:
                print(arg, end="")
        self.stack.append(None)



def parser(source):
    bytecode = dis.Bytecode(source)
    instructions = [(ins.opname, ins.arg) for ins in bytecode]

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


codeinfo = parser(source)
print(codeinfo)
vm = VM(codeinfo)
vm.run()
