import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import Screens.ScreenManager as ScreenManager

class Screen(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller