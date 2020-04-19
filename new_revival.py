import re

reg=[]
for i in range(32):
    reg.append([0,1])
# 1 means that the reg is free right now! 
# the second bit will be used as a dirty bit from now on

mem=[]
for i in range(1024):
    mem.append(0)
reg[0][0]='0x10000000'
mem_index=0    
reg[1][0]=12
reg[2][0]=13
def sep(text):
    data_index_start=0
    command_index_start=0
    
    #for check in text:
    index=-1
    flag=False
    for test in text:
        sep = '//'
        test = test.split(sep, 1)[0]
        index=index+1
        expr = re.compile('.data')
        mo=expr.search(test)
        
        if mo:
            data_index_start=index
        
        expr = re.compile('.globl\s*main')
        mo=expr.search(test)
        if mo:
            command_index_start=index
        
    return text[data_index_start:command_index_start],text[command_index_start+1:]

# above this all the common function and memory allocation will be there
        
f=open("check.s",'r')
text=f.readlines()
dataseg,command=sep(text)

special_mem=[]
#data segment works starts here FUN START NOW :)
print(dataseg)
print(command)

for i in command:
    print(i)

clean_instr_list=[]   # for storing all the instructions

def ldword(words):
    global mem_index
    for word in words:
        mem[mem_index]=int(word)
        mem_index+=1
        #print(mem[mem_index-1])
    #print(mem[:mem_index])
    #print(mem_index)
g=-1
def define_memory_chunk(name,words):
    global mem_index
    start=mem_index
    for word in words:
        mem[mem_index]=int(word)
        mem_index+=1
        #print(mem[mem_index-1])
    #print(mem[:mem_index+1])
    end=mem_index-1
    segment=[]
    segment.append(name)
    segment.append(start)
    segment.append(end)
    special_mem.append(segment)
    #print(special_mem)

while g<(len(dataseg)-1):
    g+=1
    test=dataseg[g]
    sep='//'
    if test is '\n':
        continue
    rest=test.split(sep,1)[0]
    if not rest:
        continue
    flag=False
    expr=re.compile('\w*\:\s\s*.word\s(\d*,\s*)*\d*\s*')
    
    mo=expr.search(rest)
    #checking for names memory
    if mo:
        flag=True
        ch=mo.group()
        ch=re.split('\W|,|$',ch)
        instr=[]
        for i in ch:
            if i:
                instr.append(i)
        
        #simplopr(instr)
        #print(instr)
        define_memory_chunk(instr[0],instr[2:])
        
        
    if flag is not True:
        expr=re.compile('.word\s(\d*,\s*)*\d*\s*') # for simple word
        mo=expr.search(rest)
        if mo:
            flag=True
            ch=mo.group()
            ch=re.split('\W|,|$',ch)
            instr=[]
            for i in ch:
                if i:
                    instr.append(i)
            #print(instr)
            define_memory_chunk(' ',instr[1:])
        #simplopr(instr)
            #print(instr)
        #ldword(instr[1:])
        
        #define_memory_chunk('name',instr[1:])
    #print(test)
    
#data segment ends now
    
    
    
    
    
# command segment works from here
    
def loadworda(instr):
    #print('this is isntr',instr)
    regindex=0
    memindex=0
    rg=instr[1]
    #print(rg)
    #print(ord(rg[0]))
    a=ord(rg[0][0])
    a=a-97
    regindex=(a*10 + int(rg[1]))
    
    rg = instr[2]
    memindex=int(rg[0:2]+rg[7:10],16)
    memindex=memindex/4
    reg[regindex][0]=mem[memindex]
    
def loadadda(instr):
    #print('this is isntr',instr)
    regindex=0
    rg=instr[1]
    #print(rg)
    #print(ord(rg[0]))
    a=ord(rg[0])
    a=a-97
    regindex=(a*10 + int(rg[1]))
    
    reg[regindex][0]=instr[2]
    #print (reg[regindex])
    
