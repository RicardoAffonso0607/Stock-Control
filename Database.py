import psycopg2
import time
from datetime import date

class Database():

    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",        
            database="stockcontrol", 
            user="ricardo",     
            password="ricardo"  
        )
        self.cursor = self.conn.cursor()
        time.sleep(2)

    def getProdutos(self) -> list[tuple] | str:
        """
        Busca todos os produtos 

        Retorna:
        - list[tuple]: Produtos
        - str: Mensagem de erro

        """
        try:
            self.cursor.execute("SELECT * FROM produtos")
            produtos = self.cursor.fetchall()
            if produtos == None:
                raise Exception("Nenhum produto encontrado")
            return produtos
        except Exception as e:
            return e

    def getProdutoPorID(self, id:int) -> tuple | str:
        """
        Busca produto por ID

        Parametro:
        - int: id a ser buscado

        Retorna:
        - tuple: Produto
        - str: Mensagem de erro
        """
        try:
            if id < 1:
                raise Exception("ID invalido")
            
            self.cursor.execute(f"SELECT * FROM produtos WHERE id = {id}")
            produto = self.cursor.fetchone()

            if produto == None:
                raise Exception("Produto nao encontrado")
            return produto
        except Exception as e:
            return e
        
    def getProdutoPorNome(self, nome:str) -> list[tuple] | tuple | str:
        """
        Busca todos os produtos que contenham esse nome 

        Parametro:
        - str: nome a ser buscado

        Retorna:
        - list[tuple]: Produtos (quando mais de um produto tem o mesmo nome)
        - tuple: Produto
        - str: Mensagem de erro
        """
        try:
            if nome == None:
                raise Exception("Nome invalido")
            
            self.cursor.execute(f"SELECT * FROM produtos WHERE nome = '{nome}'")
            produtos = self.cursor.fetchall()

            if produtos == None:
                raise Exception("Produto nao encontrado")
            return produtos
        except Exception as e:
            return e
        
    def atualizarProduto(self, valores_atualizados):
        try:
            if not valores_atualizados:
                raise Exception("Parametros inválidos")
            
            self.cursor.execute(f"UPDATE produtos SET preco = '{valores_atualizados[2]}', quantidade = '{valores_atualizados[3]}', data_entrada = '{valores_atualizados[4]}', vendidos = '{valores_atualizados[5]}', data_validade = '{valores_atualizados[6]}'" +
                                f"WHERE id = '{valores_atualizados[0]}'")
            self.conn.commit()
            return
        except Exception as e:
            return e
        
    def criarProduto(self, nome, preco, quantidade, vendidos, data_validade):
        try:
            if not nome or not preco or not quantidade or not vendidos or not data_validade:
                raise Exception("Parametros invalidos")
            produto = self.getProdutoPorNome(nome=nome)
            if produto != []:
                raise Exception("Produto ja existe")
            self.cursor.execute("INSERT INTO produtos (nome, preco, quantidade, data_entrada, vendidos, data_validade)" +
                                f"VALUES ('{nome}','{preco}', '{quantidade}', '{date.today()}', '{vendidos}', '{data_validade}') RETURNING id")
            id = self.cursor.fetchone()[0]
            self.conn.commit()
            return id
        except Exception as e:
            return e
        
    def excluirProduto(self, id:int):
        try:
            if id < 1:
                raise Exception("Parametros inválidos")
            produto = self.getProdutoPorID(id=id)
            if produto == None:
                return
            self.cursor.execute(f"DELETE FROM produtos WHERE id = {id}") 
            self.conn.commit()
            return
        except Exception as e:
            return e
        
    def getUsuarioPorLogin(self, login: str) -> tuple:
        """
        Busca usuario por login

        Parametro:
        - login (str): nome a ser buscado

        Retorna:
        - tuple: Usuario
        - str: Mensagem de erro
        """
        try:
            if login == None:
                raise Exception("Login invalido")
            
            self.cursor.execute(f"SELECT * FROM usuarios WHERE login = '{login}'")
            usuario = self.cursor.fetchone()

            if usuario == None:
                raise Exception("Usuario nao encontrado")
            return usuario
        except Exception as e:
            return e
        
    def createUsuario(self, nome, login, senha, nivel_acesso):
        try:
            if not nome or not login or not senha or not nivel_acesso:
                raise Exception("Parametros inválidos")
            
            self.cursor.execute("INSERT INTO usuarios (create_time, nome, login, senha, nivel_acesso)" +
                               f"VALUES ('{date.today()}','{nome}', '{login}', '{senha}', '{nivel_acesso}')")
            self.conn.commit()
            return
        except Exception as e:
            return e
        
    def existeUsuario(self, login: str) -> bool:
        """
        Verifica se usuario existe

        Parametro:
        - login (str): login a ser buscado

        Retorna:
        - bool: True se existe, False se nao existe
        - str: Mensagem de erro
        """
        try:
            if login == None:
                raise Exception("Parametros invalidos")
            
            self.cursor.execute(f"SELECT * FROM usuarios WHERE login = '{login}'")
            usuario = self.cursor.fetchone()

            if usuario == None:
                return False
            
            return True

        except Exception as e:
            return e
        
    def verificarNomeESenha(self, login: str, senha: str) -> bool:
        """
        Verifica se nome e senha estao corretos

        Parametro:
        - login (str): login a ser buscado
        - senha (str): senha a ser buscado

        Retorna:
        - bool: True se existe, False se nao existe
        - str: Mensagem de erro
        """
        try:
            if login == None or senha == None:
                raise Exception("Parametros invalidos")
            
            self.cursor.execute(f"SELECT * FROM usuarios WHERE login = '{login}' AND senha = '{senha}'")
            usuario = self.cursor.fetchone()

            if usuario == None:
                return False
            
            return True

        except Exception as e:
            return e

    def finalizarServidor(self):
        """
        Metodo para finalizar a conexao com o banco de dados
        """
        self.cursor.close()
        self.conn.close()