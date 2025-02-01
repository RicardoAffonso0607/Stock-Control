from Screens.Screen import *
from Database.DadosPedido import *
from Database.DadosProduto import *

class OrderScreen(Screen):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.dbProduto = DadosProduto()
        self.dbPedido = DadosPedido()
        self.pedido = Pedido()
        self.quantidade_vendida = {}


        # Rótulo do título
        label_titulo = tk.Label(
            self, 
            text="Pedido", 
            font=("Arial", 20, "bold"), 
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

        # Tabela de produtos a serem vendidos
        self.product_table = ttk.Treeview(
            self, 
            columns=("ID", "Nome", "Preço", "Quantidade"),
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

        self.product_table.column("ID", width=50, anchor="center")
        self.product_table.column("Nome", width=200, anchor="center")
        self.product_table.column("Preço", width=150, anchor="center")
        self.product_table.column("Quantidade", width=150, anchor="center")

        # Evento de clicar duas vezes sobre um item
        self.product_table.bind("<Double-1>", self.EditarPedido)


        # Campo de observações do pedido
        tk.Label(self, text="Observações do Pedido:", font=("Arial", 14), bg="#f2f2f2", fg="#333").pack(pady=10)
        self.observations_entry = tk.Entry(self, font=("Arial", 14), width=50)
        self.observations_entry.pack(pady=10)

        # Rótulo do valor total
        self.label_valor_total = tk.Label(
            self, 
            text="Valor Total: R$ 0.00", 
            font=("Arial", 14), 
            bg="#f2f2f2", 
            fg="#333"
        )
        self.label_valor_total.pack(pady=10)


        # Botão para adicionar um produto
        botao_adicionar = tk.Button(
            self, 
            text="Adicionar Produto", 
            font=("Arial", 14), 
            bg="#4CAF50", 
            fg="white", 
            width=20, 
            command=self.addProduct
        )
        botao_adicionar.pack(pady=10)


        # Botão para finalizar o pedido
        botao_finalizar = tk.Button(
            self, 
            text="Finalizar Pedido", 
            font=("Arial", 14), 
            bg="#4CAF50", 
            fg="white", 
            width=20, 
            command=self.finalizarPedido
        )
        botao_finalizar.pack(pady=10)


        # Botão para voltar
        botao_voltar = tk.Button(
            self, 
            text="Voltar", 
            font=("Arial", 14), 
            bg="#f44336", 
            fg="white", 
            width=20, 
            command=lambda:controller.show("ProductsScreen")
        )
        botao_voltar.pack(pady=10)


    def EditarPedido(self, event):
        item = self.product_table.selection()[0]
        item_values = self.product_table.item(item, "values")
        
        # Criar uma nova janela
        new_order_window = tk.Toplevel(self)
        new_order_window.title("Editar Pedido")
        new_order_window.geometry("500x600")
        new_order_window.transient(self)

        # Campos de edição
        tk.Label(new_order_window, text="ID:").pack(pady=5)
        id_entry = tk.Entry(new_order_window)
        id_entry.insert(0, item_values[0])
        id_entry.config(state="disabled")
        id_entry.pack(pady=5)

        tk.Label(new_order_window, text="Nome:").pack(pady=5)
        name_entry = tk.Entry(new_order_window)
        name_entry.insert(0, item_values[1])
        name_entry.config(state="disabled")
        name_entry.pack(pady=5)

        tk.Label(new_order_window, text="Preço:").pack(pady=5)
        price_entry = tk.Entry(new_order_window)
        price_entry.insert(0, item_values[2])
        price_entry.config(state="disabled")
        price_entry.pack(pady=5)

        tk.Label(new_order_window, text="Quantidade:").pack(pady=5)
        quantity_entry = tk.Entry(new_order_window)
        quantity_entry.insert(0, item_values[3])
        quantity_entry.pack(pady=5)

        tk.Label(new_order_window, text="Observações:").pack(pady=5)
        observations_entry = tk.Entry(new_order_window)
        observations_entry.insert(0, item_values[4])
        observations_entry.pack(pady=5)

        # Botão para salvar alterações
        def salvarAlteracoes():

            product = self.dbProduto.getProdutoPorID(int(id_entry.get()))

            quantidade_anterior = self.quantidade_vendida[product.getId()]
            quantidade_atual = int(quantity_entry.get())

            diferenca = quantidade_atual - quantidade_anterior

            self.quantidade_vendida[product.getId()] = int(quantity_entry.get())

            self.pedido.setDataPedido(datetime.now().strftime("%Y-%m-%d"))
            self.pedido.addValorTotal(product.getPreco() * diferenca)
            self.pedido.setObservacoes(observations_entry.get())

            self.product_table.item(item, values=[product.getId(), product.getNome(), product.getPreco(), self.quantidade_vendida[product.getId()]])
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")

            self.label_valor_total.config(text=f"Valor Total: R$ {self.pedido.getValorTotal():.2f}")

            new_order_window.destroy()
        
        # Botão para excluir o produto
        def excluirProduto():

            product = self.dbProduto.getProdutoPorID(int(id_entry.get()))

            self.pedido.setDataPedido(datetime.now().strftime("%Y-%m-%d"))

            del self.quantidade_vendida[product.getId()]

            self.pedido.addValorTotal(-product.getPreco() * int(quantity_entry.get()))
            self.pedido.removeProduto(product)

            self.product_table.delete(item)

            messagebox.showinfo("Sucesso", "Produto removido com sucesso!")

            self.label_valor_total.config(text=f"Valor Total: R$ {self.pedido.getValorTotal():.2f}")

            new_order_window.destroy()

        def voltar():
            new_order_window.destroy()

        save_button = tk.Button(new_order_window, text="Salvar", bg="#4CAF50", fg="white", command=salvarAlteracoes)
        save_button.pack(pady=10)

        delete_button = tk.Button(new_order_window, text="Excluir", bg="#f44336", fg="white", command=excluirProduto)
        delete_button.pack(pady=10)

        voltar_button = tk.Button(new_order_window, text="Voltar", bg="#f44336", fg="white", command=voltar)
        voltar_button.pack(pady=10)


    def addProduct(self):

        # Criar uma nova janela
        new_order_window = tk.Toplevel(self)
        new_order_window.title("Adicionar Produto")
        new_order_window.geometry("500x600")
        new_order_window.transient(self) 

        # Campos de edição
        tk.Label(new_order_window, text="ID:").pack(pady=5)
        id_entry = tk.Entry(new_order_window)
        id_entry.pack(pady=5)

        tk.Label(new_order_window, text="Quantidade:").pack(pady=5)
        quantity_entry = tk.Entry(new_order_window)
        quantity_entry.pack(pady=5)

        # Botão para salvar alterações
        def salvarPedidoProduto():

            product = self.dbProduto.getProdutoPorID(int(id_entry.get()))
            
            if int(quantity_entry.get()) > product.getQuantidade():
                messagebox.showerror("Erro", "Quantidade insuficiente em estoque!")
                return

            if product.getId() not in self.quantidade_vendida:
                self.quantidade_vendida[product.getId()] = int(quantity_entry.get())
            else:
                self.quantidade_vendida[product.getId()] += int(quantity_entry.get())

            self.pedido.addProduto(product)
            self.pedido.setDataPedido(datetime.now().strftime("%Y-%m-%d"))
            self.pedido.addValorTotal(product.getPreco() * int(quantity_entry.get()))

            # Atualizar a quantidade e o valor total se o produto já estiver na tabela 
            for item in self.product_table.get_children():

                item_values = self.product_table.item(item, "values")
                if int(item_values[0]) == product.getId():

                    self.product_table.item(item, values=[product.getId(), product.getNome(), product.getPreco(), self.quantidade_vendida[product.getId()]])
                    messagebox.showinfo("Sucesso", "Quantidade do produto atualizada com sucesso!")

                    self.label_valor_total.config(text=f"Valor Total: R$ {self.pedido.getValorTotal():.2f}")

                    new_order_window.destroy()
                    return

            if self.pedido != None:
                messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
                self.product_table.insert("", tk.END, values=[product.getId(), product.getNome(), product.getPreco(), self.quantidade_vendida[product.getId()]])
            else:
                messagebox.showerror("Erro", "Falha ao adicionar produto ao pedido!")

            self.label_valor_total.config(text=f"Valor Total: R$ {self.pedido.getValorTotal():.2f}")
            
            new_order_window.destroy()
        

        save_button = tk.Button(new_order_window, text="Adicionar", bg="#4CAF50", fg="white", command=salvarPedidoProduto)
        save_button.pack(pady=10)

        #messagebox.showinfo("Adicionar Produto", "Insira o ID do produto e a quantidade desejada")
        
        # Botão para voltar
        voltar_button = tk.Button(new_order_window, text="Voltar", bg="#f44336", fg="white", command=new_order_window.destroy)
        voltar_button.pack(pady=10)


    def finalizarPedido(self):
        if self.pedido.getProdutos() == []:
            messagebox.showerror("Erro", "Pedido sem produtos!")
            return

        produtos = self.pedido.getProdutos()
        for produto in produtos:
            produto.setQuantidade(produto.getQuantidade() - self.quantidade_vendida[produto.getId()])
            produto.setVendidos(produto.getVendidos() + self.quantidade_vendida[produto.getId()])
            self.dbProduto.atualizarProduto(produto)
            produto.setQuantidade(self.quantidade_vendida[produto.getId()]) # Apenas para inserir certo na tabela itens_pedido

        self.pedido.setDataPedido(datetime.now().strftime("%Y-%m-%d"))
        self.pedido.setObservacoes(self.observations_entry.get())
        self.dbPedido.criarPedido(self.pedido)

        messagebox.showinfo("Sucesso", "Pedido finalizado com sucesso!")

        #self.controller.getScreen("ProductsScreen").exibirProdutos()
        
        self.controller.show("ProductsScreen")