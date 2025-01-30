import tkinter as tk
from Screens.HomeScreen import HomeScreen
from Screens.LoginScreen import LoginScreen
from Screens.UserRegistrationScreen import UserRegistrationScreen
from Screens.ProductsScreen import ProductsScreen
from Screens.OrderScreen import OrderScreen
from Database.Database import *

class ScreenManager(tk.Tk):

    def __init__(self):
        super().__init__()

        self.state('zoomed')
        self.title("Stock Control")  
        self.resizable(True, True)
        self.minsize(width=800, height=800)
        self.update_idletasks()

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        self.frames = {}
        self.add_frame("HomeScreen", HomeScreen)
        self.add_frame("LoginScreen", LoginScreen)
        self.add_frame("UserRegistrationScreen", UserRegistrationScreen)
        self.add_frame("ProductsScreen", ProductsScreen)
        self.add_frame("OrderScreen", OrderScreen)

        self.show("HomeScreen")
        #self.show("ProductsScreen")

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
