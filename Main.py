from Database import *

def main() -> None:
    db = Database()
    print(db.getProdutos())
    print("\n")
    print(db.getProdutoPorID(2))
    print("\n")
    print(db.getProdutoPorNome('pera'))
    print("\n")
    db.finalizarServidor()


if __name__ == "__main__":
    main()