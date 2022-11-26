from tkinter import *
import tkinter.messagebox as tmsg
from tkinter import ttk
from tkinter import filedialog

import pandas as pd
import numpy as np
import sys
import random
from collections import OrderedDict
from math import sqrt


root = Tk()
root.title("PYTOPS")
root.geometry("850x625")
root.resizable(0,0)

# function for raising frames
def raise_frame(frame):
    frame.tkraise()

# global variables
n=0
k=0
h=""
g=""
attri_type=[]
c=0.0
R=0
D=np.matrix('1')
B=np.matrix('1')
M=[]
size=0

# function for calculating outputs
def cal(a):
    global size,D
    
    def E(matrix_V, a):  
        data = OrderedDict()
        data['+ve'] = []
        data['-ve'] = []

        zipped = list(zip(*matrix_V))
        for i in range(len(matrix_V[0])):
            if a[i] == 1:
                data['+ve'].append(min(zipped[i]))
                data['-ve'].append(max(zipped[i]))
            else:
                data['+ve'].append(max(zipped[i]))
                data['-ve'].append(min(zipped[i]))
        return data
	 
	
    #Calculation of Separation Measure
    def S(matrix_V, L):
        data = OrderedDict()
        data['+ve'] = []
        data['-ve'] = []

        for i in range(len(matrix_V)):
            p_total = 0
            n_total = 0

            for j in range(len(matrix_V[i])):
                p_total += (matrix_V[i][j] - L['+ve'][j]) ** 2
                n_total += (matrix_V[i][j] - L['-ve'][j]) ** 2

            data['+ve'].append(sqrt(p_total))
            data['-ve'].append(sqrt(n_total))
        return data
		
	   

    #Calculating relative closeness to the Ideal Solution 	
    def Z(S):
        data = []
        for i in range(len(S['+ve'])):
            d = S['-ve'][i] / (S['+ve'][i] + S['-ve'][i])
            data.append(d)
        return data  
	

    def getProbability(array, position):
        count=0
        for i in array:
            if array[position]==i:
                count=count+1
        return(1 - (count/np.size(array)))


    #Constructing Weighted Normalized Decision Matrix
    for i in range(1,size+1):
        globals()["al%i" % i] = []
	
    array = np.array(Z(S(D,E(D,a))))
    order = array.argsort()[::-1]

    for i in range(1,size):
        eval("al"+str(i)).append(order[i]+1)

    global h
    h = h + str(C) 
    for i in order:
        h = h + ("Alternative" + str(i+1) + ">") +"\n"

    s1=[] 
	
    sortedarray = sorted(array, key=float)[::-1]
    s1.append(sortedarray)
    s1=np.array(s1)
	
 
    for i in range(1,size):
        names = ['Rank' + str(i)]
        probability = [getProbability(eval("al" + str(i)),0)]
        global g
        for row in zip(names,probability):
            g = g + str(row) 
            g+="\n"
		

	
    meanofsortedarray = np.mean(s1, axis=0)
    standdavofsortedarray = np.std(s1, axis=0)
	

    e1 = np.array(meanofsortedarray)
    e2 = np.arange(1,len(e1)+1)
    e = np.column_stack((e2,e1))
	

    f1 = np.array(standdavofsortedarray)
    f2 = np.arange(1,len(f1)+1)
    f = np.column_stack((f2,f1))
	
    return [e,f,g,h]

####### Frames  ##########

title = Frame(root, borderwidth=8, bg="light grey",highlightbackground="grey", highlightthickness=5)
title.place(x=0,y=0,width=850,height=120)

input1 = Frame(root, borderwidth=4, bg="lemon chiffon3")
input1.place(x=0,y=120,width=850,height=505)

input2 = Frame(root, borderwidth=4, bg="lemon chiffon3")
input2.place(x=0,y=120,width=1050,height=505)

output = Frame(root, borderwidth=4, bg="lemon chiffon3")
output.place(x=0,y=120,width=1050,height=505)

####### title frame #########

ti=Label(title,text="PyTOPS",font=("times new roman",30,"bold"),bg="light grey")
ti.place(x=300,y=10)

ti=Label(title,text="(A Python based tool for TOPSIS)",font=("times new roman",20,"bold"),bg="light grey")
ti.place(x=190,y=60)

