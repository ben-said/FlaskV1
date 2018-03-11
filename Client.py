from tkinter import *
from tkinter import ttk

OPTIONS = ['Django', 'Elektra', 'Highlander', 'Matrix']

class Client:
    def __init__(self, master):
        self.frame = Frame(master, bd=1)
        self.frame2 = Frame(master, bd=2)
        self.frame3 = Frame(master, bd=3)

        self.frame3.pack(padx=5, pady=5)
        self.frame2.pack(padx=5, pady=5)


        self.v = StringVar()
        a = ttk.Radiobutton(self.frame2, text='Django', variable=self.v, value='Django').pack()
        b = ttk.Radiobutton(self.frame2, text='Elektra', variable=self.v, value='Elektra').pack()
        c = ttk.Radiobutton(self.frame2, text='Highlander', variable=self.v, value='Highlander').pack()
        d = ttk.Radiobutton(self.frame2, text='Matrix', variable=self.v, value='Matrix').pack()

        self.button = ttk.Button(master, text='Cancel', command=self.frame.quit)
        self.button.pack(side=RIGHT, padx=15, pady=5)

        self.okbut = ttk.Button(master, text='OK', command=self.getcli)
        self.okbut.pack(side=LEFT, padx=15, pady=5)




    def getcli(self):
        clientname = self.v.get()
        w = Message(self.frame, text="Please select a client!")

        if clientname in OPTIONS:
            #print("The client should be: " + str(clientname))
            root.destroy()
            client = str(clientname)
            return client
        else:
            self.frame.pack(padx=5, pady=  5)
            w.pack()


root = Tk()

app = Client(root)

root.mainloop()