def storeworda(instr):
    #print('this is isntr',instr)
    regindex=0
    memindex=0
    rg=instr[1]
    #print(rg)
    #print(ord(rg[0]))
    a=ord(rg[0])
    a=a-97
    regindex=(a*10 + int(rg[1]))
    
    rg = instr[2]
    memindex=int(rg[0:2]+rg[7:10],16)
    memindex=memindex/4
    mem[int(memindex)]=reg[int(regindex)]
    #print(mem[int(memindex)])
    
def loadwordr(instr):
    #print('this is isntr',instr)
    #print(len(instr))
    if len(instr)==3:
        regindex1=0
        regindex2=0
        memindex=0
        rg=instr[1]
        #print(rg)
        #print(ord(rg[0]))
        a=ord(rg[0])
        a=a-97
        regindex1=(a*10 + int(rg[1]))
        
        rg=instr[2]
        a=ord(rg[0])
        a=a-97
        regindex2=(a*10 + int(rg[1]))
        
        rg=reg[regindex2]
        memindex=int(rg[0:2]+rg[7:10],16)
        memindex=memindex/4
        reg[int(regindex1)]=mem[int(memindex)]
        
    if len(instr)==4:
        regindex1=0
        regindex2=0
        memindex=0
        rg=instr[1]
        #print(rg)
        #print(ord(rg[0]))
        a=ord(rg[0])
        a=a-97
        regindex1=(a*10 + int(rg[1]))
        #print(regindex1)
        rg=instr[3]
        a=ord(rg[0])
        a=a-97
        regindex2=(a*10 + int(rg[1]))
        rg=reg[regindex2]
        memindex=int(rg[0:2]+rg[7:10],16)
        memindex=memindex+int(instr[2])
        memindex=memindex/4
        #print(memindex,'dd')
        reg[int(regindex1)]=mem[int(memindex)]
        #print(mem[int(memindex)],"hello")
        
def storewordr(instr):
    #print('this is isntr',instr)
    if len(instr)==3:
        regindex1=0
        regindex2=0
        memindex=0
        rg=instr[1]
        #print(rg)
        #print(ord(rg[0]))
        a=ord(rg[0])
        a=a-97
        regindex1=(a*10 + int(rg[1]))
        
        rg=instr[2]
        a=ord(rg[0])
        a=a-97
        regindex2=(a*10 + int(rg[1]))
        
        rg=reg[regindex2]
        memindex=int(rg[0:2]+rg[7:10],16)
        memindex=memindex/4
        mem[int(memindex)]=reg[int(regindex1)]
    if len(instr)==4:
        regindex1=0
        regindex2=0
        memindex=0
        rg=instr[1]
        #print(rg)
        #print(ord(rg[0]))
        a=ord(rg[0])
        a=a-97
        regindex1=(a*10 + int(rg[1]))
        
        rg=instr[3]
        a=ord(rg[0])
        a=a-97
        regindex2=(a*10 + int(rg[1]))
        rg=reg[regindex2]
        memindex=int(rg[0:2]+rg[7:10],16)
        memindex=memindex+int(instr[2])
        memindex=memindex/4
        #print(memindex,'dd')
        mem[int(memindex)]=reg[int(regindex1)]
        #print(mem[int(memindex)])

def simplopr(command):
    index=[]
    for rg in command[1:]:
        #print(ord(rg[0]))
        a=ord(rg[0])
        a=a-97
        index.append(a*10 + int(rg[1]))
    
    if i in index:
        if i not in range(32):
            print("Invalid Syntax")
    #print(command[0])
    temp1=str(reg[index[1]][0])
    #print(temp1)
    if len(temp1)>9:
        temp1=int(temp1[-3:],16)
        #print(temp1,"tmep1")
    else:
        temp1=-1
    
    temp2=str(reg[index[2]][0])
    
    if len(temp2)>9:
        temp2=int(temp2[-3:],16)
    else:
        temp2=-1
    
    
    if command[0] == 'add':
        print("ADDED")
        if temp1!=-1 and temp2==-1:
            temp3 = temp1+reg[index[2]][0]
            print(temp3,"value")
            temp3=hex(temp3)
            #print(temp3,"hex")
            temp3=str(temp3)
            temp3=temp3[2:]
            temp3='0x10000'+temp3
            reg[index[0]][0]=temp3
        elif temp1==-1 and temp2!=-1:
            temp3 = temp2+reg[index[1]][0]
            #print(temp3,"value")
            temp3=hex(temp3)
            #print(temp3,"hex")
            temp3=str(temp3)
            temp3=temp3[2:]
            temp3='0x10000'+temp3
            reg[index[0]][0]=temp3
        else: 
            print("this is the one")
            reg[index[0]][0]=reg[index[1]][0]+reg[index[2]][0]
    elif command[0] == 'sub':
        #print("SUBTRACTED")
        reg[index[0]][0]=reg[index[1]][0]-reg[index[2]][0]
    elif command[0] == 'slt':
        if reg[index[1]][0]<reg[index[2]][0]:
            reg[index[0]][0]=1
        else:
            reg[index[0]][0]=0
    else:
        print("INVALID SYNTAX")
    
