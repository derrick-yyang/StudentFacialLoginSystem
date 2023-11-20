from tkinter import *
import tkinter.messagebox as messagebox


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.createWidgets()
        
    def createWidgets(self):
        self.alertButton = Button(self, text='login', command=self.hello)
        self.alertButton.pack()
    
    # the window after login
    def hello(self):
        messagebox.showinfo('Message', 'Hello')





