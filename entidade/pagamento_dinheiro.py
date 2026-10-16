from datetime import date
from entidade.pagamento import Pagamento


class PagamentoDinheiro(Pagamento):
    def __init__(
        self,
        paciente,
        data_pagamento: date,
        valor_pago: float,
        atendimento=None,
    ):
        super().__init__(paciente, data_pagamento, valor_pago, atendimento=atendimento)

    def detalhe(self) -> str:
        return "Espécie"
