import psycopg2
import time
from tkinter import messagebox
from datetime import date
from Database.Database import Database
from Models.Pedido import Pedido
from Models.Produto import Produto

class DadosPedido(Database):

    def __init__(self):
        super().__init__()

    def getPedidoPorId(self, id:int):
        try:
            if id == None:
                raise Exception("Falha ao procurar pedido por id - Favor informar um id")
            
            self.cursor.execute(f"SELECT * FROM pedidos WHERE id = '{id}'")
            pedido_encontrado = self.cursor.fetchone()

            if pedido_encontrado == None:
                raise Exception("Pedido nao encontrado - Falha ao procurar pedido no banco de dados")
            
            self.cursor.execute(f"SELECT * FROM itens_pedido WHERE pedido_id = '{id}'")
            produtos_relacionados = self.cursor.fetchall()

            lista_produtos = list()
            for produto_relacionados in produtos_relacionados:
                lista_produtos.append(Produto(*produto_relacionados))
            
            pedido = Pedido(*pedido_encontrado)
            pedido.addListaProdutos(lista_produtos)

            return pedido
            
        except Exception as e:
            messagebox.showerror("Erro", e)
            return e
        
    def atualizarPedido(self, pedido_atualizado:Pedido):
        try:
            if not pedido_atualizado:
                raise Exception("Parametro inválido - Falha ao atualizar pedido")
            
            self.cursor.execute(f"UPDATE pedidos SET data_pedido = '{pedido_atualizado.getDataPedido()}', valor_total = '{pedido_atualizado.getValorTotal()}', observacoes = '{pedido_atualizado.getObservacoes()}'" +
                                f"WHERE id = '{pedido_atualizado.getId()}'")
            self.conn.commit()

            return
        
        except Exception as e:
            messagebox.showerror("Erro", e)
            return e

    def criarPedido(self, novo_pedido:Pedido):
        try:
            if not novo_pedido:
                raise Exception("Parametro invalido - Falha ao criar pedido")
            
            if not novo_pedido.getProdutos():
                raise Exception("Pedido sem produtos - Favor adicionar produtos ao pedido")
            
            self.cursor.execute("INSERT INTO pedidos (data_pedido, valor_total, observacoes)" +
                               f"VALUES ('{novo_pedido.getDataPedido()}','{novo_pedido.getValorTotal()}', '{novo_pedido.getObservacoes()}') RETURNING id")
            id = self.cursor.fetchone()[0]
            self.conn.commit()

            for produto in novo_pedido.getProdutos():
                self.cursor.execute("INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario, subtotal)" +
                                   f"VALUES ('{id}', '{produto.getId()}', '{produto.getQuantidade()}', '{produto.getPreco()}','{produto.getQuantidade() * produto.getPreco()}')")
                self.conn.commit()

            return id
        
        except Exception as e:
            messagebox.showerror("Erro", e)
            return e