########## Frame 1 ###########
def print_n():
    global n
    n=int(cl.get())

    ti=Label(input1,text="Input Each Attribute Type",font=("times new roman",15),bg="lemon chiffon3")
    ti.place(x=100,y=215)

    ti=Label(input1,text="(1 is for cost type and 0 for benefit type)",font=("times new roman",10),bg="lemon chiffon3")
    ti.place(x=100,y=240)

    k=0
    def create_list():
        global k
        p=ty.get()
        attri_type.append(int(ty.get()))
        ty.delete(0,END)
        k+=1
        if k==n: 
            typ.config(state=DISABLED) # next button disabled
            ti=Label(input1,text="Attribute Types: ",font=("times new roman",15),bg="lemon chiffon3")
            ti.place(x=100,y=380)
            te=Listbox(input1,width=40,height=1,font=("Cambria",14)) # attribute type list
            te.place(x=250,y=380)
            te.insert(END,attri_type)
            ent= Button(input1, text="Done",bg="forest green",font=("Cambria",13), width=12,borderwidth=0, command=lambda:raise_frame(input2))
            ent.place(x=300,y=420)

    ty= Entry(input1,width=30,font=("Cambria",14),highlightthickness=2)
    ty.place(x=100, y=280) 

    typ= Button(input1, text="Next",bg="grey",font=("Cambria",13), width=12,borderwidth=1, relief = SOLID,command=create_list)
    typ.place(x=320,y=325)   

ti=Label(input1,text="Inputs",font=("times new roman",20,"bold"),bg="lemon chiffon3")
ti.place(x=100,y=60)

ti=Label(input1,text="Number of Attributes",font=("times new roman",15),bg="lemon chiffon3")
ti.place(x=100,y=100)

cl= Entry(input1,width=30,font=("Cambria",14),highlightthickness=2)
cl.place(x=100, y=135) 

attri=Button(input1, text="Enter",bg="grey",font=("Cambria",13) ,width=12,borderwidth=1,relief = RAISED, command=print_n).place(x=320,y=180)

######### Frame 2 ###########
def open_file():
    global B,size
    filename = filedialog.askopenfilename(title="Open a File", filetypes=[("excel files", "*.xlsx")])

    if filename:
        try:
            filename = r"{}".format(filename)
            df1 = pd.read_excel(filename,engine='openpyxl',header=None)
            _matrix = df1.values.tolist()
            A = np.matrix(_matrix)
            size = df1.shape[0]

            #Normalizing the Decision Matrix
            from sklearn.preprocessing import normalize
            B = normalize(A, norm='l2', axis=0)

        except ValueError:
            attri2.config(text="File could not be opened")
        except FileNotFoundError:
            attri2.config(text="File Not Found")
    
def open_weights():
    global M
    filename = filedialog.askopenfilename(title="Open a File", filetypes=[("excel files", "*.xlsx")])
    if filename:
        try:
            filename = r"{}".format(filename)
            df2 = pd.read_excel(filename,engine='openpyxl',header=None)
            _matrix = df2.values.tolist()
            
            M=list(np.squeeze(np.asarray(_matrix)))

        except ValueError:
            attri2.config(text="File could not be opened")
        except FileNotFoundError:
            attri2.config(text="File Not Found")

ti2=Label(input2,text="Inputs",font=("times new roman",20,"bold"),bg="lemon chiffon3")
ti2.place(x=100,y=60)

ti2=Label(input2,text="Upload Decision Matrix",font=("times new roman",15),bg="lemon chiffon3")
ti2.place(x=100,y=100)

attri2=Button(input2, text="Decision Matrix",bg="sienna1", relief = RAISED,borderwidth=1, font=("Cambria",13) ,width=20,command=open_file)
attri2.place(x=100,y=160)

ti2=Label(input2,text="Upload Weights",font=("times new roman",15) ,bg="lemon chiffon3")
ti2.place(x=470,y=100)

attri2=Button(input2, text="Weights",bg="sienna1",relief = RAISED, borderwidth=1,font=("Cambria",13) , width=20, command=open_weights)
attri2.place(x=470,y=160)

ti2=Label(input2,text="Degree of variation in weights",font=("times new roman",15),bg="lemon chiffon3")
ti2.place(x=100,y=250)
ti2=Label(input2,text="(0.25 means you want 25% of variation in given weights)",font=("times new roman",10),bg="lemon chiffon3")
ti2.place(x=100,y=280)

cl2= Entry(input2,font=("Cambria",14),highlightthickness=2,width=16)
cl2.place(x=100, y=310) 

