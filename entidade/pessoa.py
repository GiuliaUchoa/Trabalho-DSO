from abc import ABC, abstractmethod
from excecoes.dado_invalido_exception import DadoInvalidoException


class Pessoa(ABC):
    def __init__(self, nome: str, celular: str, cpf: str):
        if not isinstance(nome, str) or not nome.strip():
            raise DadoInvalidoException("nome", "deve ser um texto não vazio")
        self.__nome = nome.strip()

        if not isinstance(celular, str) or not celular.strip():
            raise DadoInvalidoException("celular", "deve ser um texto não vazio")
        self.__celular = celular.strip()

        if not isinstance(cpf, str) or not cpf.strip():
            raise DadoInvalidoException("cpf", "deve ser um texto não vazio")
        self.__cpf = cpf.strip()

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str) -> None:
        if not isinstance(nome, str) or not nome.strip():
            raise DadoInvalidoException("nome", "deve ser um texto não vazio")
        self.__nome = nome.strip()

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, celular: str) -> None:
        if not isinstance(celular, str) or not celular.strip():
            raise DadoInvalidoException("celular", "deve ser um texto não vazio")
        self.__celular = celular.strip()

    @property
    def cpf(self) -> str:
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf: str) -> None:
        if not isinstance(cpf, str) or not cpf.strip():
            raise DadoInvalidoException("cpf", "deve ser um texto não vazio")
        self.__cpf = cpf.strip()

    @abstractmethod
    def __repr__(self) -> str:
        pass