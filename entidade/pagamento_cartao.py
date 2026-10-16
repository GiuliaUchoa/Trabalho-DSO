from datetime import date
from entidade.pagamento import Pagamento
from excecoes.dado_invalido_exception import DadoInvalidoException


class PagamentoCartao(Pagamento):
    def __init__(
        self,
        paciente,
        data_pagamento: date,
        valor_pago: float,
        numero_cartao: str,
        bandeira: str,
        atendimento=None,
    ):
        super().__init__(paciente, data_pagamento, valor_pago, atendimento=atendimento)
        if not isinstance(numero_cartao, str) or not numero_cartao.strip():
            raise DadoInvalidoException("numero_cartao", "deve ser um texto não vazio")
        self.__numero_cartao = numero_cartao.strip()

        if not isinstance(bandeira, str) or not bandeira.strip():
            raise DadoInvalidoException("bandeira", "deve ser um texto não vazio")
        self.__bandeira = bandeira.strip()

    @property
    def numero_cartao(self) -> str:
        return self.__numero_cartao

    @numero_cartao.setter
    def numero_cartao(self, numero_cartao: str) -> None:
        if not isinstance(numero_cartao, str) or not numero_cartao.strip():
            raise DadoInvalidoException("numero_cartao", "deve ser um texto não vazio")
        self.__numero_cartao = numero_cartao.strip()

    @property
    def bandeira(self) -> str:
        return self.__bandeira

    @bandeira.setter
    def bandeira(self, bandeira: str) -> None:
        if not isinstance(bandeira, str) or not bandeira.strip():
            raise DadoInvalidoException("bandeira", "deve ser um texto não vazio")
        self.__bandeira = bandeira.strip()

    def detalhe(self) -> str:
        ultimos = self.__numero_cartao[-4:] if len(self.__numero_cartao) >= 4 else self.__numero_cartao
        return f"Cartão final {ultimos} ({self.__bandeira})"
