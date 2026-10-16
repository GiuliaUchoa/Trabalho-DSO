from datetime import date, time
from typing import Optional
from decimal import Decimal

from excecoes.dado_invalido_exception import DadoInvalidoException
from excecoes.horario_fora_funcionamento_exception import HorarioForaFuncionamentoException
from excecoes.paciente_menor_idade_exception import PacienteMenorIdadeException
from excecoes.pagamento_invalido_exception import PagamentoInvalidoException


class Atendimento:
    def __init__(
        self,
        clinica,
        paciente,
        profissional,
        data: date,
        horario_inicio: time,
        horario_fim: time,
        tipo_atendimento,
        valor_total: float,
        menor_acompanhado: bool = False,
        id_atendimento: Optional[int] = None,
    ):
        self.__procedimentos = []
        self.__pagamentos = []
        self.__atendimento_realizado = False
        self.__id_atendimento = id_atendimento

        self.__valida_horarios(horario_inicio, horario_fim)
        self.__valida_clinica_horario(clinica, horario_inicio, horario_fim)
        self.__valida_paciente_idade(paciente, data, menor_acompanhado)

        self.__clinica = clinica
        self.__paciente = paciente
        self.__profissional = profissional
        self.data = data
        self.__horario_inicio = horario_inicio
        self.__horario_fim = horario_fim
        self.__tipo_atendimento = tipo_atendimento
        self.valor_total = valor_total
        self.__menor_acompanhado = menor_acompanhado

        # Vincula atendimento na clínica
        if hasattr(self.__clinica, "adicionar_atendimento"):
            self.__clinica.adicionar_atendimento(self)

    def __valida_horarios(self, inicio: time, fim: time) -> None:
        if not isinstance(inicio, time) or not isinstance(fim, time):
            raise DadoInvalidoException("horarios", "devem ser do tipo datetime.time")
        if inicio >= fim:
            raise DadoInvalidoException("horarios", "horário de início deve ser anterior ao horário de fim")

    def __valida_clinica_horario(self, clinica, inicio: time, fim: time) -> None:
        if clinica is None:
            raise DadoInvalidoException("clinica", "não pode ser nula")
        if hasattr(clinica, "horario_eh_valido"):
            if not clinica.horario_eh_valido(inicio, fim):
                raise HorarioForaFuncionamentoException(
                    f"Horário ({inicio.strftime('%H:%M')} às {fim.strftime('%H:%M')}) fora do período "
                    f"de funcionamento da clínica ({clinica.hora_abertura.strftime('%H:%M')} às {clinica.hora_fechamento.strftime('%H:%M')})."
                )

    def __valida_paciente_idade(self, paciente, data_atendimento: date, acompanhado: bool) -> None:
        if paciente is None:
            raise DadoInvalidoException("paciente", "não pode ser nulo")
        if hasattr(paciente, "calcular_idade"):
            idade = paciente.calcular_idade(data_atendimento)
            if idade < 18 and not acompanhado:
                raise PacienteMenorIdadeException(
                    f"Paciente tem {idade} anos. Pacientes menores de 18 anos precisam estar acompanhados por um responsável."
                )

    @property
    def id_atendimento(self) -> Optional[int]:
        return self.__id_atendimento

    @id_atendimento.setter
    def id_atendimento(self, id_atendimento: int) -> None:
        self.__id_atendimento = id_atendimento

    @property
    def clinica(self):
        return self.__clinica

    @clinica.setter
    def clinica(self, clinica) -> None:
        self.__valida_clinica_horario(clinica, self.__horario_inicio, self.__horario_fim)
        if self.__clinica != clinica:
            if hasattr(self.__clinica, "remover_atendimento"):
                self.__clinica.remover_atendimento(self)
            self.__clinica = clinica
            if hasattr(self.__clinica, "adicionar_atendimento"):
                self.__clinica.adicionar_atendimento(self)

    @property
    def paciente(self):
        return self.__paciente

    @paciente.setter
    def paciente(self, paciente) -> None:
        self.__valida_paciente_idade(paciente, self.__data, self.__menor_acompanhado)
        self.__paciente = paciente

    @property
    def profissional(self):
        return self.__profissional

    @profissional.setter
    def profissional(self, profissional) -> None:
        if profissional is None:
            raise DadoInvalidoException("profissional", "não pode ser nulo")
        self.__profissional = profissional

    @property
    def data(self) -> date:
        return self.__data

    @data.setter
    def data(self, data: date) -> None:
        if not isinstance(data, date):
            raise DadoInvalidoException("data", "deve ser do tipo datetime.date")
        self.__data = data

    @property
    def horario_inicio(self) -> time:
        return self.__horario_inicio

    @horario_inicio.setter
    def horario_inicio(self, horario_inicio: time) -> None:
        self.__valida_horarios(horario_inicio, self.__horario_fim)
        self.__valida_clinica_horario(self.__clinica, horario_inicio, self.__horario_fim)
        self.__horario_inicio = horario_inicio

    @property
    def horario_fim(self) -> time:
        return self.__horario_fim

    @horario_fim.setter
    def horario_fim(self, horario_fim: time) -> None:
        self.__valida_horarios(self.__horario_inicio, horario_fim)
        self.__valida_clinica_horario(self.__clinica, self.__horario_inicio, horario_fim)
        self.__horario_fim = horario_fim

    @property
    def tipo_atendimento(self):
        return self.__tipo_atendimento

    @tipo_atendimento.setter
    def tipo_atendimento(self, tipo_atendimento) -> None:
        if tipo_atendimento is None:
            raise DadoInvalidoException("tipo_atendimento", "não pode ser nulo")
        self.__tipo_atendimento = tipo_atendimento

    @property
    def valor_total(self) -> float:
        return self.__valor_total

    @valor_total.setter
    def valor_total(self, valor_total: float) -> None:
        if not isinstance(valor_total, (int, float, Decimal)):
            raise DadoInvalidoException("valor_total", "deve ser numérico")
        if valor_total < 0:
            raise DadoInvalidoException("valor_total", "não pode ser negativo")
        self.__valor_total = float(valor_total)

    @property
    def menor_acompanhado(self) -> bool:
        return self.__menor_acompanhado

    @menor_acompanhado.setter
    def menor_acompanhado(self, menor_acompanhado: bool) -> None:
        self.__menor_acompanhado = menor_acompanhado

    @property
    def atendimento_realizado(self) -> bool:
        return self.__atendimento_realizado

    @atendimento_realizado.setter
    def atendimento_realizado(self, atendimento_realizado: bool) -> None:
        self.__atendimento_realizado = bool(atendimento_realizado)

    @property
    def procedimentos(self) -> list:
        return self.__procedimentos

    @property
    def pagamentos(self) -> list:
        return self.__pagamentos

    def realizar_atendimento(self) -> None:
        self.__atendimento_realizado = True

    def adicionar_procedimento(self, procedimento) -> None:
        if procedimento is None:
            raise DadoInvalidoException("procedimento", "não pode ser nulo")
        self.__procedimentos.append(procedimento)

    def remover_procedimento(self, procedimento) -> None:
        if procedimento in self.__procedimentos:
            self.__procedimentos.remove(procedimento)

    def adicionar_pagamento(self, pagamento) -> None:
        if pagamento is None:
            raise DadoInvalidoException("pagamento", "não pode ser nulo")

        # Regra 3: Os pagamentos devem ser realizados até a data do atendimento.
        if pagamento.data_pagamento > self.__data:
            raise PagamentoInvalidoException(
                f"Data do pagamento ({pagamento.data_pagamento.strftime('%d/%m/%Y')}) é posterior "
                f"à data do atendimento ({self.__data.strftime('%d/%m/%Y')})."
            )

        valor_restante = self.calcular_valor_a_pagar()
        if round(pagamento.valor_pago, 2) > round(valor_restante, 2):
            raise PagamentoInvalidoException(
                f"Valor pago (R$ {pagamento.valor_pago:.2f}) excede o saldo restante a pagar (R$ {valor_restante:.2f})."
            )

        self.__pagamentos.append(pagamento)

    def calcular_custo_procedimentos(self) -> float:
        return sum(float(proc.custo) for proc in self.__procedimentos if hasattr(proc, "custo"))

    def calcular_valor_total_com_procedimentos(self) -> float:
        return self.__valor_total + self.calcular_custo_procedimentos()

    def calcular_valor_pago(self) -> float:
        return sum(float(pag.valor_pago) for pag in self.__pagamentos if hasattr(pag, "valor_pago"))

    def calcular_valor_a_pagar(self) -> float:
        saldo = self.calcular_valor_total_com_procedimentos() - self.calcular_valor_pago()
        return max(0.0, round(saldo, 2))

    def calcular_valor_restante(self) -> float:
        return self.calcular_valor_a_pagar()

    def esta_pago(self) -> bool:
        return self.calcular_valor_a_pagar() == 0.0
