#!/usr/bin/python3
import tkinter
from tkinter import *

top = tkinter.Tk()
#add code here
text = Text(top)
text.insert(INSERT, "Are you entering a file or a url?")
L1 = Label(top, text="File name")
L1.pack(side = LEFT)
E1 = Entry(top, bd = 5)
E1.pack(side = RIGHT)
top.mainloop()
