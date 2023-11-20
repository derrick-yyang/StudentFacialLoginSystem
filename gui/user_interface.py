from tkinter import *

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


    def show_tkinter_hello(name,result):
        root = Tk()
        app = Application(master=root)
        app.master.title('Welcome ' + name)
        #student_id, name, DAY(login_date), MONTH(login_date), YEAR(login_date)
        message = Label(root, text = 'Student_id is ' + str(result[0]) + ' | Login Time: ' + str(result[2]) + '/' + str(result[3]) + '/' + str(result [4]))
        message.pack()
        app.mainloop()

    def show_tkinter_first(name,result):
        root = Tk()
        app = Application(master=root)
        app.master.title('Welcome ' + name)
        #student_id, name, DAY(login_date), MONTH(login_date), YEAR(login_date)
        message = Label(root, text = 'Student_id is ' + str(result[0]) + ' | Login Time: ' + str(result[2]) + '/' + str(result[3]) + '/' + str(result [4]))
        message.pack()
        app.mainloop()