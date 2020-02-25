import dis

class VM(object):
    def __init__(self, codeinfo):
        self.consts = codeinfo.get("consts", ())
        self.names = codeinfo.get("names", ())
        self.instructions = codeinfo.get("instructions", [])

        self.envs = {}
        self.stack = []

        self._in_consts = ["LOAD_CONST"]
        self._in_names = ["STORE_NAME", "LOAD_NAME"]
        self._return_arg = ["CALL_FUNCTION"]


    def push(self, arg):
        self.stack.append(arg)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        return None

    # ins: (insname, oparg)
    def getargs(self, ins):
        if ins.opcode < 90:
            return None
        if ins.opname in self._in_consts:
            return self.consts[ins.arg]
        elif ins.opname in self._in_names:
            return self.names[ins.arg]
        elif ins.opname in self._return_arg:
            return ins.arg
        return None
        

    def run(self):
        for ins in self.instructions:
            bytecode = ins.opname.lower()
            if not hasattr(self, bytecode):
                raise Exception(f"not found function: {bytecode}")
                
            func = getattr(self, bytecode)
            # 在每条指令执行之前, 解析出指令参数对应的真实值
            if ins.opcode >= 90:
                arg = self.getargs(ins)
                func(arg)
            else:
                func()


### 以下为所有已经实现的字节码
    def pop_top(self):
        self.pop()

    def binary_add(self):
        arg1 = self.pop()
        arg2 = self.pop()
        self.push(arg1+arg2)

    def return_value(self):
        self.pop()

    def load_const(self, arg):
        self.push(arg)
    
    def store_name(self, arg):
        self.envs[arg] = self.pop()

    def load_name(self, arg):
        self.push(self.envs.get(arg, arg))

    def call_function(self, arg):
        args = []
        for _ in range(arg):
            args.insert(0, self.pop())
        func = self.pop()
        if func == "print":
            for arg in args:
                print(arg, end="")
        self.push(None)





if __name__ == "__main__":
    from convert import parser

    source = """
a = 1 
b = 2
c = a+b
print(c)
    """
    
    codeinfo = parser(source)
    # print(codeinfo)
    vm = VM(codeinfo)
    vm.run()