def addi(command):
    index=[]
    for rg in command[1:3]:
        #print(ord(rg[0]))
        a=ord(rg[0])
        a=a-97
        index.append(a*10 + int(rg[1]))
        
    temp1=str(reg[index[1]])
    #print(temp1)
    if len(temp1)>9:
        temp1=int(temp1[-3:],16)
        #print(temp1,"tmep1")
    else:
        temp1=-1

    if i in index:
        if i not in range(32):
            print("Invalid Syntax")
    #print(command[0])
    if command[0] == 'addi':
        if temp1!=-1:
            temp3 = temp1+int(command[3])
            #print(temp3,"value")
            temp3=hex(temp3)
            #print(temp3,"hex")
            temp3=str(temp3)
            temp3=temp3[2:]
            while (len(temp3)<3):
                temp3='0'+temp3
            temp3='0x10000'+temp3
            reg[index[0]]=temp3
        else:
            reg[index[0]]=reg[index[1]]+int(command[3])
    else:
        print("INVALID SYNTAX")
 

def srch( check,command,g):
    counter=-1
    for i in command:
        counter=counter+1
        sep = '//'
        if i is '\n':
            continue
        rest = i.split(sep, 1)[0]
        if not rest:
            continue
        expr=re.compile('\s*'+check+'[:]\s*')
        mo=expr.search(rest)
        flag=False
        if mo:
            flag=True
            if counter is not g:
                return counter
            
def comparison(instr,command,g):
    index=[]
    #print(instr)
    for rg in instr[1:-1]:
        #print(ord(rg[0]))
        a=ord(rg[0])
        a=a-97
        index.append(a*10 + int(rg[1]))
    #print(index)
    if instr[0] =='beq':
        if(reg[index[0]]==reg[index[1]]):
            #print("EQUAL")
            return ((srch(instr[3],command,g))-1)
        else:
            return g
    elif instr[0] =='bne':
        if(reg[index[0]]==reg[index[1]]):
             #print("EQUAL")
             return g
        else:
            return ((srch(instr[3],command,g))-1)
    else:
        print("INVALID SYNTAX")
        return g

