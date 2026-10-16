from datetime import date
from typing import Union
from entidade.pessoa import Pessoa
from excecoes.dado_invalido_exception import DadoInvalidoException


class Paciente(Pessoa):
    def __init__(self, nome: str, celular: str, cpf: str, data_nascimento: Union[str, date]):
        super().__init__(nome, celular, cpf)
        data_convertida = self.__converter_data(data_nascimento)
        if data_convertida > date.today():
            raise DadoInvalidoException("data_nascimento", "não pode ser uma data futura")
        self.__data_nascimento = data_convertida

    def __converter_data(self, valor: Union[str, date]) -> date:
        if isinstance(valor, date):
            return valor
        if isinstance(valor, str):
            texto = valor.strip()
            try:
                partes = texto.split("/")
                if len(partes) != 3 or len(partes[0]) != 2 or len(partes[1]) != 2 or len(partes[2]) != 4:
                    raise ValueError
                dia, mes, ano = int(partes[0]), int(partes[1]), int(partes[2])
                return date(ano, mes, dia)
            except (ValueError, TypeError):
                raise DadoInvalidoException("data_nascimento", "deve estar no formato DD/MM/AAAA (ex: 15/06/2006)")
        raise DadoInvalidoException("data_nascimento", "deve ser um texto no formato DD/MM/AAAA ou datetime.date")

    @property
    def data_nascimento(self) -> date:
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento: Union[str, date]) -> None:
        data_convertida = self.__converter_data(data_nascimento)
        if data_convertida > date.today():
            raise DadoInvalidoException("data_nascimento", "não pode ser uma data futura")
        self.__data_nascimento = data_convertida

    def calcular_idade(self, data_referencia: Union[str, date] = None) -> int:
        if data_referencia is None:
            data_referencia = date.today()
        elif isinstance(data_referencia, str):
            data_referencia = self.__converter_data(data_referencia)
        elif not isinstance(data_referencia, date):
            raise DadoInvalidoException("data_referencia", "deve ser do tipo date ou texto no formato DD/MM/AAAA")

        idade = data_referencia.year - self.__data_nascimento.year
        if (data_referencia.month, data_referencia.day) < (self.__data_nascimento.month, self.__data_nascimento.day):
            idade -= 1
        return idade

    def __repr__(self) -> str:
        data_formatada = self.__data_nascimento.strftime("%d/%m/%Y")
        return f"Paciente(Nome: {self.nome}, Celular: {self.celular}, CPF: {self.cpf}, Data de nascimento: {data_formatada})"
