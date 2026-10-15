from abc import ABC
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING
from excecoes.dado_invalido_exception import DadoInvalidoException

if TYPE_CHECKING:
    from entidade.paciente import Paciente


class Pagamento(ABC):
    def __init__(self, paciente, data_pagamento: date, valor_pago: float):
        self.paciente = paciente
        self.data_pagamento = data_pagamento
        self.valor_pago = valor_pago

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
            # Caso a classe Paciente ainda não esteja disponível no módulo
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
