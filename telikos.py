import sys
import os

#file = open('countdigits.cpy','r')

keyWords = ['def', 'declare', 'if', 'else', 'while', 'not', 'and', 'or', 'return', 'int', 'input', 'print']

line = 1

currentScope = None

if os.path.exists('intfile.int'):
    os.remove('intfile.int')
if os.path.exists('cfile.c'):
    os.remove('cfile.c')

intfile = open('intfile.int','w')
cfile = open('cfile.c','w')
		
ListQuads = []

def lexanal():
    global line
    state = 0
    char = ''
    wrd = ''
    lex = []
    while True:
        char = file.read(1)
        if char != ' ' and char != '\t' and char != '\n':
            wrd += char
        if (state == 0):
            
            if char == '':
                state = 8
            if char == '\n':
                line += 1
            if char.isalpha():
                state = 1
            if char.isdigit():
                state = 2
            if char == '<':
                state = 3
            if char == '>':
                state = 4
            if char == '=':
                state = 5
            if char == '#':
                state = 6
            if char == ',' or char == ';' or char == ':':
                char = file.read(1)
                lex = [wrd, 'delimeter', line]
                state = -1
            if char == '[' or char == ']' or char == '(' or char == ')':
                char = file.read(1)
                lex = [wrd, 'groupSymbols', line] 
                state = -1
            if char == '+' or char == '-' :
                char = file.read(1)
                lex = [wrd, 'addOperators', line]
                state = -1
            if  char == '*' or wrd == '//':
                char = file.read(1)
                lex = [wrd, 'mulOperators', line]
                state = -1
        if (state == 1):
            if not char.isalnum() and char != '_':
                if not char.isspace():
                    lex += [wrd[0:-1]]
                    wrd = wrd[0:-1]
                else:
                    lex += [wrd]
                if wrd in keyWords:
                   
                   if wrd == 'declare':
                       lex = ['#declare']
                   lex += ['keyword']
                  
                else:
                    lex += ['id']
                lex += [line]
                if char == '\n':
                    line += 1
                    char = file.read(1)
                state = -1
        if (state == 2):
            if not char.isdigit():
                lex += [wrd[0:-1], 'number', line]
                if char == '\n':
                    line += 1
                state = -1
        if (state == 3):
            char = file.read(1)
            if char == '=':
                wrd = '<='
                lex += [wrd, 'relOperator', line]
                state = -1           
            # if char != '=':
            #     wrd += wrd[0:-1]
            # else:
            #     char = file.read(1)
            lex += [wrd, 'relOperator', line]
            char = file.read(1)
            state = -1
        if (state == 4):
           # wrd += char
            if char == '=':
                wrd = '>='
                lex += [wrd, 'relOperator', line]
                state = -1
            
            # if char != '=':
            #     wrd += wrd[0:-1]
            # else:
            #     char = file.read(1)
            lex += [wrd, 'relOperator', line]
            char = file.read(1)
            state = -1
        if (state == 5):
            char = file.read(1)
            if char == '=':
                wrd = '=='
                lex += [wrd, 'relOperator', line]
                state = -1
            lex += [wrd, 'assignment', line]
            char = file.read(1)
            state = -1  
        if (state == 6):
            char = file.read(1)
            if (char == '$'):
                while True:
                    char = file.read(1)
                    if char == '\n':
                        line += 1
                    if char == '#':
                        char = file.read(1)
                        if char == '$':
                            char = file.read(1)
                            if char == '\n':
                                line += 1
                            state = 0
                            wrd = ''
                            break
            elif char in ['{', '}']:
                state = 7
            elif char.isalpha():
                state = 1
                wrd = char
        if (state == 7):
            wrd += char
            lex += [wrd, 'groupSymbols', line]
            char = file.read(1)
            if char == '\n':
                line+=1
                char = file.read(1)
            state = -1
        if (state == 8):
            exit()
        if (state == -1):
            file.seek(file.tell() - 1)
            #print(lex[0])
            return lex

# while (1):
#     lexres = lexanal()
#     print(lexres)

