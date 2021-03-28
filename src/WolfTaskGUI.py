#!/usr/bin/python3
import tkinter
from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter import simpledialog
from CalendarAPI import *
from TasksAPI import *

def openfile():
    file = askopenfile(mode = 'r', filetype=[('iCalendar File', '*.ics')])
    if file is not None:
        content = file.read()
        return file.name

def submit(auth, top, v, v2):
    bool_url = True
    styleChoice = v2.get()
    if v.get() == 0:
        path = simpledialog.askstring("URL", "Enter URL below", parent = top)
        print(url)
        bool_url = True
    elif v.get() == 1:
        path = openfile()
        bool_url = False
    addAllTasks(auth, getTasksFromCalendar(bool_url, path, styleChoice))
    

def main(auth):
    top = tkinter.Tk()
    top.title('WolfTasks')
    top.geometry("600x500")
    lbl=Label(top, text="WolfTasks", fg="red", font=("IrisUPC",50))
    lbl.place(x=130,y=50)          

    Label(top, text = "Select either option URL or File:").place(x = 130, y = 230)
    Label(top, text = "Then click Proceed!").place(x = 245, y = 350)
    v = IntVar()
    v.set(0)
    offset = 0
    OPTIONS = [('URL', 0), ('File (.ical)', 1)]
    STYLE = [('Style 1 [CSC236]', 1), ('Style 2 CSC236:', 0)]
    for language, val in OPTIONS:
        Radiobutton(top,
                    text = language,
                    padx = 20,
                    variable = v,
                    value = val).place(x = 175, y = 250 + offset)
        offset += 20

    Label(top, text = "Select display style 1 or 2:").place(x = 350, y = 230)
    v2 = IntVar()
    v2.set(0)
    offset = 0
    for language, val in STYLE:
        Radiobutton(top,
                    text = language,
                    padx = 20,
                    variable = v2,
                    value = val).place(x = 350, y = 250 + offset)
        offset += 20

    proceed = Button(top, text = 'Proceed', command=lambda:submit(auth, top, v, v2)).pack(side = BOTTOM)

    top.mainloop() 


if __name__ == '__main__':
    auth = checkAuth()
    main(auth)