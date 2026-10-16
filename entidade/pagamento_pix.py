from datetime import date
from entidade.pagamento import Pagamento
from excecoes.dado_invalido_exception import DadoInvalidoException


class PagamentoPix(Pagamento):
    def __init__(
        self,
        paciente,
        data_pagamento: date,
        valor_pago: float,
        cpf_pagador: str,
        atendimento=None,
    ):
        super().__init__(paciente, data_pagamento, valor_pago, atendimento=atendimento)
        if not isinstance(cpf_pagador, str) or not cpf_pagador.strip():
            raise DadoInvalidoException("cpf_pagador", "deve ser um texto não vazio")
        self.__cpf_pagador = cpf_pagador.strip()

    @property
    def cpf_pagador(self) -> str:
        return self.__cpf_pagador

    @cpf_pagador.setter
    def cpf_pagador(self, cpf_pagador: str) -> None:
        if not isinstance(cpf_pagador, str) or not cpf_pagador.strip():
            raise DadoInvalidoException("cpf_pagador", "deve ser um texto não vazio")
        self.__cpf_pagador = cpf_pagador.strip()

    def detalhe(self) -> str:
        return f"CPF Pagador: {self.__cpf_pagador}"