#---------------------------Pinakas Symbolwn------------------------------------ 
scopes = []

class Entity():
   
    def __init__(self):
        self.name = ""
        self.type = ""
        self.variable = self.variable()
        self.func = self.func()
        self.const = self.const()
        self.parameter = self.parameter()
        self.temp_var = self.temp_var()

    class variable():
        def __init__(self) :
            self.offset = 0
    
    class func():
        def __init__(self) :
            self.startQuad = 0
            self.argument = []
            self.flength = 0

    class const():
        def __init__(self) :
            self.value = ""

    class parameter():
        def __init__(self) :
            self.parMode = 0
            self.offset = 0

    class temp_var():
        def __init__(self) :
            self.offset = 0

class Scope():
    
    def __init__(self):
        self.name = ""
        self.entity = []
        self.nestingLevel = 0
        self.mitriki = None

class Argument():

    def __init__(self): 
        self.name = ""
        self.parMode = 0
        self.type = 0

def newScope(name):
    global currentScope
    s = Scope()
    s.name = name
    if currentScope == None:
        s.nestingLevel = 0
    else:
        s.nestingLevel = currentScope.nestingLevel + 1
    
    s.mitriki = currentScope
    currentScope = s

def deleteScope():
    global currentScope
    global scopes
    temp = currentScope

    print('(')
    for i in temp.entity:
        print(i.name , "-" , i.type , end = "\t")
    print(')')
    currentScope = temp.mitriki
    scopes += [temp]
    del temp

def newEntity(ent):
    global currentScope
    currentScope.entity.append(ent)   

def newArgument(arg):
    global currentScope
    currentScope.entity[-1].func.argument.append(arg)

def search(n,i):#arithmos quad i
    global ListQuads
    a = ''
    while True:
        i -= 1
        if ListQuads[i][1] == 'begin_block':
            a = ListQuads[i][2]
            break
    for s in scopes:
        if s.name == a:
            t = s
    while t != None :
        for i in t.entity :
            if i.name == n :
                return t,i
        t = t.mitriki
    return None

def calc_offset():
    global currentScope
    counter = 0
    if currentScope != None :
        for i in currentScope.entity:
            if i.type == "variable" or i.type == "parameter" or i.type == "temp_variable" : 
                counter += 1

    return 12 + 4 * counter
    
def conv_param():

    global currentScope
    for i in currentScope.mitriki.entity[-1].func.argument:
        ent = Entity()
        ent.name = i.name
        ent.type = "parameter"
        ent.parameter.parMode = i.parMode
        ent.parameter.offset = calc_offset()
        
        newEntity(ent)


#-------------------------Telikos--------------------------------------

riscFile = open('riscFile.asm','w')
riscFile.write('             \n\n\n')


def gnlvcode(varName,i):

    global currentScope
    global riscFile

    riscFile.write('lw t0,-4(sp)\n') #metaferei ston t0 th dieythinsi mias mh topikhw metavliths (stoiva gonea)
    s,e = search(varName,i) #psaxno to scope kai to entity ths metavliths

    level = currentScope.nestingLevel - s.nestingLevel #apo ton pinaka symvolwn vriskei posa epipeda epano visketai h mh topikh metavlith
    level = level - 1 # -1 afou exoume grapsei gia ton gonea

    count = 0
    while count <= level :
        riscFile.write('lw t0 ,-4(t0)\n') 
        count += 1

    if e.type == 'parameter':
        riscFile.write('addi t0,t0,-{0}'.format(e.parameter.offset))
    elif e.type == 'variable':
        riscFile.write('addi t0,t0,-{0}'.format(e.variable.offset))
    


