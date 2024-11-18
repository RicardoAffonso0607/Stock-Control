import psycopg2
import time

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

    def testar(self):
        self.cursor.execute("SELECT * FROM produtos")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

    def finalizarServidor(self):
        self.cursor.close()
        self.conn.close()