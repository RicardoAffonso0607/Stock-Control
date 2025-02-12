from Screens.Screen import *
from Database.DadosUsuario import *
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class UserRegistrationScreen(Screen):

    def __init__(self, parent, controller) -> None:
        super().__init__(parent, controller)
        self.dbUsuario = DadosUsuario()

        # Tema
        self.style = ttk.Style(theme="cosmo")

        # Fundo
        self.configure(bg=self.style.colors.get("light"))

        # Centralização
        content_frame = ttk.Frame(self)
        content_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Ícone (rosto de usuário)
        label_icone = ttk.Label(
            content_frame,
            text="👤",  # Emoji de rosto
            font=("Arial", 100),  # Tamanho grande para o emoji
            bootstyle="primary"
        )
        label_icone.pack(side="top", anchor="center", pady=(0, 20))

        # Rótulo do título
        label_titulo = ttk.Label(
            content_frame, 
            text="Cadastro de Usuários", 
            font=("Helvetica", 30, "bold"),  
            bootstyle="dark"
        )
        label_titulo.pack(pady=10)

        # Campo para nome
        label_nome = ttk.Label(content_frame, text="Nome:", font=("Helvetica", 12), bootstyle="dark")
        label_nome.pack(pady=5)
        self.entry_nome = ttk.Entry(content_frame, font=("Helvetica", 12), width=30)
        self.entry_nome.pack(pady=5)

        # Campo para login
        label_login = ttk.Label(content_frame, text="Login:", font=("Helvetica", 12), bootstyle="dark")
        label_login.pack(pady=5)
        self.entry_login = ttk.Entry(content_frame, font=("Helvetica", 12), width=30)
        self.entry_login.pack(pady=5)

        # Campo para senha
        label_senha = ttk.Label(content_frame, text="Senha:", font=("Helvetica", 12), bootstyle="dark")
        label_senha.pack(pady=5)
        self.entry_senha = ttk.Entry(content_frame, font=("Helvetica", 12), width=30, show="*")
        self.entry_senha.pack(pady=5)

        # Botões para o nível de acesso
        self.nivel_acesso = tk.IntVar(value=3)

        access_frame = ttk.Frame(content_frame)
        access_frame.pack(pady=10)

        admin_rb = ttk.Radiobutton(access_frame, text="Admin", variable=self.nivel_acesso, value=1, bootstyle="primary")
        admin_rb.pack(side="left", padx=10)

        mod_rb = ttk.Radiobutton(access_frame, text="Moderador", variable=self.nivel_acesso, value=2, bootstyle="primary")
        mod_rb.pack(side="left", padx=10)

        user_rb = ttk.Radiobutton(access_frame, text="Usuário", variable=self.nivel_acesso, value=3, bootstyle="primary")
        user_rb.pack(side="left", padx=10)

        # Botão para cadastrar
        botao_cadastrar = ttk.Button(
            content_frame, 
            text="Cadastrar", 
            bootstyle="success", 
            width=25,  
            padding=10,  
            command=self.cadastrar
        )
        botao_cadastrar.pack(pady=10)

        # Botão para voltar
        botao_voltar = ttk.Button(
            content_frame, 
            text="Voltar", 
            bootstyle="secondary", 
            width=25,  
            padding=10,  
            command=lambda: controller.show("ProductsScreen")
        )
        botao_voltar.pack(pady=10)

    def cadastrar(self):
        nome = self.entry_nome.get()
        login = self.entry_login.get()
        senha = self.entry_senha.get()
        nivel_acesso = self.nivel_acesso.get()

        if not nome or not login or not senha:
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return

        if self.dbUsuario.existeUsuario(login):
            messagebox.showerror("Erro", "Esse login já está cadastrado!")
            return

        novo_usuario = Usuario(
            id=None,
            create_time=None,
            nome=nome,
            login=login,
            senha=senha,
            nivel_acesso=nivel_acesso
        )

        self.dbUsuario.createUsuario(novo_usuario)
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        self.entry_nome.delete(0, tk.END)
        self.entry_login.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)
        self.nivel_acesso.set(3)  # Reset para o valor padrão