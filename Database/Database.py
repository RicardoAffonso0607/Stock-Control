import psycopg2
import time
from datetime import date

class Database():

    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",        
            database="projeto_aps", 
            user="ricardo",     
            password="senha"  
        )
        self.cursor = self.conn.cursor()
        time.sleep(2)

    def finalizarServidor(self):
        """
        Metodo para finalizar a conexao com o banco de dados
        """
        self.cursor.close()
        self.conn.close()