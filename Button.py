from tkinter import *
from main import *
import os

root = Tk()

global is_on
is_on = True

my_label = Label(root,
                 text="Translator",
                 fg="green",
                 font=("Helvetica", 32))

my_label.pack(pady=20)


def switch():
    global is_on
    if is_on:
        on_button.config(image=off)
        is_on = False

    else:
        on_button.config(image=on)
        is_on = True






on = PhotoImage(file="Images/on.png")
off = PhotoImage(file="Images/off.png")

on_button = Button(root, image=on, bd=0, command=switch)
on_button.pack(pady=50)

root.mainloop()
