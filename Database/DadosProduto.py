import psycopg2
import time
from tkinter import messagebox
from datetime import date
from Database.Database import Database
from Models.Produto import Produto

class DadosProduto(Database):

    def __init__(self):
        super().__init__()

    def getProdutos(self) -> list[Produto] | str:
        """
        Busca todos os produtos 

        Retorna:
        - list[Produto]: Produtos
        - str: Mensagem de erro

        """
        try:
            self.cursor.execute("SELECT * FROM produtos")
            produtos_encontrados = self.cursor.fetchall()

            if produtos_encontrados == None:
                raise Exception("Nenhum produto encontrado")
            lista_produtos = list()

            for produto_encontrado in produtos_encontrados:
                lista_produtos.append(Produto(*produto_encontrado))

            return lista_produtos
        
        except Exception as e:
            messagebox.showerror("Erro", e)
            return e

    def getProdutoPorID(self, id:int) -> Produto | str:
        """
        Busca produto por ID

        Parametro:
        - int: id a ser buscado

        Retorna:
        - Produto: Produto
        - str: Mensagem de erro
        """
        try:
            if id < 1:
                raise Exception("ID invalido - ID deve ser maior que 0")
            
            self.cursor.execute(f"SELECT * FROM produtos WHERE id = {id}")
            produto_encontrado = self.cursor.fetchone()

            if produto_encontrado == None:
                raise Exception("Produto nao encontrado - ID de produto invalido")
            
            return Produto(*produto_encontrado)
        
        except Exception as e:
            messagebox.showerror("Erro", e)
            return e
        
    def getProdutoPorNome(self, nome:str) -> list[Produto] | Produto | str:
        """
        Busca todos os produtos que contenham esse nome 

        Parametro:
        - str: nome a ser buscado

        Retorna:
        - list[Produto]: Produtos (quando mais de um produto tem o mesmo nome)
        - Produto: Produto
        - str: Mensagem de erro
        """
        try:
            if nome == None:
                raise Exception("Nome de produto invalido")
            
            self.cursor.execute(f"SELECT * FROM produtos WHERE nome = '{nome}'")
            produtos_encontrados = self.cursor.fetchall()

            if produtos_encontrados == None:
                raise Exception("Produto nao encontrado - Nome de produto invalido")
            
            lista_produtos = list()
            for produto_encontrado in produtos_encontrados:
                lista_produtos.append(Produto(*produto_encontrado))
            return lista_produtos
            
        except Exception as e:
            messagebox.showerror("Erro", e)
            return e
        
    def atualizarProduto(self, produto_atualizado:Produto):
        try:
            if not produto_atualizado:
                raise Exception("Parametro inválido - Falha ao atualizar produto")
            
            self.cursor.execute(f"UPDATE produtos SET preco = '{produto_atualizado.getPreco()}', quantidade = '{produto_atualizado.getQuantidade()}', data_entrada = '{produto_atualizado.getDataEntrada()}', vendidos = '{produto_atualizado.getVendidos()}', data_validade = '{produto_atualizado.getDataValidade()}'" +
                                f"WHERE id = '{produto_atualizado.getId()}'")
            self.conn.commit()

            return
        
        except Exception as e:
            messagebox.showerror("Erro", e)
            return e
        
    def criarProduto(self, novo_produto:Produto):
        try:
            if not novo_produto:
                raise Exception("Parametro invalido - Falha ao criar produto")
            produto_existente = self.getProdutoPorNome(nome=novo_produto.getNome())

            if produto_existente != []:
                raise Exception("Produto ja existe")
            
            self.cursor.execute("INSERT INTO produtos (nome, preco, quantidade, data_entrada, vendidos, data_validade)" +
                                f"VALUES ('{novo_produto.getNome()}','{novo_produto.getPreco()}', '{novo_produto.getQuantidade()}', '{date.today()}', '{novo_produto.getVendidos()}', '{novo_produto.getDataValidade()}') RETURNING id")
            id = self.cursor.fetchone()[0]
            self.conn.commit()

            return id
        
        except Exception as e:
            messagebox.showerror("Erro", e)
            return e
        
    def excluirProduto(self, id:int):
        try:
            if id < 1:
                raise Exception("Parametros inválidos - ID precisa ser maior que 0")
            
            produto = self.getProdutoPorID(id=id)

            if produto == None:
                return
            
            self.cursor.execute(f"DELETE FROM produtos WHERE id = {id}") 
            self.conn.commit()

            return
        
        except Exception as e:
            messagebox.showerror("Erro", e)
            return e
