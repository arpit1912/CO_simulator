
import re

reg=[]
for i in range(32):
    reg.append(0)

reg[1]=20
reg[2]=20

mem=[]
for i in range(1024):
    mem.append(0)

mem_index=0    
#print(reg)

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
def run_once(xhe):
    global g
    if g==(len(command)-1):
        g=-1
    g+=1
    #print(g)
    test=command[g]
    #print(test)
    sep = '//'
    if test is '\n':
        return
    rest = test.split(sep, 1)[0]
    if not rest:
        return
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
        print(instr)
    
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
        return
    for i in range(32):
        lab[i]['text']=text=dic[i]+' = '+str(reg[i])
    mylist.delete(0,'end')
    for i in range(1024):
        ind=hex(i*4)
        ind=str(ind[2:])
        while len(ind)<3:
            ind='0'+ind
        mylist.insert(END, '0x10000'+ind+' = ' + str(mem[i]))
    mylist.pack( side = TOP,expand=True, fill = BOTH )
def run_all_at_once(xhe):
    global g
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
            print(instr)
        
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
    for i in range(32):
        lab[i]['text']=text=dic[i]+' = '+str(reg[i])
    mylist.delete(0,'end')
    for i in range(1024):
        ind=hex(i*4)
        ind=str(ind[2:])
        while len(ind)<3:
            ind='0'+ind
        mylist.insert(END, '0x10000'+ind+' = ' + str(mem[i]))
    mylist.pack( side = TOP,expand=True, fill = BOTH )















from tkinter import *
from functools import partial

root = Tk()
root.geometry("1200x600")

left = Frame(root, borderwidth=1, relief="solid")
#left.geometry("300x130")

right = Frame(root, borderwidth=1, relief="solid")
container = Frame(left, borderwidth=0.5, relief="solid")
button_section = Frame(left,borderwidth=0.5,relief ="solid")

#label1 = Label(container, text="I could be a canvas, but I'm a label right now")
#label2 = Label(button_section, text="I could be a button")
#label3 = Label(button_section, text="So could I")
line_by_line = Button(button_section, 
                   text="ONE LINE", 
                   fg="blue",
                   command=partial(run_once, 2))
all_line = Button(button_section, 
                   text="All LINES", 
                   fg="red",
                   command=partial(run_all_at_once, 2))

lab=[]
dic={0:'a0',1:'a1',2:'a2',3:'a3',4:'a4',5:'a5',6:'a6',7:'a7',8:'a8',9:'a9',
     10:'b0',11:'b1',12:'b2',13:'b3',14:'b4',15:'b5',16:'b6',17:'b7',18:'b8',19:'b9',
     20:'c0',21:'c1',22:'c2',23:'c3',24:'c4',25:'c5',26:'c6',27:'c7',28:'c8',29:'c9',
     30:'d0',31:'d1'}
for i in range(32):
    
    lab1=Label(container, text=dic[i]+' = '+str(reg[i]))
    lab1.pack(side="top")
    lab.append(lab1)
lab_mem=[]  
scrollbar = Scrollbar(right)
scrollbar.pack(side = RIGHT,fill =Y)
mylist=Listbox(right,yscrollcommand =scrollbar.set,height=100)
  
for i in range(1024):
        ind=hex(i*4)
        ind=str(ind[2:])
        while len(ind)<3:
            ind='0'+ind
        mylist.insert(END, '0x10000'+ind+' = ' + str(mem[i])) 
mylist.pack( side = TOP,expand=True, fill = BOTH )
scrollbar.config( command = mylist.yview )

left.pack(side="left", expand=True, fill="both")
right.pack(side="right", expand=True, fill="both")
button_section.pack(side="top",padx=5,pady=5)
container.pack(expand=True, fill="both", padx=5, pady=5)

#label1.pack()
#label2.pack(side="left",padx=5,pady=5)
#label3.pack(side="right",padx=5,pady=5)

line_by_line.pack(side="left",expand=True,fill="both",padx=5,pady=5)
all_line.pack(side="right",expand=True,fill="both",padx=5,pady=5)
root.mainloop()