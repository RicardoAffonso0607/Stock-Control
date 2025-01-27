from Database.Database import *
from Database.DadosProduto import * 
from Screens.ScreenManager import *
import tkinter as tk

class Main():

    def __init__(self):
        self.db = Database()
        self.screenManager = ScreenManager()
        self.dbProdutos = DadosProduto()

    def testeDB(self) -> None:
        produtos = self.dbProdutos.getProdutos()
        for produto in produtos:
            print(produto)
        print("\n")
        produto = self.dbProdutos.getProdutoPorID(2)
        print(produto)
        print("\n")
        produtos = self.dbProdutos.getProdutoPorNome('pera')
        for produto in produtos:
            print(produto)
        print("\n")
        #print(self.db.createUsuario("teste", "teste", "teste", 3))
        #print(self.db.verificarNomeESenha("ricardo", "ricar"))

    def main(self) -> None:
        self.screenManager.mainloop()

    def finalizar(self):
        self.db.finalizarServidor()

if __name__ == "__main__":
    main = Main()
    main.main()
    #main.testeDB()
    main.finalizar()
