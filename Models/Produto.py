class Produto:

    def __init__(self, id = None, nome = None, preco = None, quantidade = None, data_entrada = None, vendidos = None, data_validade = None):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.data_entrada = data_entrada
        self.vendidos = vendidos
        self.data_validade = data_validade

    def __str__(self):
        return f"Produto: id = {self.id}, nome = {self.nome}, preco = {self.preco}"
    
    def getAll(self):
        return [self.id, self.nome, self.preco, self.quantidade, self.data_entrada, self.vendidos, self.data_validade]

    def getId(self):
        return self.id
    
    def setNome(self, nome):
        self.nome = nome

    def getNome(self):
        return self.nome
    
    def setPreco(self, preco):
        self.preco = preco

    def getPreco(self):
        return self.preco
    
    def setQuantidade(self, quantidade):
        self.quantidade = quantidade

    def getQuantidade(self):
        return self.quantidade
    
    def setDataEntrada(self, data_entrada):
        self.data_entrada = data_entrada

    def getDataEntrada(self):
        return self.data_entrada
    
    def setVendidos(self, vendidos):
        self.vendidos = vendidos

    def getVendidos(self):
        return self.vendidos
    
    def setDataValidade(self, data_validade):
        self.data_validade = data_validade

    def getDataValidade(self):
        return self.data_validade