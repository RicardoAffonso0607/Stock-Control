from Models.Usuario import *

class Config:

    _estado = None  # Instância única

    def __new__(cls, *args, **kwargs):
        """
        Implementação do padrão Singleton
        """
        if cls._estado is None:
            cls._estado = super().__new__(cls, *args, **kwargs)
            cls._estado.usuario_atual = Usuario()
        return cls._estado

    def getUsuarioAtual(self) -> Usuario:
        return self.usuario_atual
    
    def setUsuarioAtual(self, usuario:Usuario):
        self.usuario_atual = usuario