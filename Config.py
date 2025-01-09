class Config:

    _estado = None  # Instância única

    def __new__(cls, *args, **kwargs):
        """
        Implementação do padrão Singleton
        """
        if cls._estado is None:
            cls._estado = super().__new__(cls, *args, **kwargs)
            cls._estado.usuario_atual = None
        return cls._estado

    def getUsuarioAtual(self):
        return self.usuario_atual
    
    def setUsuarioAtual(self, usuario):
        self.usuario_atual = usuario