ti2=Label(input2,text="Number of simulations",font=("times new roman",15),bg="lemon chiffon3")
ti2.place(x=470,y=250)
ti2=Label(input2,text="(Simulation within the given variation in weights)",font=("times new roman",10),bg="lemon chiffon3")
ti2.place(x=470,y=280)

cl3= Entry(input2,font=("Cambria",14),highlightthickness=2,width=16)
cl3.place(x=470, y=310) 

########## Output #########

def save_c1():
    text_file=open('Rank_with_varying_weights.txt','w')
    text_file.write(lb1.get(1.0, END))
    text_file.close()

def save_b1():
    text_file=open('standard_deviation_relative_closeness.txt','w')
    text_file.write(lb4.get(1.0, END))
    text_file.close()

def save_a1():
    text_file=open('mean_relative_closeness.txt','w')
    text_file.write(lb3.get(1.0, END))
    text_file.close()

def save_d1():
    text_file=open('Probability_rank_reversal.txt','w')
    text_file.write(lb2.get(1.0, END))
    text_file.close()


ti3=Label(output,text="Outputs",font=("times new roman",20,"bold"),bg="lemon chiffon3")
ti3.place(x=70,y=60)

ti3=Label(output,text="Rank with varying weights",font=("times new roman",13),bg="lemon chiffon3")
ti3.place(x=70,y=100)

scrollbar=Scrollbar(output)
scrollbar.pack(side=RIGHT, fill=Y)
lb1 = Text(output, yscrollcommand = scrollbar.set,height=7,width=33)
lb1.place(x=70,y=130)
scrollbar.config(command=lb1.yview)

un=Button(output, text="Save",bg="forest green", width=10,borderwidth=0, command=save_c1).place(x=268,y=250)

ti4=Label(output,text="Probability of rank reversal",font=("times new roman",13),bg="lemon chiffon3")
ti4.place(x=400,y=100)

scrollbar=Scrollbar(output)
scrollbar.pack(side=RIGHT, fill=Y)
lb2 = Text(output,yscrollcommand = scrollbar.set,height=7,width=33)
lb2.place(x=400,y=130)
scrollbar.config(command=lb2.yview)

un=Button(output, text="Save",bg="forest green", width=10,borderwidth=0, command=save_d1).place(x=598,y=250)

ti5=Label(output,text="Mean of relative closeness to ideal solution",font=("times new roman",13),bg="lemon chiffon3")
ti5.place(x=70,y=275)

scrollbar=Scrollbar(output)
scrollbar.pack(side=RIGHT, fill=Y)
lb3 = Text(output, yscrollcommand = scrollbar.set,height=7,width=33)
lb3.place(x=70,y=305)
scrollbar.config(command=lb3.yview)

un=Button(output, text="Save",bg="forest green", width=10,borderwidth=0, command=save_a1).place(x=268,y=425)

ti4=Label(output,text="Standard deviation of relative closeness to ideal solution",font=("times new roman",13),bg="lemon chiffon3")
ti4.place(x=400,y=275)

scrollbar=Scrollbar(output)
scrollbar.pack(side=RIGHT, fill=Y)
lb4 = Text(output, yscrollcommand = scrollbar.set,height=7,width=33)
lb4.place(x=400,y=305)
scrollbar.config(command=lb4.yview)

un=Button(output, text="Save",bg="forest green", width=10,borderwidth=0, command=save_b1).place(x=598,y=425)

def run_cr_func():
    global c,R,M,B,D,C
    c=float(cl2.get())
    R=int(cl3.get())

    min1 = [x*(1-c) for x in M]
    max1 = [x*(1+c) for x in M]
    y1 = []
    for j in range(1,R+1):
        for i in range(len(M)):
            y =  random.uniform(min1[i], max1[i])
            y1.append(y)
        s = sum(y1)
        C = [ i/s for i in y1 ]
        y1=[]
    D=C*B

    raise_frame(output)
    [a1,b1,c1,d1] = cal(attri_type)

    for x in a1:
        lb3.insert(END,x)
    for x in b1:
        lb4.insert(END,x)
    lb1.insert(END,c1)
    lb2.insert(END,d1)

run=Button(input2, text="RUN",bg="forest green", width=15,relief = RAISED, borderwidth=1, command=run_cr_func).place(x=330,y=400)
raise_frame(input1)
root.mainloop()
