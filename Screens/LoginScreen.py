from Screens.Screen import *
from Database.DadosUsuario import *
from Config.Config import *
from ttkbootstrap import Style, ttk
import tkinter as tk

class LoginScreen(Screen):

    def __init__(self, parent, controller) -> None:
        super().__init__(parent, controller)
        self.dbUsuario = DadosUsuario()
        self.config = Config()

        # Tema
        self.style = Style(theme="cosmo")  

        # Fundo
        self.configure(bg=self.style.colors.get("light"))

        # Frame principal para centralizar a área de login
        content_frame = ttk.Frame(self)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")  # Centraliza na tela

        # Frame da área de login com borda
        login_frame = ttk.Frame(
            content_frame, 
            padding=20,  # Espaçamento interno
            bootstyle="light"  # Define a cor de fundo 
        )
        login_frame.pack(expand=True, fill="both")

        # Ícone (cadeado) sem fundo
        label_icone = ttk.Label(
            login_frame,
            text="🔒",  
            font=("Arial", 100),  
            foreground=self.style.colors.get("primary"),  # Define apenas a cor do texto
            background=self.style.colors.get("light"),  # Mantém o fundo igual ao da área de login
        )
        label_icone.pack(side="top", anchor="center", pady=(0, 20))

        # Campo para usuário
        label_login = ttk.Label(login_frame, text="Login:", font=("Arial", 12), bootstyle="dark", background=self.style.colors.get("light"))
        label_login.pack(pady=5)
        self.entry_login = ttk.Entry(login_frame, font=("Arial", 12), width=30)
        self.entry_login.pack(pady=5)

        # Campo para senha
        label_senha = ttk.Label(login_frame, text="Senha:", font=("Arial", 12), bootstyle="dark", background=self.style.colors.get("light"))
        label_senha.pack(pady=5)
        self.entry_senha = ttk.Entry(login_frame, font=("Arial", 12), width=30, show="*")
        self.entry_senha.pack(pady=5)

        # Botão para logar
        botao_logar = ttk.Button(
            login_frame, 
            text="Logar", 
            bootstyle="success", 
            width=25,  
            padding=10,  
            command=self.logar
        )
        botao_logar.pack(side="top", anchor="center", pady=15)

        # Botão para voltar
        botao_voltar = ttk.Button(
            login_frame, 
            text="Voltar", 
            bootstyle="secondary", 
            width=25,  
            padding=10,  
            command=lambda: controller.show("HomeScreen")
        )
        botao_voltar.pack(side="top", anchor="center", pady=15)

    def logar(self):
        login = self.entry_login.get()
        senha = self.entry_senha.get()
        if not login or not senha: 
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return

        if self.dbUsuario.verificarNomeESenha(login, senha) == False:
            messagebox.showerror("Erro", "Login e/ou senha incorretos")
            return
        else:
            messagebox.showinfo("Login", f"Bem-vindo, {login}!")
            self.config.setUsuarioAtual(self.dbUsuario.getUsuarioPorLogin(login))
            self.controller.show("ProductsScreen")
