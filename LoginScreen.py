import tkinter as tk
from tkinter import messagebox
from Database import *

class LoginScreen(tk.Frame):

    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.parent = parent 
        self.controller = controller
        self.db = Database()

        # Rótulo do título
        label_titulo = tk.Label(
            self, 
            text="Login", 
            font=("Arial", 20, "bold"), 
            bg="#f2f2f2", 
            fg="#333"
        )
        label_titulo.pack(pady=20)

        # Campo para usuário
        label_login = tk.Label(self, text="Login:", font=("Arial", 12), bg="#f2f2f2", fg="#333")
        label_login.pack(pady=5)
        self.entry_login = tk.Entry(self, font=("Arial", 12), width=30)
        self.entry_login.pack(pady=5)

        # Campo para senha
        label_senha = tk.Label(self, text="Senha:", font=("Arial", 12), bg="#f2f2f2", fg="#333")
        label_senha.pack(pady=5)
        self.entry_senha = tk.Entry(self, font=("Arial", 12), width=30, show="*")
        self.entry_senha.pack(pady=5)

        # Botão para logar
        botao_logar = tk.Button(
            self, 
            text="Logar", 
            font=("Arial", 14), 
            bg="#4CAF50", 
            fg="white", 
            width=10, 
            command=self.logar
        )
        botao_logar.pack(pady=10)

        # Botão para voltar
        botao_voltar = tk.Button(
            self, 
            text="Voltar", 
            font=("Arial", 14), 
            bg="#f44336", 
            fg="white", 
            width=10, 
            command=lambda:controller.show("HomeScreen")
        )
        botao_voltar.pack(pady=10)

    def logar(self):
        login = self.entry_login.get()
        senha = self.entry_senha.get()
        if not login or not senha: 
            messagebox.showwarning("Erro", "Preencha todos os campos!")

        if self.db.verificarNomeESenha(login, senha) == False:
            messagebox.showerror("Erro", "Login e/ou senha incorretos")
            return
        else:
            messagebox.showinfo("Login", f"Bem-vindo, {login}!")


        