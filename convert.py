import dis
from instruction import Instruction
from instype import isjabs, isjrel

"""parser: 根据字符串解析出codeobject
Keyword arguments:
argument 源代码字符串
Return: 包含codeobject属性的字典
"""


def parser(source):
    bytecode = dis.Bytecode(source)
    instructions = turnins(list(bytecode))

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


def turnins(bytecodes):
    instructions = [Instruction(bytecode.opname, bytecode.arg) for bytecode in bytecodes]
    targets = _findall_target(bytecodes)
    # print(f"target: {targets}")
    for offset, index in targets:
        jmps = _findall_jmp(bytecodes, offset)
        # print(f"jmps-offset-{offset}: {jmps}")
        for jmpindex in jmps:
            opname = bytecodes[jmpindex].opname
            # 该跳转为绝对跳转
            if isjabs(opname):
                instructions[jmpindex].arg = index
            elif isjrel(opname):
                instructions[jmpindex].arg = index - jmpindex
            else:
                raise Exception(f"jmp error for bytecode: {opname}")
    return instructions

# 找到所有跳转到目标指令的bytecode
def _findall_jmp(bytecodes, offset):
    jmps = []
    for index, bytecode in enumerate(bytecodes):
        if bytecode.arg == offset and isjabs(bytecode.opname):
            jmps.append(index)
        elif bytecode.argval == offset and isjrel(bytecode.opname):
            jmps.append(index)
        
    return jmps

# 找到所有jmp_target的bytecode
def _findall_target(bytecodes):
    targets = [(bytecode.offset, bytecodes.index(bytecode)) for bytecode in bytecodes if bytecode.is_jump_target]
    return targets


if __name__ == "__main__":
    source = """
if 3 > 2:
    print("bigger!")
else:
    print("small!")
    """
    res = parser(source)
    for index, ins in enumerate(res.get("instructions")):
        print(f"{index} : {ins}")
    print("\n")
    dis.dis(source)
    