g=-1
while g<(len(command)-1):
    g+=1
    #print(g)
    test=command[g]
    #print(test)
    sep = '//'
    if test is '\n':
        continue
    rest = test.split(sep, 1)[0]
    if not rest:
        continue
    flag=False
    # flag is used to keep the track of the number of instructions compiled in a step
    #for add sub and so on:)
    expr=re.compile('(\s*\w\w\w\s*\$\w\d\s*,\s*\$(\w\d|zero)\s*,\s*\$(\w\d|zero)\s*)')
    mo=expr.search(rest)
    
    if mo:
        flag=True
        ch=mo.group()
        ch=re.split('\W|,|$',ch)
        instr=[]
        for i in ch:
            if i:
                instr.append(i)
        clean_instr_list.append(instr+[5])
        simplopr(instr)
        print(instr)
        print("simplopr")
    
    if flag is not True: #for bne and beq
        expr=re.compile('(\s*\w\w\w\w\s*\$\w\d\s*,\s*\$(\w\d|zero)\s*,\s*\d*\s*)')
        mo=expr.search(rest)
        if mo:
            flag=True
            ch=mo.group()
            ch=re.split('\W|,|$',ch)
            instr=[]
            for i in ch:
                if i:
                    instr.append(i)
            print(instr)
            addi(instr)
            clean_instr_list.append(instr+[5])
            #g=(srch(instr[3],command,g))-1
            #print(g)
            
    if flag is not True: #for bne and beq
        expr = re.compile('(\s*\w\w\w\s*\$(\w\d|zero)\s*,\s*\$(\w\d|zero)\s*,\s*(\w|\d)*\s*)')
        mo=expr.search(rest)
        if mo:
            flag=True
            ch=mo.group()
            ch=re.split('\W|,|$',ch)
            instr=[]
            for i in ch:
                if i:
                    instr.append(i)
            print(instr)
            clean_instr_list.append(instr+[5])
            g=comparison(instr,command,g)
            #g=(srch(instr[3],command,g))-1
            #print(g)
            
    if flag is not True:  # for jump
        expr = re.compile('(\s*[j]\s\s*(\w|\d)*)')
        mo=expr.search(rest)
        if mo:
            flag=True
            ch=mo.group()
            ch=re.split('\W|,|$',ch)
            instr=[]
            for i in ch:
                if i:
                    instr.append(i)
            g=(srch(instr[1],command,g))-1
            #continue
            #print(g)
            #print(instr)
            clean_instr_list.append(instr+[5])
    if flag is not True:  # for LW,LA,SW with register as reference 
        expr = re.compile('(\s*\w\w\s*\$\w\d\s*,\s*((\$\w\d)|(\d\(\$\w\d\))))')   
        mo=expr.search(rest)
        #print("lw chcek")
        if mo:
            flag=True
            ch=mo.group()
            ch=re.split('\W|,|$',ch)
            instr=[]
            for i in ch:
                if i:
                    instr.append(i)
            print(instr)
            clean_instr_list.append(instr+[5])
            if instr[0]=='lw':
                print("kload")
                #loadwordr(instr)
            elif instr[0]=='sw':
                storewordr(instr)
                #print("kk")
            elif instr[0]=='la':
                loadaddr(instr)
                #print("kkk")
    
    if flag is not True:  # for LW,LA,SW with address as reference 
        expr = re.compile('(\s*\w\w\s*\$\w\d\s*,\s*(0x([0-9a-f])*))')   
        mo=expr.search(rest)
        if mo:
            flag=True
            ch=mo.group()
            ch=re.split('\W|,|$',ch)
            instr=[]
            for i in ch:
                if i:
                    instr.append(i)
            #print(instr)
            clean_instr_list.append(instr+[5])
            if instr[0]=='lw':
                loadworda(instr)
                
            elif instr[0]=='sw':
                storeworda(instr)
            elif instr[0]=='la':
                loadadda(instr)

    
    if flag is not True:
        expr =re.compile('\s*(\w|\d)*')
        mo=expr.search(rest)
        if mo:
            flag=True
            
    if flag is not True:
        print("Invalid Syntax")
        break




print(" the clean part starts from here\n")
def convert_to_index(command):
    index=[]
    for rg in command[1:-1]:
            #print(ord(rg[0]))
        a=ord(rg[0])
        a=a-97
        index.append(a*10 + int(rg[1]))   
    return index
def convert_to_index_address(command): # output format reg1 index(target) , reg 2[index](address stored in this register) , offset/4 for finding the index in memory 
    index=[]
    reg1_index = (ord(command[1][0])-97)*10 + int(command[1][1])
    index.append(reg1_index)
    reg2_index = (ord(command[3][0])-97)*10 + int(command[3][1])
    index.append(reg2_index)
    index.append(int((int(command[2]))/4))
    return index




def instruction_fetch(instruction):
    if instruction[0] == 'add':
        print("this is add")  
        # now we can enumerate our fetched instructions I'm giving 1 to the instruction add
        instruction[0]=1
    
    if instruction[0] == 'lw':
        print("this is a load word instruction")
        instruction[0] = 2

    instruction[-1]-=1  # indicating that this stage is done
def instruction_decode(instruction):
    instruction[-1]-=1

    #right now i don't think that we need to do anything in the decoding part for add as such for now


