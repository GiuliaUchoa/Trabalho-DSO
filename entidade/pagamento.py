from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, Optional
from excecoes.dado_invalido_exception import DadoInvalidoException

if TYPE_CHECKING:
    from entidade.paciente import Paciente


class Pagamento(ABC):
    def __init__(self, paciente, data_pagamento: date, valor_pago: float, atendimento=None):
        if paciente is None:
            raise DadoInvalidoException("paciente", "não pode ser nulo")
        try:
            from entidade.paciente import Paciente
            if not isinstance(paciente, Paciente):
                raise DadoInvalidoException("paciente", "deve ser uma instância válida de Paciente")
        except ImportError:
            pass
        self.__paciente = paciente

        if not isinstance(data_pagamento, date):
            raise DadoInvalidoException("data_pagamento", "deve ser uma data válida (date)")
        self.__data_pagamento = data_pagamento

        if not isinstance(valor_pago, (int, float, Decimal)):
            raise DadoInvalidoException("valor_pago", "deve ser um valor numérico")
        if valor_pago <= 0:
            raise DadoInvalidoException("valor_pago", "deve ser maior que zero")
        self.__valor_pago = float(valor_pago)
        self.__atendimento = atendimento

    @property
    def paciente(self):
        return self.__paciente

    @paciente.setter
    def paciente(self, paciente):
        if paciente is None:
            raise DadoInvalidoException("paciente", "não pode ser nulo")
        try:
            from entidade.paciente import Paciente
            if not isinstance(paciente, Paciente):
                raise DadoInvalidoException("paciente", "deve ser uma instância válida de Paciente")
        except ImportError:
            pass
        self.__paciente = paciente

    @property
    def data_pagamento(self) -> date:
        return self.__data_pagamento

    @data_pagamento.setter
    def data_pagamento(self, data_pagamento: date) -> None:
        if not isinstance(data_pagamento, date):
            raise DadoInvalidoException("data_pagamento", "deve ser uma data válida (date)")
        self.__data_pagamento = data_pagamento

    @property
    def valor_pago(self) -> float:
        return self.__valor_pago

    @valor_pago.setter
    def valor_pago(self, valor_pago: float) -> None:
        if not isinstance(valor_pago, (int, float, Decimal)):
            raise DadoInvalidoException("valor_pago", "deve ser um valor numérico")
        if valor_pago <= 0:
            raise DadoInvalidoException("valor_pago", "deve ser maior que zero")
        self.__valor_pago = float(valor_pago)

    @property
    def atendimento(self):
        return self.__atendimento

    @atendimento.setter
    def atendimento(self, atendimento) -> None:
        self.__atendimento = atendimento

    @abstractmethod
    def detalhe(self) -> str:
        pass
