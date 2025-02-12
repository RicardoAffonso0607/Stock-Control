from Screens.Screen import *

class HomeScreen(Screen):

    def __init__(self, parent, controller) -> None:
        super().__init__(parent, controller)

        # Tema
        self.style = ttk.Style(theme="cosmo")  

        # Fundo
        self.configure(bg=self.style.colors.get("secondary"))

        # Centralização
        content_frame = ttk.Frame(self)
        content_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Ícone (caixa)
        label_icone = ttk.Label(
            content_frame,
            text="📦",  
            font=("Arial", 100),  
            bootstyle="primary"
        )
        label_icone.pack(side="top", anchor="center", pady=(0, 20))

        # Rótulo título
        label_titulo = ttk.Label(
            content_frame, 
            text="Stock Control", 
            font=("Helvetica", 50, "bold"),  
            bootstyle="dark"  
        )
        label_titulo.pack(side="top", anchor="center", pady=(0, 40))

        # Botão de Login
        botao_login = ttk.Button(
            content_frame, 
            text="Login", 
            bootstyle="success", 
            width=25,  
            padding=10,  
            command=lambda: controller.show("LoginScreen")
        )
        botao_login.pack(side="top", anchor="center", pady=15)

        # Botão de Sair
        botao_sair = ttk.Button(
            content_frame, 
            text="Sair", 
            bootstyle="danger", 
            width=25,  
            padding=10,  
            command=lambda: controller.destroy()
        )
        botao_sair.pack(side="top", anchor="center", pady=15)