def instruction_execution(instruction,laches):
    instruction[-1]-=1
    dependency =False
    execution_lache =[]   # for data forwarding we need the laches result to forward it in the next stage
    if instruction[0] == 1:
         # this means that the instruction is add
        index=[]
        for rg in instruction[1:4]:
        #print(ord(rg[0]))
            a=ord(rg[0])
            a=a-97
            index.append(a*10 + int(rg[1]))
        print(index)
        # now the index stores the references of all the registers index[0]-> target register index[1],index[2] -> one that should be added
        if reg[index[1]][1]==0 or reg[index[2]][1]==0: # value is not updated which should be at that time
            dependency = True
            instruction[-1]+=1
            print("im breakning at ",i)
            return execution_lache,dependency   # the true value of dependency shows the depency on the other instructions
        print(instruction)
        print(reg)
        print("register are",reg[index[0]][0],reg[index[1]][0],reg[index[2]][0])
        reg[index[0]][0]=(reg[index[1]][0])+(reg[index[2]][0])
        execution_lache.append((reg[index[0]][0],index[0]))

    if instruction[0] == 2: # this means we are in the lw instruction
        print(instruction, "here comes the indexes")
        index = convert_to_index_address(instruction)
        reg[index[0]][1] = 0 # memory is out of date            
        print(index)
        
    return execution_lache,dependency

def instruction_memory_back(instruction):
    instruction[-1]-=1
    index_update = -1
    if instruction[0] ==2:   # updating the value of the target register here 
    # One thing to keep in mind is that we cant make the dirty bit 1 here as the other instruction EX will then be runned in the same cycle
        index = convert_to_index_address(instruction)
        print(index)
        rg = reg[index[1]][0]
        memindex=int(rg[0:2]+rg[7:10],16)
        reg[index[0]][0] =  mem[int(memindex/4) +index[2]]
        index_update = index[0] # now it can be used further
    return index_update    

def instruction_write_back(instruction,instruction_list,instruction_index):
    instruction[-1]-=1
    if instruction[0] == 1:
        index=[]
        for rg in instruction[1:-1]:
            #print(ord(rg[0]))
            a=ord(rg[0])
            a=a-97
            index.append(a*10 + int(rg[1]))    
        reg[index[0]][1] = 1
    instruction_list.pop(instruction_index)
  # 1->add
  # 2->lw          


run =5
cycles=0
execution_lache =[]
while(len(clean_instr_list)!=0):
    i=0
    index_update = -1
    stages_flag = [False,False,False,False,False]  # for making sure that each stage should be used once in a cycle
    while(i < len(clean_instr_list)):
        if(clean_instr_list[i][-1]==5 and stages_flag[0] is not True):
            instruction_fetch(clean_instr_list[i])
            stages_flag[0] = True
            print(clean_instr_list[i])
        elif(clean_instr_list[i][-1]==4 and stages_flag[1] is not True):
            instruction_decode(clean_instr_list[i])
            stages_flag[1] = True
            print(clean_instr_list[i])

        elif(clean_instr_list[i][-1]==3 and stages_flag[2] is not True):
                #index = convert_to_index(instruction)
            if clean_instr_list[i][0] == 1:    
                execution_lache,dependency = instruction_execution(clean_instr_list[i],execution_lache)
                if dependency is True:
                    print("im breakning at ",i)
                    break
            if clean_instr_list[i][0] == 2:
                execution_lache,dependency = instruction_execution(clean_instr_list[i],execution_lache)
            stages_flag[2] = True
            print(clean_instr_list[i])

        elif(clean_instr_list[i][-1]==2 and stages_flag[3] is not True):
            index_update = instruction_memory_back(clean_instr_list[i])
            stages_flag[3] = True
            print(clean_instr_list[i])

        elif(clean_instr_list[i][-1]==1 and stages_flag[4] is not True):
            instruction_write_back(clean_instr_list[i],clean_instr_list,i)
            stages_flag[4] = True
            i-=1
            #print(clean_instr_list[i])
        i+=1
    if index_update!=-1:    
        reg[index_update][1] = 1
    print(stages_flag)
    
    print("   \n\n\n\n\n")
    cycles+=1
    run-=1
    print(clean_instr_list)
    # if run ==0:
    #     exit(0)
print("cycles are ",cycles)
print(reg)