def loadvr(v,r,i):

    global currentScope
    global riscFile

    if v.isdigit():
        riscFile.write('li t{0},{1}\n'.format(r,v))
    else :

        s,e = search(v,i)
        
        if s.nestingLevel == 0 and e.type == 'temp_variable':
            riscFile.write('lw t{0},-{1}(gp)\n'.format(r,e.temp_var.offset))
        elif s.nestingLevel == 0 and e.type == 'variable':
            riscFile.write('lw t{0},-{1}(gp)\n'.format(r,e.variable.offset))
        elif s.nestingLevel == currentScope.nestingLevel :
            if e.type == 'temp_variable':
                riscFile.write('lw t{0},-{1}(sp)\n'.format(r,e.tep_var.offset))
            elif e.type == 'variable':
                riscFile.write('lw t{0},-{1}(sp)\n'.format(r,e.variable.offset))
            elif e.type == 'parameter' and e.parameter.parMode == 'CV':
                riscFile.write('lw t{0},-{1}(sp)\n'.format(r,e.parameter.offset))
        elif currentScope.nestingLevel > s.nestingLevel :
            if e.type == 'parameter':
                gnlvcode(v,i)
                riscFile.write('lw t{0},(t0)\n'.format(r))
            elif e.type == 'variable':
                gnlvcode(v,i)
                riscFile.write('lw t{0},(t0)\n'.format(r))

            
        


def storerv(r,v,i):

    global currentScope
    global riscFile


    s,e = search(v,i)

    if s.nestingLevel == 0 and e.type == 'temp_variable':
        riscFile.write('sw t{0},-{1}(gp)\n'.format(r,e.temp_var.offset))
    elif s.nestingLevel == 0 and e.type == 'variable':
        riscFile.write('sw t{0},-{1}(gp)\n'.format(r,e.variable.offset))
    elif s.nestingLevel == currentScope.nestingLevel :
        if e.type == 'temp_variable':
            riscFile.write('sw t{0},-{1}(sp)\n'.format(r,e.tep_var.offset))
        elif e.type == 'variable':
            riscFile.write('sw t{0},-{1}(sp)\n'.format(r,e.variable.offset))
        elif e.type == 'parameter' and e.parameter.parMode == 'CV':
            riscFile.write('sw t{0},-{1}(sp)\n'.format(r,e.parameter.offset))
            #den exw REF
        elif currentScope.nestingLevel > s.nestingLevel :
            if e.type == 'parameter':
                gnlvcode(v,i)
                riscFile.write('sw t{0},(t0)\n'.format(r))
            elif e.type == 'variable':
                gnlvcode(v,i)
                riscFile.write('sw t{0},(t0)\n'.format(r))       

