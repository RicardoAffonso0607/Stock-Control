from Screens.Screen import *

class OrderScreen(Screen):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # Rótulo do título
        label_titulo = tk.Label(
            self, 
            text="Criar Pedido", 
            font=("Arial", 20, "bold"), 
            bg="#f2f2f2", 
            fg="#333"
        )
        label_titulo.pack(pady=20)

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