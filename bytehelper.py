import dis


# 显示所有类型的字节码序列
def display():
    bytecode = [ byte for byte in dis.opname if byte[0] != "<"]

    # print(bytecode)
    print(f"dis.cmp_op:\n\t{dis.cmp_op}\n")
    toremove = []

    display = ["hascompare", "hasconst", "hasfree",
            "hasname", "hasjrel", "hasjabs", "haslocal"]

    for attr in display:
        if not hasattr(dis, attr):
            raise Exception(f"dis.{attr} not found!")
        print(f"dis.{attr}:")
        func = getattr(dis, attr)
        for bytecode in func:
            print(f"\t{dis.opname[bytecode]:<20}\t{bytecode}")
            toremove.append(dis.opname[bytecode])
        print("")
    print("other bytecode:")
    bytecodes = [bytecode for bytecode in dis.opname if bytecode[0] != "<"]
    for bytecode in bytecodes:
        if bytecode in toremove:
            continue
        print(f"\t{bytecode:<20}\t{dis.opmap.get(bytecode)}")

if __name__ == "__main__":
    import sys
    stdout = sys.stdout
    with open("./bytecode", "w", encoding="utf8") as f:
        sys.stdout = f
        display()
    sys.stdout =stdout