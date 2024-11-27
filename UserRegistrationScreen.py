import tkinter as tk
from tkinter import messagebox
from Database import *

class UserRegsitrationScreen(tk.Frame):

    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.parent = parent 
        self.controller = controller
        self.db = Database()
        self.nivel_acesso = 0

        # Rótulo do título
        label_titulo = tk.Label(
            self, 
            text="Cadastro de Usuarios", 
            font=("Arial", 20, "bold"), 
            bg="#f2f2f2", 
            fg="#333"
        )
        label_titulo.pack(pady=20)

        # Campo para nome
        label_nome = tk.Label(self, text="Nome:", font=("Arial", 12), bg="#f2f2f2", fg="#333")
        label_nome.pack(pady=5)
        self.entry_nome = tk.Entry(self, font=("Arial", 12), width=30)
        self.entry_nome.pack(pady=5)

        # Campo para login
        label_login = tk.Label(self, text="Login:", font=("Arial", 12), bg="#f2f2f2", fg="#333")
        label_login.pack(pady=5)
        self.entry_login = tk.Entry(self, font=("Arial", 12), width=30)
        self.entry_login.pack(pady=5)

        # Campo para senha
        label_senha = tk.Label(self, text="Senha:", font=("Arial", 12), bg="#f2f2f2", fg="#333")
        label_senha.pack(pady=5)
        self.entry_senha = tk.Entry(self, font=("Arial", 12), width=30, show="*")
        self.entry_senha.pack(pady=5)

        # Botões para o nivel de acesso
        self.nivel_acesso = tk.IntVar(value=3)

        admin_rb = tk.Radiobutton(self, text="Admin", variable=self.nivel_acesso, value=1, font=("Arial", 10))
        admin_rb.pack(pady=10)

        mod_rb = tk.Radiobutton(self, text="Moderador", variable=self.nivel_acesso, value=2, font=("Arial", 10))
        mod_rb.pack(pady=10)

        user_rb = tk.Radiobutton(self, text="Usuário", variable=self.nivel_acesso, value=3, font=("Arial", 10))
        user_rb.pack(pady=10)

        # Botão para cadastrar
        botao_cadastrar = tk.Button(
            self, 
            text="Cadastrar", 
            font=("Arial", 14), 
            bg="#4CAF50", 
            fg="white", 
            width=10, 
            command=self.cadastrar
        )
        botao_cadastrar.pack(pady=10)

        # Botão para voltar
        botao_voltar = tk.Button(
            self, 
            text="Voltar", 
            font=("Arial", 14), 
            bg="#f44336", 
            fg="white", 
            width=10, 
            command=lambda:controller.show("ProductsScreen")
        )
        botao_voltar.pack(pady=10)

    def cadastrar(self):
        nome = self.entry_nome.get()
        login = self.entry_login.get()
        senha = self.entry_senha.get()
        if not login or not senha or not nome or self.nivel_acesso == 0: 
            messagebox.showwarning("Erro", "Preencha todos os campos!")

        if self.db.existeUsuario(login) == True:
            messagebox.showerror("Erro", "Esse login ja esta cadastrado")
            return
        else:
            self.db.createUsuario(nome, login, senha, self.nivel_acesso)
            messagebox.showinfo("Usuario cadastrado!")


        