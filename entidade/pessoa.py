class Pessoa:
    def __init__(self, nome, celular, cpf):
        self.__nome = nome
        self.__celular = celular
        self.__cpf = cpf
    
    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def celular(self):
        return self.__celular
    @celular.setter
    def celular(self, celular):
        self.__celular = celular

    @property
    def cpf(self):
        return self.__cpf
    @cpf.setter
    def cpf(self, cpf):
        self.__cpf = cpf