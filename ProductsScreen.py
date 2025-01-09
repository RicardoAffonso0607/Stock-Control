import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Database import *
from datetime import datetime
from Config import *

class ProductsScreen(tk.Frame):

    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.parent = parent 
        self.controller = controller
        self.db = Database()
        self.config = Config()

        # Rótulo do título
        label_titulo = tk.Label(
            self, 
            text="Stock Control", 
            font=("Arial", 24, "bold"), 
            bg="#f2f2f2", 
            fg="#333"
        )
        label_titulo.pack(pady=20)

        # Treeviwe com os produtos
        scrollbar = ttk.Scrollbar(
            self, 
            orient="vertical"
        )
        scrollbar.pack(side="right", fill="y")

        self.product_table = ttk.Treeview(
            self, 
            columns=("ID", "Nome", "Preço", "Quantidade", "Data de entrada", "Vendidos", "Data de validade"),
            show="headings",
            height=15,
            yscrollcommand=scrollbar.set
        )
        self.product_table.pack(fill="both", expand=True)
        
        # Configuração das colunas
        self.product_table.heading("ID", text="ID")
        self.product_table.heading("Nome", text="Nome")
        self.product_table.heading("Preço", text="Preço")
        self.product_table.heading("Quantidade", text="Quantidade")
        self.product_table.heading("Data de entrada", text="Data de entrada")
        self.product_table.heading("Vendidos", text="Vendidos")
        self.product_table.heading("Data de validade", text="Data de validade")

        self.product_table.column("ID", width=50, anchor="center")
        self.product_table.column("Nome", width=150, anchor="center")
        self.product_table.column("Preço", width=100, anchor="center")
        self.product_table.column("Quantidade", width=100, anchor="center")
        self.product_table.column("Data de entrada", width=100, anchor="center")
        self.product_table.column("Vendidos", width=100, anchor="center")
        self.product_table.column("Data de validade", width=100, anchor="center")

        # Preenche a tabela
        self.popularTreeview()

        # Evento de clicar duas vezes sobre um item
        self.product_table.bind("<Double-1>", self.exibirAlteracoes)

        # Botão para cadastrar novos usuarios
        botao_cadastrar_usuario = tk.Button(
            self, 
            text="Cadastrar novo usuario", 
            font=("Arial", 14), 
            bg="#f44336", 
            fg="white", 
            width=20, 
            command=self.registrarUsuario
        )
        botao_cadastrar_usuario.pack(padx=5)

        # Botão para cadastrar novos produtos
        botao_cadastrar_produto = tk.Button(
            self, 
            text="Cadastrar novo produto", 
            font=("Arial", 14), 
            bg="#f44336", 
            fg="white", 
            width=20, 
            command=self.criarProduto
        )
        botao_cadastrar_produto.pack(padx=5)

        # Botão para voltar
        botao_voltar = tk.Button(
            self, 
            text="Voltar para tela inicial", 
            font=("Arial", 14), 
            bg="#f44336", 
            fg="white", 
            width=20, 
            command=lambda:controller.show("HomeScreen")
        )
        botao_voltar.pack(padx=5)

    def popularTreeview(self):
        produtos = self.db.getProdutos()
        produtos.sort(key=lambda x: x[0]) # Organiza por ID
        for produto in produtos:
            self.product_table.insert("", tk.END, values=produto)

    def registrarUsuario(self):
        usuario = self.db.getUsuarioPorLogin(self.config.getUsuarioAtual())  
        if usuario[5] >= 3:
            return
        self.controller.show("UserRegistrationScreen")

    def criarProduto(self):
        usuario = self.db.getUsuarioPorLogin(self.config.getUsuarioAtual())  
        if usuario[5] >= 3:
            return

        # Criar uma nova janela
        new_product_window = tk.Toplevel(self)
        new_product_window.title("Criar Produto")
        new_product_window.geometry("500x600")
        new_product_window.transient(self) 

        # Campos de edição
        tk.Label(new_product_window, text="Nome:").pack(pady=5)
        name_entry = tk.Entry(new_product_window)
        name_entry.pack(pady=5)

        tk.Label(new_product_window, text="Preço:").pack(pady=5)
        price_entry = tk.Entry(new_product_window)
        price_entry.pack(pady=5)

        tk.Label(new_product_window, text="Quantidade:").pack(pady=5)
        quantity_entry = tk.Entry(new_product_window)
        quantity_entry.pack(pady=5)

        tk.Label(new_product_window, text="Vendidos:").pack(pady=5)
        solds_entry = tk.Entry(new_product_window)
        solds_entry.pack(pady=5)

        tk.Label(new_product_window, text="Data de validade: formato (aaaa-mm-dd)").pack(pady=5)
        validity_date_entry = tk.Entry(new_product_window)
        validity_date_entry.pack(pady=5)

        # Botão para salvar alterações
        def salvarAlteracoes():
            new_product_name = name_entry.get()
            new_product_price = float(price_entry.get())
            new_product_quantity = int(quantity_entry.get())
            new_product_solds = int(solds_entry.get())
            new_product_validity_date = validity_date_entry.get()

            # Validar dados
            if new_product_name == None or new_product_name == " ":
                messagebox.showerror("Erro", "Nome inválido!")
                return

            if new_product_price < 0:
                messagebox.showerror("Erro", "Preço inválido!")
                return

            if new_product_quantity < 0:
                messagebox.showerror("Erro", "Quantidade inválida!")
                return
            
            if new_product_solds < 0:
                messagebox.showerror("Erro", "Quantidade de itens vendidos inválidos!")
                return
            
            if not datetime.strptime(new_product_validity_date, "%Y-%m-%d"):
                messagebox.showerror("Erro", "Data de validade inválida!")
                return

            new_product_id = self.db.criarProduto(
                nome=new_product_name,
                preco=new_product_price,
                quantidade=new_product_quantity,
                vendidos=new_product_solds,
                data_validade=new_product_validity_date
                )
            new_product = self.db.getProdutoPorID(new_product_id)
            if new_product != None:
                messagebox.showinfo("Sucesso", "Produto criado com sucesso!")
                self.product_table.insert("", tk.END, values=new_product)
            else:
                messagebox.showerror("Erro", "Falha ao criar produto")
            new_product_window.destroy()

        def voltar():
            new_product_window.destroy()

        save_button = tk.Button(new_product_window, text="Criar", bg="#4CAF50", fg="white", command=salvarAlteracoes)
        save_button.pack(pady=10)

        voltar_button = tk.Button(new_product_window, text="Voltar", bg="#f44336", fg="white", command=voltar)
        voltar_button.pack(pady=10)

    def exibirAlteracoes(self, eventoAcionado):
        selected_item = self.product_table.selection()
        if not selected_item:
            return  
        
        usuario = self.db.getUsuarioPorLogin(self.config.getUsuarioAtual())  
        if usuario[5] >= 3:
            return
        
        item = selected_item[0]
        values = self.product_table.item(item, "values")

        # Criar uma nova janela
        edit_window = tk.Toplevel(self)
        edit_window.title("Editar Produto")
        edit_window.geometry("500x600")
        edit_window.transient(self)  

        # Nome do produto
        label_titulo = tk.Label(
            edit_window, 
            text=f"{values[1]}", 
            font=("Arial", 18, "bold"), 
            bg="#f2f2f2", 
            fg="#333"
        )
        label_titulo.pack(pady=20)

        # Campos de edição
        tk.Label(edit_window, text="Preço:").pack(pady=5)
        price_entry = tk.Entry(edit_window)
        price_entry.insert(0, values[2])
        price_entry.pack(pady=5)

        tk.Label(edit_window, text="Quantidade:").pack(pady=5)
        quantity_entry = tk.Entry(edit_window)
        quantity_entry.insert(0, values[3])
        quantity_entry.pack(pady=5)

        tk.Label(edit_window, text="Data de Entrada:").pack(pady=5)
        entry_date_entry = tk.Entry(edit_window)
        entry_date_entry.insert(0, values[4])
        entry_date_entry.pack(pady=5)

        tk.Label(edit_window, text="Vendidos:").pack(pady=5)
        solds_entry = tk.Entry(edit_window)
        solds_entry.insert(0, values[5])
        solds_entry.pack(pady=5)

        tk.Label(edit_window, text="Data de validade:").pack(pady=5)
        validity_date_entry = tk.Entry(edit_window)
        validity_date_entry.insert(0, values[6])
        validity_date_entry.pack(pady=5)

        # Botão para salvar alterações
        def salvarAlteracoes():
            new_price = float(price_entry.get())
            new_quantity = int(quantity_entry.get())
            new_entry_date = entry_date_entry.get()
            new_solds = int(solds_entry.get())
            new_validity_date = validity_date_entry.get()

            # Validar dados
            if new_price < 0:
                messagebox.showerror("Erro", "Preço inválido!")
                return

            if new_quantity < 0:
                messagebox.showerror("Erro", "Quantidade inválida!")
                return
            
            if not datetime.strptime(new_entry_date, "%Y-%m-%d"):
                messagebox.showerror("Erro", "Data de entrada inválida!")
                return
            
            if new_solds < 0:
                messagebox.showerror("Erro", "Quantidade de itens vendidos inválidos!")
                return
            
            if not datetime.strptime(new_validity_date, "%Y-%m-%d"):
                messagebox.showerror("Erro", "Data de validade inválida!")
                return

            # Atualizar o Treeview
            updated_values = (
                values[0],  # ID
                values[1],  # Nome
                new_price,
                new_quantity,
                new_entry_date,
                new_solds,
                new_validity_date,
            )
            self.db.atualizarProduto(updated_values)
            self.product_table.item(item, values=updated_values)
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            edit_window.destroy()

        def excluirAlteracoes():
            self.db.excluirProduto(int(values[0]))
            self.product_table.delete(item)
            messagebox.showinfo("Sucesso", "Produto excluido com sucesso!")
            edit_window.destroy()

        save_button = tk.Button(edit_window, text="Salvar", bg="#4CAF50", fg="white", command=salvarAlteracoes)
        save_button.pack(pady=10)

        exluir_button = tk.Button(edit_window, text="Excluir", bg="#f44336", fg="white", command=excluirAlteracoes)
        exluir_button.pack(pady=10)


        