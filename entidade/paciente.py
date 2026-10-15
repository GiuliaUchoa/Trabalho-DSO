from entidade.pessoa import Pessoa
from datetime import date

class Paciente(Pessoa):
    def __init__(self, nome: str, celular: str, cpf: str, data_nascimento: date):
        super().__init__(nome, celular, cpf)
        self.__data_nascimento = data_nascimento

    @property
    def data_nascimento(self):
        return self.__data_nascimento
    @data_nascimento.setter
    def data_nascimento(self, data_nascimento):
        if not isinstance(data_nascimento, date):
            raise TypeError("data_nascimento deve ser um objeto do tipo date.")
        self.__data_nascimento = data_nascimento

    def calcular_idade(self, data_referencia: date) -> int:
        if not isinstance(data_referencia, date):
            raise TypeError("data_referencia deve ser um objeto do tipo date.")
        idade = data_referencia.year - self.__data_nascimento.year
        if (data_referencia.month, data_referencia.day) < (self.__data_nascimento.month, self.__data_nascimento.day):
            idade -= 1
        return idade