import re
reg=[]
for i in range(32):
    reg.append(0)

mem=[]
for i in range(1024):
    mem.append(0)

inputs =open("input.txt",'r')
text=inputs.readlines()

# initialising some values to check the working
block_l1  = int(text[0])
assoc_l1  = int(text[1])
setl1size = int(text[2])
l1_latency = int(text[3])

block_l2  = int(text[5])
assoc_l2  = int(text[6])
setl2size=int(text[7])
l2_latency = int(text[8])

mem_latency = int(text[10])

set_l1 = int(setl1size/(block_l1*assoc_l1))
set_l2 = int(setl2size/(block_l2*assoc_l2))
# computing the set size here

cache_l1  = []
for i in range(set_l1):
    temp1 = []
    for j in range(assoc_l1):
        temp2 = []
        temp3 =[]
        for k  in range(block_l1):
            temp3.append(-1)
        temp2.append(temp3)
        temp2.append(-1)
        temp2.append(-1)
        temp1.append(temp2)
    cache_l1.append(temp1)
# structure of the cache--->  cache[<index>]  has the set  now in each set we have three things 
# 1-> blocks 2-> starting index 3-> time for LRU of that block  
print("---------cache_l1------")
print(cache_l1)
print("-----------------------")
cache_l2 = []

for i in range(set_l2):
    temp1 = []
    for j in range(assoc_l2):
        temp2 = []
        temp3 =[]
        for k  in range(block_l2):
            temp3.append(-1)
        temp2.append(temp3)
        temp2.append(-1)
        temp2.append(-1)
        temp1.append(temp2)
    cache_l2.append(temp1)

print("--------cache_l2------")
print(cache_l2)
print("----------------------")

# this function writes the cache with a block of address from the memory
# this function assumes that cache does not have that address block
def cache_writing(addr,cache,associativity,block_size,number_of_sets):

    page =[]

    set_number = addr%(associativity*block_size*number_of_sets)
    set_number = int(set_number/(associativity*block_size))
    free_space = False
    blocks = cache[set_number]

    maxindex = 0
    max_time = cache[set_number][0][2]

    for i in range(len(blocks)):
        if (cache[set_number][i][2]>max_time):
            max_time = cache[set_number][i][2]
            maxindex = i


        if blocks[i][1]== -1:
            free_space = True
            cache[set_number][i][2] = 1
            page_starting = int(addr/block_size)
            cache[set_number][i][1] = (page_starting*block_size)
            for j in range(block_size):
                cache[set_number][i][0][j] = mem[(page_starting*block_size) + j]
            #print(cache[set_number][i][2]) 
            break
        else:
            cache[set_number][i][2]+=1
            #print(cache[set_number][i][2])

    if free_space is False:
        
        cache[set_number][maxindex][2] = 0
        page_starting = int(addr/block_size)
        cache[set_number][maxindex][1] = (page_starting*block_size)
        for j in range(block_size):
            cache[set_number][maxindex][0][j] = mem[(page_starting*block_size) + j]



#   for set in cache[0][set_number]:
# this set find the address whether it is present or not

def find_addr(addr,cache,associativity,block_size,number_of_sets):
    found_addr  = -1
    set_number = addr%(associativity*block_size*number_of_sets)
    set_number = int(set_number/(associativity*block_size))

    blocks = cache[set_number]
    page_starting = int(addr/block_size)
    for i in range(len(blocks)):
            if (page_starting*block_size) == cache[set_number][i][1] :
                #print("hello")
                found_addr = i
                cache[set_number][i][2] = 0
                break

    return found_addr
# this update the block with the new value 
def update_value(addr,value,cache,associativity,block_size,number_of_sets):
    found_addr  = False
    set_number = addr%(associativity*block_size*number_of_sets)
    set_number = int(set_number/(associativity*block_size))

    blocks = cache[set_number]
    page_starting = int(addr/block_size)
    for i in range(len(blocks)):
            if (page_starting*block_size) == cache[set_number][i][1] :
                found_addr = True
                offset = addr%block_size
                cache[set_number][i][0][int(offset)] = value
                cache[set_number][i][2] = 0
                #print("updated")
            cache[set_number][i][2]+=1

    return found_addr


