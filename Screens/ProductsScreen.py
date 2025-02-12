from Screens.Screen import *
from Database.DadosProduto import *
from Database.DadosUsuario import *
from Config.Config import *
import csv
from datetime import datetime

class ProductsScreen(Screen):

    def __init__(self, parent, controller) -> None:
        super().__init__(parent, controller)
        self.dbProduto = DadosProduto()
        self.dbUsuario = DadosUsuario()
        self.config = Config()

        # Tema (consistente com a tela inicial)
        self.style = ttk.Style(theme="cosmo")

        # Fundo
        self.configure(bg=self.style.colors.get("light"))

        # Frame para centralizar o conteúdo
        content_frame = ttk.Frame(self)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Rótulo do título
        label_titulo = ttk.Label(
            content_frame,
            text="Stock Control",
            font=("Helvetica", 24, "bold"),
            bootstyle="dark"
        )
        label_titulo.pack(pady=20)

        # Treeview com os produtos
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.product_table = ttk.Treeview(
            content_frame,
            columns=("ID", "Nome", "Preço", "Quantidade", "Data de entrada", "Vendidos", "Data de validade"),
            show="headings",
            height=15,
            yscrollcommand=scrollbar.set,
            bootstyle="light"
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

        # Frame para os botões
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=20)

        # Botão para cadastrar novos usuários
        botao_cadastrar_usuario = ttk.Button(
            button_frame,
            text="Cadastrar novo usuário",
            bootstyle="primary",
            width=30,
            command=self.registrarUsuario
        )
        botao_cadastrar_usuario.pack(side="left", padx=5)

        # Botão para cadastrar novos produtos
        botao_cadastrar_produto = ttk.Button(
            button_frame,
            text="Cadastrar novo produto",
            bootstyle="primary",
            width=30,
            command=self.criarProduto
        )
        botao_cadastrar_produto.pack(side="left", padx=5)

        # Botão para criar um novo pedido
        botao_criar_pedido = ttk.Button(
            button_frame,
            text="Criar novo pedido",
            bootstyle="primary",
            width=30,
            command=self.criarPedido
        )
        botao_criar_pedido.pack(side="left", padx=5)

        # Botão para exportar para CSV
        botao_exportar_csv = ttk.Button(
            button_frame,
            text="Exportar para CSV",
            bootstyle="primary",
            width=30,
            command=self.exportarParaCSV
        )
        botao_exportar_csv.pack(side="left", padx=5)

        # Botão para voltar
        botao_voltar = ttk.Button(
            button_frame,
            text="Voltar para tela inicial",
            bootstyle="secondary",
            width=30,
            command=lambda: controller.show("HomeScreen")
        )
        botao_voltar.pack(side="left", padx=5)

    def exibirProdutos(self):
        produtos = self.dbProduto.getProdutos()
        produtos.sort(key=lambda x: x.getId())  # Organiza por ID
        for produto in produtos:
            self.product_table.insert("", tk.END, values=produto.getAll())
            if produto.getQuantidade() <= 0:
                messagebox.showwarning("Sem estoque", f"O produto {produto.getNome()} está sem estoque")

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
        new_product_window = ttk.Toplevel(self)
        new_product_window.title("Criar Produto")
        new_product_window.geometry("500x600")
        new_product_window.transient(self)

        # Campos de edição
        ttk.Label(new_product_window, text="Nome:").pack(pady=5)
        name_entry = ttk.Entry(new_product_window)
        name_entry.pack(pady=5)

        ttk.Label(new_product_window, text="Preço:").pack(pady=5)
        price_entry = ttk.Entry(new_product_window)
        price_entry.pack(pady=5)

        ttk.Label(new_product_window, text="Quantidade:").pack(pady=5)
        quantity_entry = ttk.Entry(new_product_window)
        quantity_entry.pack(pady=5)

        ttk.Label(new_product_window, text="Vendidos:").pack(pady=5)
        solds_entry = ttk.Entry(new_product_window)
        solds_entry.pack(pady=5)

        ttk.Label(new_product_window, text="Data de validade: formato (aaaa-mm-dd)").pack(pady=5)
        validity_date_entry = ttk.Entry(new_product_window)
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
            if not novo_produto.getNome():
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
            if new_product:
                messagebox.showinfo("Sucesso", "Produto criado com sucesso!")
                self.product_table.insert("", tk.END, values=new_product.getAll())
            else:
                messagebox.showerror("Erro", "Falha ao criar produto")
            new_product_window.destroy()

        def voltar():
            new_product_window.destroy()

        save_button = ttk.Button(new_product_window, text="Criar", bootstyle="success", command=salvarAlteracoes)
        save_button.pack(pady=10)

        voltar_button = ttk.Button(new_product_window, text="Voltar", bootstyle="secondary", command=voltar)
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
        edit_window = ttk.Toplevel(self)
        edit_window.title("Editar Produto")
        edit_window.geometry("500x600")
        edit_window.transient(self)

        # Nome do produto
        label_titulo = ttk.Label(
            edit_window,
            text=f"{produto_selecionado.getNome()}",
            font=("Helvetica", 18, "bold"),
            bootstyle="dark"
        )
        label_titulo.pack(pady=20)

        # Campos de edição
        ttk.Label(edit_window, text="Preço:").pack(pady=5)
        price_entry = ttk.Entry(edit_window)
        price_entry.insert(0, produto_selecionado.getPreco())
        price_entry.pack(pady=5)

        ttk.Label(edit_window, text="Quantidade:").pack(pady=5)
        quantity_entry = ttk.Entry(edit_window)
        quantity_entry.insert(0, produto_selecionado.getQuantidade())
        quantity_entry.pack(pady=5)

        ttk.Label(edit_window, text="Data de Entrada:").pack(pady=5)
        entry_date_entry = ttk.Entry(edit_window)
        entry_date_entry.insert(0, produto_selecionado.getDataEntrada())
        entry_date_entry.pack(pady=5)

        ttk.Label(edit_window, text="Vendidos:").pack(pady=5)
        solds_entry = ttk.Entry(edit_window)
        solds_entry.insert(0, produto_selecionado.getVendidos())
        solds_entry.pack(pady=5)

        ttk.Label(edit_window, text="Data de validade:").pack(pady=5)
        validity_date_entry = ttk.Entry(edit_window)
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
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
            edit_window.destroy()

        save_button = ttk.Button(edit_window, text="Salvar", bootstyle="success", command=salvarAlteracoes)
        save_button.pack(pady=10)

        voltar_button = ttk.Button(edit_window, text="Voltar", bootstyle="danger", command=edit_window.destroy)
        voltar_button.pack(pady=10)

        excluir_button = ttk.Button(edit_window, text="Excluir", bootstyle="danger", command=excluirProduto)
        excluir_button.pack(pady=10)