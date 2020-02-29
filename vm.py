from instype import *
import dis


class VM(object):
    def __init__(self, codeinfo):
        self.consts = codeinfo.get("consts", ())
        self.names = codeinfo.get("names", ())
        self.instructions = codeinfo.get("instructions", [])

        self.envs = {}
        self.stack = []

        self.pc = 0
        self.inslength = len(self.instructions)

    def push(self, arg):
        self.stack.append(arg)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        raise Exception("vm pop error!")

    # ins: (insname, oparg)
    def getargs(self, ins):
        if not ins.HAVEARG:
            return None
        if isconst(ins.opname):
            return self.consts[ins.arg]
        elif isname(ins.opname):
            return self.names[ins.arg]
        
        return ins.arg
        

    def run(self):
        while(self.pc < self.inslength):
            ins = self.instructions[self.pc]

            bytecode = ins.opname.lower()
            if not hasattr(self, bytecode):
                raise Exception(f"not found function: {bytecode}")
                
            func = getattr(self, bytecode)
            # 在每条指令执行之前, 解析出指令参数对应的真实值
            if ins.HAVEARG:
                arg = self.getargs(ins)
                func(arg)
            else:
                func()


### 以下为所有已经实现的字节码
    def pop_top(self):
        self.pop()
        self.pc += 1

    def binary_add(self):
        arg1 = self.pop()
        arg2 = self.pop()
        self.push(arg1+arg2)
        self.pc += 1

    def return_value(self):
        self.pop()
        self.pc += 1

    def load_const(self, arg):
        self.push(arg)
        self.pc += 1

    def store_name(self, arg):
        self.envs[arg] = self.pop()
        self.pc += 1

    def load_name(self, arg):
        self.push(self.envs.get(arg, arg))
        self.pc += 1

    def call_function(self, arg):
        args = []
        for _ in range(arg):
            args.insert(0, self.pop())
        func = self.pop()
        if func == "print":
            for arg in args:
                print(arg, end="")
        self.push(None)
        self.pc += 1

    def compare_op(self, arg):
        op = dis.cmp_op[arg]
        res = True
        right = self.pop()
        left  = self.pop()
        if op == "<":
            res = left < right
        elif op == ">":
            res = left > right
        self.push(res)
        self.pc += 1
    
    def pop_jump_if_false(self, arg):
        res = self.pop()
        if res:
            self.pc += 1
        else:
            self.pc = arg

    def jump_forward(self, arg):
        self.pc += arg

if __name__ == "__main__":
    from convert import parser

    source = """
if 3 < 2:
    print("big")
else:
    print("small")
"""
    
    codeinfo = parser(source)
    # print(codeinfo)
    vm = VM(codeinfo)
    vm.run()
