from entidade.pessoa import Pessoa
from datetime import date

class Paciente(Pessoa):
    def __init__(self, nome: str, celular: str, cpf: str, data_nascimento: date):
        super().__init__(nome, celular, cpf)
        if len(data_nascimento) != 10 or data_nascimento[2] != '/' or data_nascimento[5] != '/':
            raise ValueError('A formatação da data está errada.')
            # formato padrao de entrada: '00/00/0000'
        datas = data_nascimento.split('/')
        data_formatada = date(int(datas[2]), int(datas[1]), int(datas[0]))
        self.__data_nascimento = data_formatada

    @property
    def data_nascimento(self):
        return self.__data_nascimento
    @data_nascimento.setter
    def data_nascimento(self, data_nascimento):
        if len(data_nascimento) != 10 or data_nascimento[2] != '/' or data_nascimento[5] != '/':
            raise ValueError('A formatação da data está errada.')
        datas = data_nascimento.split('/')
        data_formatada = date(int(datas[2]), int(datas[1]), int(datas[0]))
        self.__data_nascimento = data_formatada

    def calcular_idade(self, data_referencia: date) -> int:
        if len(data_referencia) != 10 or data_referencia[2] != '/' or data_referencia[5] != '/':
            raise ValueError('A formatação da data está errada.')
        datas = data_referencia.split('/')
        data_formatada = date(int(datas[2]), int(datas[1]), int(datas[0]))
        idade = data_formatada.year - self.__data_nascimento.year
        if (data_formatada.month, data_formatada.day) < (self.__data_nascimento.month, self.__data_nascimento.day):
            idade -= 1
        return idade

    def __repr__(self):
        return f"Paciente(Nome: {self.nome}, Celular: {self.celular}, CPF: {self.cpf}, Data de nascimento: {self.data_nascimento})"
