import psycopg2
import time
from datetime import date
from Database.Database import Database
from Models.Usuario import Usuario

class DadosUsuario(Database):

    def __init__(self):
        super().__init__()

    def getUsuarioPorLogin(self, login: str) -> Usuario:
        """
        Busca usuario por login

        Parametro:
        - login (str): nome a ser buscado

        Retorna:
        - Usuario: Usuario
        - str: Mensagem de erro
        """
        try:
            if login == None:
                raise Exception("Login invalido")
            
            self.cursor.execute(f"SELECT * FROM usuarios WHERE login = '{login}'")
            usuario_encontrado = self.cursor.fetchone()

            if usuario_encontrado == None:
                raise Exception("Usuario nao encontrado")
            return Usuario(*usuario_encontrado)
        except Exception as e:
            return e
        
    def createUsuario(self, novo_usuario:Usuario):
        try:
            if not novo_usuario:
                raise Exception("Parametros inválidos")
            
            self.cursor.execute("INSERT INTO usuarios (create_time, nome, login, senha, nivel_acesso)" +
                               f"VALUES ('{date.today()}','{novo_usuario.getNome()}', '{novo_usuario.getLogin()}', '{novo_usuario.getSenha()}', '{novo_usuario.getNivelAcesso()}')")
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