# type 1 for fetching value 
# type 2 for writing the value
latency = 0
#update_value(addr,value,cache,associativity,block_size,number_of_sets)
Miss_In_L1 = 0
Miss_In_L2 = 0
instruction_L1 = 0
instruction_L2 = 0
def cache_working(addr,value,type):
    global latency,Miss_In_L1,Miss_In_L2,instruction_L1,instruction_L2
    if type == 1:
        latency+=l1_latency
        instruction_L1+=1
        found = find_addr(addr,cache_l1,assoc_l1,block_l1,set_l1)
        if found == -1:
            Miss_In_L1+=1
            #print("Not found in L1")
            cache_writing(addr,cache_l1,assoc_l1,block_l1,set_l1)
            instruction_L2+=1
            latency+= l2_latency
            found_l2 = find_addr(addr,cache_l2,assoc_l2,block_l2,set_l2)
            if found_l2 == -1:
                Miss_In_L2+=1
               #print("Not found in L2 ")
                cache_writing(addr,cache_l2,assoc_l2,block_l2,set_l2)
                latency+=mem_latency

    if type == 2:
        check_l1 = update_value(addr,value,cache_l1,assoc_l1,block_l1,set_l1)
        latency+=l1_latency
        instruction_L1+=1
        if check_l1 is False:
            Miss_In_L1+=1
            check_l2 = update_value(addr,value,cache_l2,assoc_l2,block_l2,set_l2)
            latency+=l2_latency
            instruction_L2+=1
            if check_l2 is false:
                Miss_In_L2+=1
    #print(latency)

mem_index=0    
reduce =0
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
        
f=open("bubblesort.s",'r')
text=f.readlines()
dataseg,command=sep(text)

special_mem=[]
#data segment works starts here FUN START NOW :)
#print(dataseg)

def ldword(words):
    global mem_index
    for word in words:
        mem[mem_index]=int(word)
        cache_working(mem_index,int(word),2)
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
    a=ord(rg[0])
    a=a-97
    regindex=(a*10 + int(rg[1]))
    
    rg = instr[2]
    memindex=int(rg[0:2]+rg[7:10],16)
    memindex=memindex/4
    cache_working(memindex,0,1)
    reg[regindex]=mem[memindex]
    
def loadadda(instr):
    #print('this is isntr',instr)
    regindex=0
    rg=instr[1]
    #print(rg)
    #print(ord(rg[0]))
    a=ord(rg[0])
    a=a-97
    regindex=(a*10 + int(rg[1]))
    
    reg[regindex]=instr[2]
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
    cache_working(memindex,reg[int(regindex)],2)
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
        cache_working(int(memindex),0,1)
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
        #print(reg)
        #print(rg)
        memindex=int(rg[0:2]+rg[7:10],16)
        memindex=memindex+int(instr[2])
        memindex=memindex/4
        #print(memindex,'dd')
        cache_working(int(memindex),0,1)
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
        cache_working(memindex,reg[int(regindex1)],2)
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
        cache_working(memindex,reg[int(regindex1)],2)
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
    temp1=str(reg[index[1]])
    #print(temp1)
    if len(temp1)>9:
        temp1=int(temp1[-3:],16)
        #print(temp1,"tmep1")
    else:
        temp1=-1
    
    temp2=str(reg[index[2]])
    
    if len(temp2)>9:
        temp2=int(temp2[-3:],16)
    else:
        temp2=-1
    
    
    if command[0] == 'add':
        #print("ADDED")
        if temp1!=-1 and temp2==-1:
            temp3 = temp1+reg[index[2]]
            #print(temp3,"value")
            temp3=hex(temp3)
            #print(temp3,"hex")
            temp3=str(temp3)
            temp3=temp3[2:]
            temp3='0x10000'+temp3
            reg[index[0]]=temp3
        elif temp1==-1 and temp2!=-1:
            temp3 = temp2+reg[index[1]]
            #print(temp3,"value")
            temp3=hex(temp3)
            #print(temp3,"hex")
            temp3=str(temp3)
            temp3=temp3[2:]
            temp3='0x10000'+temp3
            reg[index[0]]=temp3
        else: 
            reg[index[0]]=reg[index[1]]+reg[index[2]]
    elif command[0] == 'sub':
        #print("SUBTRACTED")
        reg[index[0]]=reg[index[1]]-reg[index[2]]
    elif command[0] == 'slt':
        if reg[index[1]]<reg[index[2]]:
            reg[index[0]]=1
        else:
            reg[index[0]]=0
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
    global reduce
    if instr[0] =='beq':
        if(reg[index[0]]==reg[index[1]]):
            #print("EQUAL")
            return ((srch(instr[3],command,g))-1)
        else:
            reduce+=1
            return g
    elif instr[0] =='bne':
        if(reg[index[0]]==reg[index[1]]):
             #print("EQUAL")
             reduce+=1
             return g
        else:
            return ((srch(instr[3],command,g))-1)
    else:
        print("INVALID SYNTAX")
        return g

