from Flask.Client import Client
from tkinter import *

def tester(client):
    print(client)


root = Tk()


test = tester(Client(root))