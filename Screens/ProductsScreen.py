from Screens.Screen import *
from Database.DadosProduto import *
from Database.DadosUsuario import *
from Config.Config import *
import csv

class ProductsScreen(Screen):

    def __init__(self, parent, controller) -> None:
        super().__init__(parent, controller)
        self.dbProduto = DadosProduto()
        self.dbUsuario = DadosUsuario()
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
        self.exibirProdutos()

        # Evento de clicar duas vezes sobre um item
        self.product_table.bind("<Double-1>", self.editarProduto)

        # Botão para cadastrar novos usuarios
        botao_cadastrar_usuario = tk.Button(
            self, 
            text="Cadastrar novo usuario", 
            font=("Arial", 14), 
            bg="#4CAF50", 
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
            bg="#4CAF50", 
            fg="white", 
            width=20, 
            command=self.criarProduto
        )
        botao_cadastrar_produto.pack(padx=5)

        # Botão para criar um novo pedido
        botao_criar_pedido = tk.Button(
            self, 
            text="Criar novo pedido", 
            font=("Arial", 14), 
            bg="#4CAF50", 
            fg="white", 
            width=20, 
            command=self.criarPedido
        )
        botao_criar_pedido.pack(padx=5)

        # Botão para exportar para CSV
        botao_exportar_csv = tk.Button(
            self, 
            text="Exportar para CSV", 
            font=("Arial", 14), 
            bg="#4CAF50", 
            fg="white", 
            width=20, 
            command=self.exportarParaCSV
        )
        botao_exportar_csv.pack(padx=5)

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

    def exibirProdutos(self):
        produtos = self.dbProduto.getProdutos()
        produtos.sort(key=lambda x: x.getId()) # Organiza por ID
        for produto in produtos:
            self.product_table.insert("", tk.END, values=produto.getAll())
            if produto.getQuantidade() <= 0:
                messagebox.showwarning("Sem estoque", "O produto" + produto.getNome() + "está sem estoque")

    def atualizarProdutos(self):
        for item in self.product_table.get_children():
            self.product_table.delete(item)
        self.exibirProdutos()

    def registrarUsuario(self):
        usuario = self.config.getUsuarioAtual()  
        if usuario.getNivelAcesso() >= 3:
            return
        self.controller.show("UserRegistrationScreen")

    def criarPedido(self):
        self.controller.show("OrderScreen")

    def exportarParaCSV(self):
        with open("products.csv", "w", newline='') as myfile:
            csvwriter = csv.writer(myfile, delimiter=',')
        
            for id in self.product_table.get_children():
                row = self.product_table.item(id)["values"]
                csvwriter.writerow(row)

        messagebox.showinfo("Sucesso", "Arquivo exportado com sucesso!")

    def criarProduto(self):
        usuario = self.config.getUsuarioAtual()  
        if usuario.getNivelAcesso() >= 3:
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
            novo_produto = Produto()
            novo_produto.setNome(name_entry.get())
            novo_produto.setPreco(float(price_entry.get()))
            novo_produto.setQuantidade(int(quantity_entry.get()))
            novo_produto.setVendidos(int(solds_entry.get()))
            novo_produto.setDataValidade(validity_date_entry.get())

            # Validar dados
            if novo_produto.getNome() == None or novo_produto.getNome() == " ":
                messagebox.showerror("Erro", "Nome inválido!")
                return

            if novo_produto.getPreco() < 0:
                messagebox.showerror("Erro", "Preço inválido!")
                return

            if novo_produto.getQuantidade() < 0:
                messagebox.showerror("Erro", "Quantidade inválida!")
                return
            
            if novo_produto.getVendidos() < 0:
                messagebox.showerror("Erro", "Quantidade de itens vendidos inválidos!")
                return
            
            if not datetime.strptime(novo_produto.getDataValidade(), "%Y-%m-%d"):
                messagebox.showerror("Erro", "Data de validade inválida!")
                return

            id = self.dbProduto.criarProduto(novo_produto)
            new_product = self.dbProduto.getProdutoPorID(id)
            if new_product != None:
                messagebox.showinfo("Sucesso", "Produto criado com sucesso!")
                self.product_table.insert("", tk.END, values=new_product.getAll())
            else:
                messagebox.showerror("Erro", "Falha ao criar produto")
            new_product_window.destroy()

        def voltar():
            new_product_window.destroy()

        save_button = tk.Button(new_product_window, text="Criar", bg="#4CAF50", fg="white", command=salvarAlteracoes)
        save_button.pack(pady=10)

        voltar_button = tk.Button(new_product_window, text="Voltar", bg="#f44336", fg="white", command=voltar)
        voltar_button.pack(pady=10)

    def editarProduto(self, event):
        selected_item = self.product_table.selection()
        if not selected_item:
            return  
        
        usuario = self.config.getUsuarioAtual()  
        if usuario.getNivelAcesso() >= 3:
            return
        
        item = selected_item[0]
        values = self.product_table.item(item, "values")
        produto_selecionado = Produto(*values)

        # Criar uma nova janela
        edit_window = tk.Toplevel(self)
        edit_window.title("Editar Produto")
        edit_window.geometry("500x600")
        edit_window.transient(self)

        # Nome do produto
        label_titulo = tk.Label(
            edit_window, 
            text=f"{produto_selecionado.getNome()}", 
            font=("Arial", 18, "bold"), 
            bg="#f2f2f2", 
            fg="#333"
        )
        label_titulo.pack(pady=20)

        # Campos de edição
        tk.Label(edit_window, text="Preço:").pack(pady=5)
        price_entry = tk.Entry(edit_window)
        price_entry.insert(0, produto_selecionado.getPreco())
        price_entry.pack(pady=5)

        tk.Label(edit_window, text="Quantidade:").pack(pady=5)
        quantity_entry = tk.Entry(edit_window)
        quantity_entry.insert(0, produto_selecionado.getQuantidade())
        quantity_entry.pack(pady=5)

        tk.Label(edit_window, text="Data de Entrada:").pack(pady=5)
        entry_date_entry = tk.Entry(edit_window)
        entry_date_entry.insert(0, produto_selecionado.getDataEntrada())
        entry_date_entry.pack(pady=5)

        tk.Label(edit_window, text="Vendidos:").pack(pady=5)
        solds_entry = tk.Entry(edit_window)
        solds_entry.insert(0, produto_selecionado.getVendidos())
        solds_entry.pack(pady=5)

        tk.Label(edit_window, text="Data de validade:").pack(pady=5)
        validity_date_entry = tk.Entry(edit_window)
        validity_date_entry.insert(0, produto_selecionado.getDataValidade())
        validity_date_entry.pack(pady=5)

        # Botão para salvar alterações
        def salvarAlteracoes():
            produto_selecionado.setPreco(float(price_entry.get()))
            produto_selecionado.setQuantidade(int(quantity_entry.get()))
            produto_selecionado.setDataEntrada(entry_date_entry.get())
            produto_selecionado.setVendidos(int(solds_entry.get()))
            produto_selecionado.setDataValidade(validity_date_entry.get())

            # Validar dados
            if produto_selecionado.getPreco() < 0:
                messagebox.showerror("Erro", "Preço inválido!")
                return

            if produto_selecionado.getQuantidade() < 0:
                messagebox.showerror("Erro", "Quantidade inválida!")
                return
            
            if not datetime.strptime(produto_selecionado.getDataEntrada(), "%Y-%m-%d"):
                messagebox.showerror("Erro", "Data de entrada inválida!")
                return
            
            if produto_selecionado.getVendidos() < 0:
                messagebox.showerror("Erro", "Quantidade de itens vendidos inválidos!")
                return
            
            if not datetime.strptime(produto_selecionado.getDataValidade(), "%Y-%m-%d"):
                messagebox.showerror("Erro", "Data de validade inválida!")
                return

            # Atualizar o Treeview
            self.dbProduto.atualizarProduto(produto_selecionado)
            self.product_table.item(item, values=produto_selecionado.getAll())
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            edit_window.destroy()

        def excluirProduto():
            self.dbProduto.excluirProduto(int(produto_selecionado.getId()))
            self.product_table.delete(item)
            messagebox.showinfo("Sucesso", "Produto excluido com sucesso!")
            edit_window.destroy()

        save_button = tk.Button(edit_window, text="Salvar", bg="#4CAF50", fg="white", command=salvarAlteracoes)
        save_button.pack(pady=10)

        voltar_button = tk.Button(edit_window, text="Voltar", bg="#f44336", fg="white", command=edit_window.destroy)
        voltar_button.pack(pady=10)

        exluir_button = tk.Button(edit_window, text="Excluir", bg="#f44336", fg="white", command=excluirProduto)
        exluir_button.pack(pady=10)


        