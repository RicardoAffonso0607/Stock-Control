class Usuario:

    def __init__(self, id = None, create_time = None, nome = None, login = None, senha = None, nivel_acesso = None):
        self.id = id
        self.create_time = create_time
        self.nome = nome
        self.login = login
        self.senha = senha
        self.nivel_acesso = nivel_acesso

    def __str__(self):
        return f"Usuario: id = {self.id}, login = {self.nome}, nivel_acesso = {self.nivel_acesso}"

    def getId(self):
        return self.id
    
    def setCreateTime(self, create_time):
        self.create_time = create_time

    def getCreateTime(self):
        return self.create_time

    def getNome(self):
        return self.nome
    
    def setNome(self, nome):
        self.nome = nome

    def getLogin(self):
        return self.login
    
    def setLogin(self, login):
        self.login = login

    def getSenha(self):
        return self.senha
    
    def setSenha(self, senha):
        self.senha = senha

    def getNivelAcesso(self):
        return self.nivel_acesso
    
    def setNivelAcesso(self, nivel_acesso):
        self.nivel_acesso = nivel_acesso