g=-1
clean_instr_list=[]
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
        
        simplopr(instr)
        #print(instr)
        clean_instr_list.append(instr+[5])
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
            #print(instr)
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
            #print(instr)
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
            reduce-=1
            clean_instr_list.append(instr+[5])
    if flag is not True:  # for LW,LA,SW with register as reference 
        expr = re.compile('(\s*\w\w\s*\$\w\d\s*,(\s*(\d*\(\$\w\d\))|(0x\d*)))')   
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
            #print(instr)
            clean_instr_list.append(instr+[5])
            if instr[0]=='lw':
                #print("kload")
                loadwordr(instr)
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
g=-1   
print("--------------------------------------------Register-----------------------------------------------------\n\n") 
print(reg)
print("\n\n")
reg1=[]
for i in range(32):
    reg1.append([0,1])

print("---------cache_l1------")
print(cache_l1)
print("\n\n")

print("---------cache_l2------")
print(cache_l2)
print("\n\n")
print("---------------------------------------------Memory------------------------------------------------------\n\n")
print(mem)
print("===============================================================================================")
print("===============================================================================================\n")

def convert_to_index(command):
    index=[]
    for rg in command[1:-1]:
            #print(ord(rg[0]))
        a=ord(rg[0])
        a=a-97
        index.append(a*10 + int(rg[1]))   
    return index
def convert_to_index_address(command): # output format reg1 index(target) , reg1 2[index](address stored in this register) , offset/4 for finding the index in memory 
    index=[]
    reg1_index = (ord(command[1][0])-97)*10 + int(command[1][1])
    index.append(reg1_index)
    reg2_index = (ord(command[3][0])-97)*10 + int(command[3][1])
    index.append(reg2_index)
    index.append(int((int(command[2]))/4))
    return index
def branch_address(command): # out put format index[0] =reg1[1]  and index[1] = reg1[2]
    index=[]
    reg1_index = (ord(command[1][0])-97)*10 + int(command[1][1])
    index.append(reg1_index)
    reg2_index = (ord(command[2][0])-97)*10 + int(command[2][1])
    index.append(reg2_index)
    return index

# add->1 lw ->2 j -> 3  bne -> 4 beq ->6 addi -> 5 , la -> 7 sub -> 9||slt -> 8 
#addi,beq,la,slt,sub


def instruction_fetch(instruction):
    if instruction[0] == 'add': 
        # now we can enumerate our fetched instructions I'm giving 1 to the instruction add
        instruction[0]=1
    if instruction[0] == 'lw':
        instruction[0] = 2
    if instruction[0] =='j':
        instruction[0] = 3
    if instruction[0] =='bne':
        instruction[0] = 4
    if instruction[0] == 'addi':
        instruction[0]  = 5
    if instruction[0] == 'beq':
        instruction[0]  = 6
    if instruction[0] == 'la':
        instruction[0]  = 7
    if instruction[0] == 'slt':
        instruction[0]  = 8
    if instruction[0] == 'sub':
        instruction[0]  = 9
    instruction[-1]-=1  # indicating that this stage is done