def finalCode(): 

    global currentScope
    global riscFile
    global ListQuads

    i = -1 #aukson arithmos parametrou
    case = {
        'jump': 'j L %s\n',
        '==': 'beq t1,t2,L %d\n',
        '>': 'bgt t1,t2,L %d\n',
        '<': 'blt t1,t2,L %d\n',
        '>=': 'bge t1,t2,L %d\n',
        '<=': 'ble t1,t2,L %d\n',
        '=': '',
        '+' : 'add t1,t1,t2\n',
        '-' : 'sub t1,t1,t2\n',
        '*' : 'mul t1,t1,t2\n',
        '//' : 'div t1,t1,t2\n',
        'in': 'li a7,5\n',
        'out':'li a0,%d\n',
        'halt':'li a0,0\nli a7,93\necall\n',
        'retv':'lw t0,-8(sp)\nsw t1,(t0)\n',
        'par': {
                'CV':'sw t0, -%d(fp)\n',
                'RET':'addi t0,sp,-%d\nsw t0,8(fp)\n'
                },
        'call': {
                    '==':'lw t0,-4(sp)\nswt0,-4(fp)\n',
                    '<': 'sw sp,-4(fp)\n'   
                },
        'begin_block': {
                        '!=': 'sw ra,(sp)\n',
                        '==' : 'j L: %d\n'
                    },
        'end_block': 'lw ra,(sp)\njr ra\n'
    }

    for quad in ListQuads:

        oper = quad[1]       
        num = quad[0]
        if oper == 'jump':
            riscFile.write(case['jump'] % (quad[4]))
        elif oper == '==':
            loadvr(quad[2], 1,num)
            loadvr(quad[3], 2,num)
            riscFile.write(case['=='] %(quad[4]))
        elif oper == '>':
            loadvr(quad[2], 1,num)
            loadvr(quad[3], 2,num)    
            riscFile.write(case['>'] %(quad[4]))
        elif oper == '<':
            loadvr(quad[2], 1,num)
            loadvr(quad[3], 2,num)
            riscFile.write(case['<'] %(quad[4]))
        elif oper == '>=':
            loadvr(quad[2], 1,num)
            loadvr(quad[3], 2,num)
            riscFile.write(case['>='] %(quad[4]))
        elif oper == '<=':
            loadvr(quad[2], 1,num)
            loadvr(quad[3], 2,num)
            riscFile.write(case['<='] %(quad[4]))
        elif oper == '=':
            loadvr(quad[2], 1,num)
            storerv(1,quad[4],num)
        elif oper == '+':
            loadvr(quad[2], 1,num)
            loadvr(quad[3], 2,num)
            riscFile.write(case['+'])
            storerv(1,quad[4],num)
        elif oper == '-':
            loadvr(quad[2], 1,num)
            loadvr(quad[3], 2,num)
            riscFile.write(case['-'])
            storerv(1,quad[4],num)
        elif oper == '*':
            loadvr(quad[2], 1,num)
            loadvr(quad[3], 2,num)
            riscFile.write(case['*'])
            storerv(1,quad[4],num)
        elif oper == '//':
            loadvr(quad[2], 1,num)
            loadvr(quad[3], 2,num)
            riscFile.write(case['//'])
            storerv(1,quad[4],num)
        elif oper == 'in':
            loadvr(quad[2], 1,num)
            riscFile.write(case['in'])
            riscFile.write('ecall\n')
        elif oper == 'out':
            loadvr(quad[2],1,num)
            riscFile.write(case['out'] %(1))
            riscFile.write('li a7,1')
            riscFile.write('ecall\n')
        elif oper == 'halt':
            riscFile.write(case['halt'])
        elif oper == 'retv':
            loadvr(quad[2], 1,num)
            riscFile.write(case['retv'])
        elif oper == 'par':
            if i == -1:
                s,e = search(quad[2],num)
                for j in s.entity:
                    if j.type == 'function':
                        riscFile.write('add fp,sp,%d\n' % (j.func.flength))
                        break
            i = 0
            if quad[3] == 'CV':
                loadvr(quad[2],0,num)
                riscFile.write(case['par']['CV'] % (12+4*i))
                i += 1
            elif quad[3] == 'RET':
                s,e = search(quad[2],num)
                riscFile.write(case['par']['RET'] % e.temp_var.offset)
        elif oper == 'call':
            i = -1 
            s,e = search(quad[4],num)
            if s.nestingLevel == currentScope.nestingLevel:
                riscFile.write(case['call']['=='])
            elif s.nestingLevel < currentScope.nestingLevel:
                riscFile.write(case['call']['<'])
            riscFile.write('add sp,sp,%d\n' %(e.func.flength))
            riscFile.write('jal L%d\n' %(e.func.startQuad))
            riscFile.write('add sp,sp,%d\n' %(e.func.flength))
        elif oper == 'begin_block' and currentScope.nestingLevel != 0:
            riscFile.write(case['begin_block']['!='])
        elif oper == 'begin_block' and currentScope.nestingLevel == 0:
            riscFile.seek(0,0)#epistrefo stin arxi tou arxeiou
            riscFile.write(case['begin_block']['=='] %(quad[0]))
            riscFile.seek(0,2)#epistrefo sto telos tou arxeiou
            riscFile.write('add sp,sp,%d\n' %(calc_offset()))
            riscFile.write('move s0,sp\n')
        elif oper == 'end_block' and currentScope.nestingLevel != 0:
            riscFile.write(case['end_block'])


#----------------------Endiamesos kwdikas------------------------------------

token = ""

Count_Quad = 0	
			
def nextQuad():    
    global Count_Quad
    return Count_Quad + 1
    
