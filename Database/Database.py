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

    def finalizarServidor(self):
        """
        Metodo para finalizar a conexao com o banco de dados
        """
        self.cursor.close()
        self.conn.close()