def instruction_decode(instruction):
    #print("instruction -> decode : ",instruction)
    dependency = False
    instruction[-1]-=1
    if instruction[0] == 4 or instruction[0] == 6:
        #print("Its the branch instruction")
        index = branch_address(instruction)
        #print(index)
        if reg1[index[1]][1]==0 or reg1[index[0]][1]==0:
            #print(reg1)
            dependency =True
            instruction[-1]+=1
            return 0,dependency
        return 1,dependency 
    # bne and beq above    
    if instruction[0] == 2: # this means we are in the lw instruction
        #print(instruction, "here comes the indexes")
        index = convert_to_index_address(instruction)
        reg1[index[0]][1] = 0 
    if instruction[0] == 7:
        #print(instruction, "here comes the indexes")
        index = (ord(instruction[1][0])-97)*10 + int(instruction[1][1])
        reg1[index][1] = 0 
    return 0,dependency
    #right now i don't think that we need to do anything in the decoding part for add as such for now


def instruction_execution(instruction,laches):
    instruction[-1]-=1
    dependency =False
    execution_lache =[]   # for data forwarding we need the laches result to forward it in the next stage
    if instruction[0] == 1 or instruction[0] == 9 or instruction[0] == 8:
         # this means that the instruction is add
        index=[]
        for rg in instruction[1:4]:
        #print(ord(rg[0]))
            a=ord(rg[0])
            a=a-97
            index.append(a*10 + int(rg[1]))
        #print(index)
        # now the index stores the references of all the registers index[0]-> target register index[1],index[2] -> one that should be added
        if reg1[index[1]][1]==0 or reg1[index[2]][1]==0: # value is not updated which should be at that time
            dependency = True
            instruction[-1]+=1
            #print("dependency is there ",i)
            return execution_lache,dependency   # the true value of dependency shows the depency on the other instructions
        
        execution_lache.append((reg1[index[0]][0],index[0]))

    if instruction[0] == 2: # this means we are in the lw instruction
        #print(instruction, "here comes the indexes")
        index = convert_to_index_address(instruction)
        #print(index) 
        reg1[index[0]][1] = 0
        if reg1[index[1]][1] ==0:
            dependency =True
            instruction[-1]+=1
            #print("dependency",dependency)
            return execution_lache,dependency
         # memory is out of date            
    if instruction[0] == 7:
        #print(instruction, "here comes the indexes")
        index = (ord(instruction[1][0])-97)*10 + int(instruction[1][1])
        reg1[index][1] = 0 # memory is out of date            
        #print(index) 
        #print(reg1)
    if instruction[0] == 5:
         # this means that the instruction is add
        index=[]
        for rg in instruction[1:3]:
        #print(ord(rg[0]))
            a=ord(rg[0])
            a=a-97
            index.append(a*10 + int(rg[1]))
        #print(index)
        # now the index stores the references of all the registers index[0]-> target register index[1],index[2] -> one that should be added
        if reg1[index[1]][1]==0: # value is not updated which should be at that time
            dependency = True
            instruction[-1]+=1
            #print("im breakning at ",i)
            return execution_lache,dependency   # the true value of dependency shows the depency on the other instructions
        #print(instruction)
        #print(reg1)
        #print("register are",reg1[index[0]][0],reg1[index[1]][0],reg1[index[2]][0])
        #reg1[index[0]][0]=int(reg1[index[1]][0])+int(instruction[3])
        execution_lache.append((reg1[index[0]][0],index[0]))

    return execution_lache,dependency

def instruction_memory_back(instruction):
    instruction[-1]-=1
    index_update = -1
    if instruction[0] ==2:   # updating the value of the target register here 
    # One thing to keep in mind is that we cant make the dirty bit 1 here as the other instruction EX will then be runned in the same cycle
        index = convert_to_index_address(instruction)
        #print(index)
        index_update = index[0] # now it can be used further
    if instruction[0] == 7:
        index = (ord(instruction[1][0])-97)*10 + int(instruction[1][1])
        index_update = index
    return index_update    