def genQuad(prwto, deutero, trito, tetarto):
	
    global Count_Quad
    global ListQuads
    list = []
	
    list = [nextQuad()]			
    list += [prwto] + [deutero] + [trito] + [tetarto]		
	
    Count_Quad +=1	
    ListQuads += [list]
    return list

        
                  
T_x = 1
List_Temp = []
def newTemp():
        
    global T_x
    global List_Temp

    lst = ['T_']
    lst.append(str(T_x))
    temp = "".join(lst)
    ent = Entity()
    ent.name = temp
    ent.type = "temp_variable"
    ent.temp_var.offset = calc_offset()
    newEntity(ent)
    T_x +=1
    List_Temp += [temp]

    return temp
    
def emptyList():
        
	pointer = []	
	return pointer
    
def makeList(x):
        
	ListX = [x]
	
	return ListX

def merge(List1, List2):
	
    list = []
    list += List1 + List2

    return list
    
def backPatch(list, z):

    global ListQuads
    for i in range(len(list)):
	    for j in range(len(ListQuads)):
                if(list[i] == ListQuads[j][0] and ListQuads[j][4] == '_'):
                    ListQuads[j][4] = z
                    
                    j = len(ListQuads)

token=""
def startRule():
    _main_part()
    call_main_part()
    print('OKKKK')
def _main_part():

    global token
    token = lexanal()
    if token[0] == 'def' :
        _main_function()
    
def _main_function():

    global token
    global scopes
    token = lexanal()
    f = token[0]
    ent = Entity()
    ent.name = f 
    ent.type = "function"
    ent.func.flength = calc_offset()
    genQuad("begin_block",f,"_","_")
    if token[1] == 'id' :
        token = lexanal()
        if token[0] == '(':
            token = lexanal()
            if token[0] == ')':
                token = lexanal()
                if token[0] == ':': 
                    token = lexanal()
                    if token[0] == '#{' :
                        ent.func.startQuad = nextQuad()
                        newScope(ent.name)
                        newEntity(ent)
                        token = lexanal()
                        declarations()
                        while token[0] == 'def' :
                            def_function()
                        statements() 
                        #deleteScope()
                        if token[0] != '#}':
                            print("Error ")
                            exit(1)
                        #token = lexanal()
                        genQuad("halt","_","_","_")
                        genQuad("end_block",f,"_","_")
                        scopes += [currentScope]
                        finalCode()

                        deleteScope()
                                    
def def_function():

    global token
    global currentScope
    token = lexanal()
    f = token[0]
    ent = Entity()
    ent.name = f
    
    ent.type = "function"
    ent.func.flength = calc_offset()
    genQuad("begin_block",f,"_","_")
    if token[1] == 'id':
        token = lexanal()
        if token[0] == '(' :
            token = lexanal()
            ent.func.startQuad = nextQuad()
            ent.func.nestingLevel = currentScope.nestingLevel + 1
            newEntity(ent)
            id_list("parameter")
            if token[0] == ')':
                token = lexanal()
                if token[0] == ':':
                    token = lexanal()
                    if token[0] == '#{' :
                        newScope(ent.name)
                        conv_param()
                        token = lexanal()
                        declarations()
                        while  token[0] == 'def' :  
                            def_function()                       
                        statements()
                        deleteScope()
                        if token[0] != '#}':
                            
                            print("Error ")
                            exit(1)                       
                        token = lexanal()
                        genQuad("end_block",f,"_","_")
                        

def declarations() :

    global token
    global cfile     
    while token[0] == '#declare' :
        cfile.write('int ')
        token = lexanal()
        declaration_line()
    
def declaration_line():

    global token
    id_list("declare")

def statement():
    
    global token 
    if token[1] == 'id' or token[0] == 'print' or token[0] == 'return':
        simple_statement() 
    elif token[0] == 'if' or token[0] == 'while' :
        structured_statement()
    else :
        print('Error if while')
        exit(1)

def statements():

    global token
    statement()
    while token[1] == 'id' or token[0] == 'print' or token[0] == 'return' or token[0] == 'if' or token[0] == 'while':
        statement()

