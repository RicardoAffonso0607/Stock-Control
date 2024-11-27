from Database import *
from ScreenManager import *
import tkinter as tk

class Main():

    def __init__(self):
        self.db = Database()
        self.screenManager = ScreenManager(self.db)

    def testeDB(self) -> None:
        print(self.db.getProdutos())
        print("\n")
        print(self.db.getProdutoPorID(2))
        print("\n")
        print(self.db.getProdutoPorNome('pera'))
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
