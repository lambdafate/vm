from instype import *
from frame import Frame
import dis
import copy

class VM(object):
    def __init__(self):
        self.globals = {}
        self.frame   = None
        self.retval  = None
    
    def push_frame(self, frame):
        frame.prev = self.frame
        self.frame = frame
    
    def pop_frame(self):
        # 返回module frame 或者 自定义的函数帧
        self.frame = self.frame.prev if self.frame.prev else self.frame
        return self.frame

    # ins: (insname, oparg)
    def getargs(self, ins):
        if not ins.HAVEARG:
            return None
        if isconst(ins.opname):
            return self.frame.consts[ins.arg]
        elif isname(ins.opname):
            return self.frame.names[ins.arg]
        return ins.arg
    
    def run(self, codeinfo):
        frame = self.make_frame(codeinfo, self.frame, "Module", self.globals)
        self.run_frame(frame)

    def make_frame(self, codeinfo, prev=None, funcname="", globals={}):
        return Frame(codeinfo, prev, funcname, globals)

    def run_frame(self, frame):
        if frame == None or not isinstance(frame, Frame):
            raise Exception(f"run frame error: frame->{frame}")
        
        self.push_frame(frame)
        while(self.frame.notfinish()):
            ins = self.frame.instructions[self.frame.pc]

            bytecode = ins.opname.lower()
            if not hasattr(self, bytecode):
                raise Exception(f"not found function: {bytecode}, pc={self.frame.pc}")
                
            func = getattr(self, bytecode)
            # 在每条指令执行之前, 解析出指令参数对应的真实值
            if ins.HAVEARG:
                arg = self.getargs(ins)
                func(arg)
            else:
                func()

            # 该指令执行完毕后, 可能会改变当前帧栈(return_value)
            # if not self.frame:
            #     return


### 以下为所有已经实现的字节码
    def pop_top(self):
        self.frame.pop()
        self.frame.incpc()

    def binary_add(self):
        arg1 = self.frame.pop()
        arg2 = self.frame.pop()
        self.frame.push(arg1+arg2)
        self.frame.incpc()
    
    def inplace_add(self):
        tos = self.frame.pop()
        tos1 = self.frame.pop()
        self.frame.push(tos+tos1)
        self.frame.incpc()

    def return_value(self):
        """
            有两种return类型, 1.自定义函数 return to Module/函数帧 2.Module帧向上返回
            无论哪种类型, 1.返回帧后当前帧pc+1  2.如果当前不为Module帧, 则将上一帧的返回值push到当前帧中
        """
        # 获取当前帧栈的返回值
        self.retval = self.frame.pop()
        # 查看当前帧栈类型
        if self.frame.prev:
            self.pop_frame()                # 改变当前帧栈
            self.frame.push(self.retval)    # 将返回值压入当前帧栈
    
        self.frame.incpc()

    def load_const(self, arg):
        self.frame.push(arg)
        self.frame.incpc()

    def store_name(self, arg):
        self.globals[arg] = self.frame.pop()
        self.frame.incpc()

    def load_name(self, arg):
        self.frame.push(self.globals.get(arg, arg))
        self.frame.incpc()
    
    def load_fast(self, arg):
        self.frame.push(self.frame.locals.get(self.frame.varnames[arg]))
        self.frame.incpc()

    def store_fast(self, arg):
        value = self.frame.pop()
        varname = self.frame.varnames[arg]
        self.frame.locals[varname] = value
        self.frame.incpc()

    def make_function(self, arg):
        funcname = self.frame.pop()
        codeinfo = self.frame.pop()
        frame    = self.make_frame(codeinfo, self.frame, funcname, self.globals)
        self.frame.push(frame)
        self.frame.incpc()

    def call_function(self, arg):
        args = self.frame.popn(arg)
        func = self.frame.pop()             # frame对象 或者 builtin
        if func == "print":
            for arg in args:
                print(arg, end="")
            self.frame.push(None)
            self.frame.incpc()
        
        if isinstance(func, Frame):
            # 不在这里使pc指向下一条指令, 在frame返回, 即执行return_value时, 指向下一条指令
            # self.frame.incpc()
            # 使用深拷贝的对象, 不使用func, func相当于原始数据, 不能修改, 否则下次调用会出错
            self.push_frame(copy.deepcopy(func))

    def compare_op(self, arg):
        op = dis.cmp_op[arg]
        res = True
        right = self.frame.pop()
        left  = self.frame.pop()
        if op == "<":
            res = left < right
        elif op == ">":
            res = left > right
        self.frame.push(res)
        self.frame.incpc()
    
    def pop_jump_if_false(self, arg):
        res = self.frame.pop()
        if res:
            self.frame.incpc()
        else:
            self.frame.jmpc(arg)

    def jump_forward(self, arg):
        self.frame.incpc(arg)
    
    def jump_absolute(self, arg):
        self.frame.jmpc(arg)

if __name__ == "__main__":
    from convert import parser

    source = """
def demo():
    a = 2
    return a

x = demo() + demo()
print(x)
"""
    
    codeinfo = parser(source)


    # for index, ins in enumerate(codeinfo.get("instructions")):
    #     print(f"{index:<4}{ins}")

    # dis.dis(source)

    vm = VM()
    vm.run(codeinfo)