def simple_statement():

    global token
    if token[1] == 'id':
        a = token[0]
        token = lexanal()
        assignment_stat(a)
    elif token[0] == 'print':
        token = lexanal()
        print_stat()
    elif token[0] == 'return':
        token = lexanal()
        return_stat()
    
def structured_statement():

    global token
    if token[0] == 'if' :
        token = lexanal()
        if_stat()
    elif token[0] == 'while':
        token = lexanal()
        while_stat()

def assignment_stat(a):

    global token
    if token[0] == '=':
        token = lexanal()
        if token[0] == 'int':
            token = lexanal()
            if token[0] == '(' :
                token = lexanal()
                if token[0] == 'input':
                    token = lexanal()
                    if token[0] == '(':
                        token = lexanal()
                        if token[0] == ')' :
                            token = lexanal()
                            if token[0] == ')' :
                                token = lexanal()
                                if token[0] != ';' :
                                    exit(1)
                                else:
                                    genQuad('in',a,'_','_')
        elif token[1] == 'addOperator' or token[1] == 'number' or token[0] == '(' or token[1] == 'id':
            z = expression()
            genQuad("=",z,"_",a)
            if token[0] != ';' :
                exit(1)
        token = lexanal()

def print_stat():

    global token
    if token[0] == '(':
        token = lexanal()
        e = expression()
        genQuad('out',e,'_','_')
        if token[0] == ')':
            token = lexanal()
            
            if token[0] != ';':
                exit(1)
    token = lexanal()

def return_stat():

    global token
    if token[0] == '(':
        token = lexanal()
        e = expression()
        genQuad('retv',e,'_','_')
        if token[0] == ')':
            token = lexanal()
            if token[0] != ';':
                exit(1)
    token = lexanal()


def if_stat():

    global token
    if token[0] == '(':
        token = lexanal()
        x,y = condition()
        if token[0] == ')':
            token = lexanal()
            if token[0] == ':':
                token = lexanal()
                if token[0] == '#{':
                    token = lexanal()
                    backPatch(x,nextQuad())
                    statements()
                    iflist = makeList(nextQuad())
                    genQuad('jump','_','_','_')
                    if token [0]!= '#}':
                        exit(5)
                    else:
                        backPatch(y,nextQuad())
                        
                        token = lexanal()
                else:
                    backPatch(x,nextQuad())
                    statement()
                    iflist = makeList(nextQuad())
                    genQuad('jump','_','_','_')
                    backPatch(y,nextQuad())
                if token[0] == 'else':
                     token = lexanal()
                     if token[0] == ':':
                        token = lexanal()
                        if token[0] == '#{':
                            token = lexanal()
                            statements()
                            if token [0]!= '#}':
                                exit(5)
                            else:
                                backPatch(iflist,nextQuad())
                                token = lexanal()
                        else:
                            
                            statement()
                            backPatch(iflist,nextQuad())
def while_stat():

    global token
    if token[0] == '(':
        token = lexanal()
        n = nextQuad()
        x,y = condition()        
        if token[0] == ')':
            token = lexanal()
            if token[0] == ':':
                token = lexanal()
                if token[0] == '#{':
                    token = lexanal()
                    backPatch(x,nextQuad())
                    statements()
                    if token [0] != '#}':
                        exit(0)
                    else:
                        genQuad('jump','_','_',n)
                        backPatch(y,nextQuad())
                        token = lexanal()
                else:
                    backPatch(x,nextQuad())
                    statement()
                    genQuad('jump','_','_',n)
                    backPatch(y,nextQuad())

