# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 13:00:33 2020
@author: ARPIT
"""
import re
#add $s1,$s2,AA$s3
#print(re.split('sum','sum, sum '))
test='beq $s1, $zero ,help //sub $s1 , $s2, $s3'
sep = '//'
rest = test.split(sep, 1)[0]
print (rest)
expr=re.compile(' (\s*\w\w\w\s*\$\w\d\s*,\s*\$(\w\d|zero)\s*,\s*\$(\w\d|zero)\s*)')

"""
adding new regex expressions, check once
ADD/SUB/AND/SLT->  (\s*\w\w\w\s*\$\w\d\s*,\s*\$(\w\d|zero)\s*,\s*\$(\w\d|zero)\s*)
BNE/BEQ->  (\s*\w\w\w\s*\$(\w\d|zero)\s*,\s*\$(\w\d|zero)\s*,\s*(\w|\d)*\s*)
jump->   (\s*[j]\s*(\w|\d)*)
LW/SW->  (\s*\w\w\s*\$\w\d\s*,(\s*(\d\(\$\w\d\))|(0x\d*)))
jump register->   
@arpit: discuss LW,SW with me once
"""

mo=expr.search(rest)

if mo:
    ch=mo.group()
    ch=re.split('\W|,|$',ch)
    instr=[]
    for i in ch:
        if i:
            instr.append(i)
    print(instr)
#print(re.split('sum','sum arpit'))