from Models.Produto import *

class Pedido:

    def __init__(self, id = None, data_pedido = None, valor_total = None):
        self.id = id
        self.data_pedido = data_pedido
        self.valor_total = valor_total
        self.observacoes = None
        self.produtos = list()

    def getId(self):
        return self.id
    
    def setDataPedido(self, data_pedido):
        self.data_pedido = data_pedido

    def getDataPedido(self):
        return self.data_pedido
    
    def setValorTotal(self, valor_total):
        self.valor_total = valor_total

    def getValorTotal(self):
        return self.valor_total
    
    def setObservacoes(self, observacoes):
        self.observacoes = observacoes

    def getObservacoes(self):
        return self.observacoes
    
    def addProduto(self, produto:Produto):
        if produto != None:
            self.produtos.append(produto)

    def addListaProdutos(self, produtos:list):
        self.produtos = produtos

    def getProdutos(self):
        return self.produtos
    

