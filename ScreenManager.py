import tkinter as tk
from HomeScreen import HomeScreen
from LoginScreen import LoginScreen
from UserRegistrationScreen import UserRegsitrationScreen
from ProductsScreen import ProductsScreen
from Database import *

class ScreenManager(tk.Tk):

    def __init__(self, db: Database):
        super().__init__()
        self.db = db

        self.geometry("1900x1200")  
        self.title("Stock Control")  
        self.resizable(True, True)
        self.minsize(width=800, height=800)
        self.update_idletasks()

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self.telas = (HomeScreen, LoginScreen)

        self.frames = {}
        self.add_frame("HomeScreen", HomeScreen)
        self.add_frame("LoginScreen", LoginScreen)
        self.add_frame("UserRegsitrationScreen", UserRegsitrationScreen)
        self.add_frame("ProductsScreen", ProductsScreen)

        self.show("HomeScreen")

    def add_frame(self, name, frame_class):
        """
        Adiciona uma tela ao dicionário frames
        """
        frame = frame_class(self.container, self)
        self.frames[name] = frame
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show(self, name):
        """
        Exibe a tela especificada pelo nome
        """
        if name not in self.frames:
            raise KeyError(f"Tela {name} não registrada.")
        frame = self.frames[name]
        frame.tkraise()

    def finalizar(self):
        self.destroy()
