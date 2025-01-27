import tkinter as tk
from tkinter import messagebox
import Screens.ScreenManager as ScreenManager

class Screen(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller