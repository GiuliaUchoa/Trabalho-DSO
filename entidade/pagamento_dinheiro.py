from datetime import date
from entidade.pagamento import Pagamento


class PagamentoDinheiro(Pagamento):
    def __init__(
        self,
        paciente,
        data_pagamento: date,
        valor_pago: float,
    ):
        super().__init__(paciente, data_pagamento, valor_pago)
