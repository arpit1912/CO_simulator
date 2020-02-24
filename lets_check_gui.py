# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 00:39:59 2020

@author: ARPIT
"""



arr=[]
arr.append(12)

arr.append(2)

arr.append(1223)

arr.append(1212)


from tkinter import *
master = Tk() 
for i in range(len(arr)):
    Label(master, text='reg['+str(i)+'] = '+str(arr[i])).grid(row=i) 
#Label(master, text='Last Name').grid(row=1) 
#e1 = Entry(master) 
#e2 = Entry(master) 
#e1.grid(row=0, column=1) 
#e2.grid(row=1, column=1) 
mainloop() 
#print(e1)
=======