def id_list(x):

    global token
    global currentScope
    global cfile
    if token[1] =='id':
        ent = Entity()
        ent.name = token[0]
        cfile.write(token[0])
        if x == "declare":
            ent.type = "variable"
            ent.variable.offset = calc_offset()
            newEntity(ent)
        else:
            ent = Argument()
            ent.name = token[0]
            ent.type = "parameter"
            ent.parMode = "CV"
            newArgument(ent) 
            #print(len(currentScope.entity[-1].func.argument))
            
        token = lexanal()
        while token[0] == ',':
            cfile.write(token[0])
            token = lexanal()           
            if token[1] == 'id':
                 ent = Entity()
                 ent.name = token[0]
                 cfile.write(token[0])
                 if x == "declare":
                    ent.type = "variable"
                    ent.variable.offset = calc_offset()
                    newEntity(ent)
                 else:
                    ent = Argument()
                    ent.name = token[0]
                    ent.type = "parameter"
                    ent.parMode = "CV"
                    newArgument(ent)
                 token = lexanal()
        cfile.write(';\n\t')         

def expression():

    global token
    optional_sign()
    fac = term()
    while token[1] == 'addOperators':
        sign = token[0]
        w = newTemp()
        token = lexanal()
        fac2 = term()
        genQuad(sign,fac,fac2,w)
        fac = w
    return fac

def term():

    global token
    fac = factor()
    while token[1] == 'mulOperators':
        sign = token[0]
        w = newTemp()
        token = lexanal()
        fac2 = factor()
        genQuad(sign,fac,fac2,w)
        fac = w
    return fac          

def factor():

    global token
    if token[0] == '(':
        token = lexanal()
        x1 = expression()
        if token[0] != ')':
            exit(0)
        else:
            place = x1
            token = lexanal()
    elif token[1] == 'id':
        place = token[0]
        token = lexanal()
        idtail(place)
    elif token[1] != 'number':
        exit(0)
    else:
        place=token[0]
        token = lexanal()   
    return place

def idtail(p):
    
    global token
    if token[0] == '(':
        token = lexanal()
        actual_par_list(p)
        if token [0] == ')':
            token = lexanal()
        else:
            exit(0)

def actual_par_list(p):

    global token
    e = expression()
    genQuad('par',e,'CV','_')
    while token[0] == ',':
            token = lexanal()
            e = expression()
            genQuad('par',e,'CV','_')
    g = newTemp()
    genQuad('par',g,'RET','_')
    genQuad('call','_','_',p)

def optional_sign():

    global token
    if token[1] == 'addOperator':
        token = lexanal()
    
def condition():

    global token
    x,y = bool_term()
    while token[0] == 'or':
            token = lexanal()
            backPatch(y,nextQuad())
            genQuad('jump','_','_',nextQuad())
            x2,y2 = bool_term()
            x = merge(x,x2)
            y = y2
    genQuad('jump','_','_','_')  
    return x,y     

def bool_term():

    global token   
    x,y = bool_factor()
    while token[0] == 'and':
            token = lexanal()
            backPatch(x,nextQuad())
            x2,y2 = bool_factor()
            y = merge(y,y2)
            x = x2
    return x,y
       
            

def bool_factor():

    global token
    if token[0] == 'not':
        token = lexanal()
        if token[0] == '[':
            token = lexanal()
            l1,l2= condition()
            if token[0] != ']':
                exit(0)
            else:
                token = lexanal()
                l1,l2 = l2,l1
    elif token[0] == '[':
        token = lexanal()
        condition()
        if token[0] != ']':
                exit(0)
        else:
                token = lexanal()
    else:
        x = expression()
        if token[1] != 'relOperator':
            exit(5)
        else:
            t = token[0]
            token = lexanal()
            y = expression()
            l1 = makeList(nextQuad())
            genQuad(t,x,y,"_")
            l2 = makeList(nextQuad())
    return l1,l2
 
    
def call_main_part():

    global token 
    if token[0] == 'if':
        token = lexanal()
        if token[0] == '__name__':
            token = lexanal()
            if token[0] == '==':
                token = lexanal()
                if token[0] == '"__main__"':
                    token = lexanal()
                    if token[0] == ':':
                        token = lexanal()
                        main_function_call()


def main_function_call():

    global token 
    if token[1] == 'id':
        token = lexanal()
        if token[0] == '(':
            token = lexanal()
            if token[0] == ')':
                token = lexanal()
                if token[0] != ';':
                    exit(1)
    token = lexanal()