def instruction_write_back(instruction,instruction_list,instruction_index):
    instruction[-1]-=1
    index_update =-1
    if instruction[0] == 1 or instruction[0] == 9:
        index=[]
        for rg in instruction[1:-1]:
            #print(ord(rg[0]))
            a=ord(rg[0])
            a=a-97
            index.append(a*10 + int(rg[1]))    
        index_update = index[0]
    instruction_list.pop(instruction_index)
    return index_update
  # 1->add
  # 2->lw          


cycles=0
execution_lache =[]
intr_len = len(clean_instr_list)
#print(clean_instr_list)
while(len(clean_instr_list)!=0):
    i=0
    index_update = -1
    stages_flag = [False,False,False,False,False]  # for making sure that each stage should be used once in a cycle
    while(i < len(clean_instr_list)):
        #print("starting instructions  ",clean_instr_list)
        if(clean_instr_list[i][-1]==5 and stages_flag[0] is not True):
            instruction_fetch(clean_instr_list[i])
            stages_flag[0] = True
            #print("instruction fetched-> ",clean_instr_list[i])

        elif(clean_instr_list[i][-1]==4 and stages_flag[1] is not True):
            stall,dependency = instruction_decode(clean_instr_list[i])
            if dependency is True:
             #   print(" branch break")
                break
            #print("stalls------->",stall)
            cycles = cycles + stall
            stages_flag[1] = True
            #print("instruction decode ->",clean_instr_list[i])

        elif(clean_instr_list[i][-1]==3 and stages_flag[2] is not True):
            #print("inside the execution_lache")
                #index = convert_to_index(instruction)
            if clean_instr_list[i][0] == 1 or clean_instr_list[i][0] == 5 or clean_instr_list[i][0]== 9 or clean_instr_list[0]==8:    
                execution_lache,dependency = instruction_execution(clean_instr_list[i],execution_lache)
                if dependency is True:
                 #   print("im breakning for add like instruction ",i)
                    break
                #print(clean_instr_list[i])
            elif clean_instr_list[i][0] == 2:
                #print("this is the lw instruction -------------------")
                #print(reg1)
                execution_lache,dependency = instruction_execution(clean_instr_list[i],execution_lache)
                
                if dependency is True:
                    #print("im breakning at ",i)
                    break
            else:
                execution_lache,dependency = instruction_execution(clean_instr_list[i],execution_lache)
                if dependency is True:
                    #print("im breakning at ",i)
                    break
            stages_flag[2] = True
            #print("execution_unit -> ",clean_instr_list[i])


        elif(clean_instr_list[i][-1]==2 and stages_flag[3] is not True):
            #print("inside the memory back")
            index_update = instruction_memory_back(clean_instr_list[i])
            #print("index_updated is ",index_update)
            stages_flag[3] = True
            #print(clean_instr_list[i])

        elif(clean_instr_list[i][-1]==1 and stages_flag[4] is not True):
            index_update = instruction_write_back(clean_instr_list[i],clean_instr_list,i)
            stages_flag[4] = True
            i-=1
            #print(clean_instr_list[i])
        i+=1
    if index_update!=-1:    
        reg1[index_update][1] = 1
    
    cycles+=1
    #print('the cycles compiled are ',cycles,"  ",clean_instr_list)
    # if run ==0:
    #     exit(0)
cycles = cycles - reduce
print(" NUMBER OF STALLS ARE : ",(cycles-intr_len-4))
print(" CYCLES ARE(without adding latency due to misses) : ",cycles)
print(" MISS rate in L1 cache :",Miss_In_L1/instruction_L1)
print(" Miss rate in L2 cache :",Miss_In_L2/instruction_L2)
print(" Latency Due to misses:",latency)
print(" IPC(without latency) : ",(intr_len/cycles))
print(" IPC : ",intr_len/(cycles+latency))
print("===============================================================================================")
print("===============================================================================================\n")
