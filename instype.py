import dis

ARGTYPE_COMPARE = 0
ARGTYPE_CONST = 1
ARGTYPE_FREE = 2
ARGTYPE_NAME = 3
ARGTYPE_JREL = 4
ARGTYPE_JABS = 5
ARGTYPE_LOCAL = 6
ARGTYPE_OTHER = 7

def iscompare(bytecode):
    bytecode = bytecode if isinstance(bytecode, int) else dis.opmap.get(bytecode)
    return bytecode in dis.hascompare
    

def isconst(bytecode):
    bytecode = bytecode if isinstance(bytecode, int) else dis.opmap.get(bytecode)
    return bytecode in dis.hasconst
    

def isfree(bytecode):
    bytecode = bytecode if isinstance(bytecode, int) else dis.opmap.get(bytecode)
    return bytecode in dis.hasfree
    

def isname(bytecode):
    bytecode = bytecode if isinstance(bytecode, int) else dis.opmap.get(bytecode)
    return bytecode in dis.hasname
    

def isjrel(bytecode):
    bytecode = bytecode if isinstance(bytecode, int) else dis.opmap.get(bytecode)
    return bytecode in dis.hasjrel
    

def isjabs(bytecode):
    bytecode = bytecode if isinstance(bytecode, int) else dis.opmap.get(bytecode)
    return bytecode in dis.hasjabs
    

def islocal(bytecode):
    bytecode = bytecode if isinstance(bytecode, int) else dis.opmap.get(bytecode)
    return bytecode in dis.haslocal
    

def what_the_fuck_are_args(bytecode):
        
    if iscompare(bytecode):
        return ARGTYPE_COMPARE
    
    if isconst(bytecode):
        return ARGTYPE_CONST
    
    if isfree(bytecode):
        return ARGTYPE_FREE
    
    if isname(bytecode):
        return ARGTYPE_NAME
    
    if isjrel(bytecode):
        return ARGTYPE_JREL
    
    if isjabs(bytecode):
        return ARGTYPE_JABS
    
    if islocal(bytecode):
        return ARGTYPE_LOCAL
    return ARGTYPE_OTHER
    