def intFile():

    global intfile
    global ListQuads

    for quad in ListQuads:
        intfile.write(str(quad[0]))
        intfile.write(" ")
        intfile.write(str(quad[1]))
        intfile.write("  ")
        intfile.write(str(quad[2]))
        intfile.write("  ")
        intfile.write(str(quad[3]))
        intfile.write("  ")
        intfile.write(str(quad[4]))
        intfile.write("\n")
    

def cFile():

    global List_Temp
    global cfile
    global ListQuads

    if len(List_Temp) != 0:
        cfile.write('int ')
        for i in range(len(List_Temp)):
            cfile.write(List_Temp[i])
            if len(List_Temp) == i+1:
                cfile.write(';\n\t')
            else:
                cfile.write(',')

    count = 0
    for quad in ListQuads:
        if quad[1] == 'begin_block':
            cfile.write('L' + str(count+1) + ': ' + '\n\t')
        elif quad[1] == '=':
            cfile.write('L' + str(count+1) + ': ' + quad[4] + '=' + quad[2] + ';\n\t')
        elif quad[1] == '+':
            cfile.write('L' + str(count+1) + ': ' + quad[4] + '=' + quad[2] + '+'+quad[3] + ';\n\t')
        elif quad[1] == '-':
            cfile.write('L' + str(count+1) + ': ' + quad[4] + '=' + quad[2] + '-'+quad[3] + ';\n\t')                    
        elif quad[1] == '*':
            cfile.write('L' + str(count+1) + ': ' + quad[4] + '=' + quad[2] + '*' + quad[3] + ';\n\t')
        elif quad[1] == '//':
            cfile.write('L' + str(count+1) + ': ' + quad[4] + '=' + quad[2] + '//' + quad[3] + ';\n\t')
        elif quad[1] == 'jump':
            cfile.write('L' + str(count+1) + ': ' + 'goto L' + str(quad[4]) + ';\n\t')
        elif quad[1] == '<':
            cfile.write('L' + str(count+1) + ': ' + 'if(' + quad[2] + '<' + quad[3] + ') goto L' + str(quad[4]) + ';\n\t')
        elif quad[1] == '>': 
            cfile.write('L' + str(count+1) + ': ' + 'if(' + quad[2] + '>' + quad[3] + ') goto L' + str(quad[4]) + ';\n\t')
        elif quad[1] == '<=':
            cfile.write('L' + str(count+1) + ': ' + 'if(' + quad[2] + '<=' + quad[3] + ') goto L' + str(quad[4]) + ';\n\t')
        elif quad[1] == '>=':
            cfile.write('L' + str(count+1) + ': ' + 'if(' + quad[2] + '>=' + quad[3] + ') goto L' + str(quad[4]) + ';\n\t')
        elif quad[1] == '==':
            cfile.write('L' + str(count+1) + ': ' + 'if(' + quad[2] + '==' + quad[3] + ') goto L' + str(quad[4]) + ';\n\t')
        elif quad[1] == 'in':
            cfile.write('L' + str(count+1) + ': ' +'scanf(\'%d\', '+ quad[2]+');\n\t')
        elif quad[1] == 'out':
            cfile.write('L' + str(count+1) + ': ' + 'printf(\''+ quad[2]+'= %d\', '+ quad[2]+');\n\t')
        # elif quad[1] == 'halt':
        #     cfile.write('L' + str(count+1) + ': {}\n\t')
        count += 1

def runfiles():

    global intfile
    global cfile
    global ListQuads

    cfile.write('int main(){\n\t')
    startRule()
    intFile()
    cFile()
    cfile.write("\n}")
    ListQuads = [] #adiazoume th lista me ta quads
    intfile.close()
    riscFile.close()
    cfile.close()


#### main() ###
filename = sys.argv[1]

try:
    file = open(filename,'r')
    runfiles()
except IOError:
    print("Incorrect file or path name ", filename)
else:
    # main code
    #startRule()    
    for i in range(len(ListQuads)) :
       print(ListQuads[i])
file.close()





