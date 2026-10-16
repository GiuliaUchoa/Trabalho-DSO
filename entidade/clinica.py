from datetime import time
from typing import TYPE_CHECKING, Optional
from excecoes.dado_invalido_exception import DadoInvalidoException
from excecoes.horario_invalido_exception import HorarioInvalidoException

if TYPE_CHECKING:
    from entidade.profissional_saude import ProfissionalSaude


class Clinica:
    def __init__(
        self,
        nome: str,
        cidade: str,
        descricao: str,
        hora_abertura: time = time(8, 0),
        hora_fechamento: time = time(18, 0),
    ):
        self.__profissionais = []
        self.__atendimentos = []

        if not isinstance(nome, str) or not nome.strip():
            raise DadoInvalidoException("nome", "deve ser um texto não vazio")
        self.__nome = nome.strip()

        if not isinstance(cidade, str) or not cidade.strip():
            raise DadoInvalidoException("cidade", "deve ser um texto não vazio")
        self.__cidade = cidade.strip()

        if not isinstance(descricao, str):
            raise DadoInvalidoException("descricao", "deve ser um texto")
        self.__descricao = descricao.strip()
        self.__valida_horarios(hora_abertura, hora_fechamento)
        self.__hora_abertura = hora_abertura
        self.__hora_fechamento = hora_fechamento

    def __valida_horarios(self, abertura: time, fechamento: time) -> None:
        if not isinstance(abertura, time) or not isinstance(fechamento, time):
            raise HorarioInvalidoException("Os horários de abertura e fechamento devem ser do tipo datetime.time.")
        if abertura >= fechamento:
            raise HorarioInvalidoException("A hora de abertura deve ser estritamente anterior à hora de fechamento.")

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str) -> None:
        if not isinstance(nome, str) or not nome.strip():
            raise DadoInvalidoException("nome", "deve ser um texto não vazio")
        self.__nome = nome.strip()

    @property
    def cidade(self) -> str:
        return self.__cidade

    @cidade.setter
    def cidade(self, cidade: str) -> None:
        if not isinstance(cidade, str) or not cidade.strip():
            raise DadoInvalidoException("cidade", "deve ser um texto não vazio")
        self.__cidade = cidade.strip()

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str) -> None:
        if not isinstance(descricao, str):
            raise DadoInvalidoException("descricao", "deve ser um texto")
        self.__descricao = descricao.strip()

    @property
    def hora_abertura(self) -> time:
        return self.__hora_abertura

    @hora_abertura.setter
    def hora_abertura(self, hora_abertura: time) -> None:
        self.__valida_horarios(hora_abertura, self.__hora_fechamento)
        self.__hora_abertura = hora_abertura

    @property
    def hora_fechamento(self) -> time:
        return self.__hora_fechamento

    @hora_fechamento.setter
    def hora_fechamento(self, hora_fechamento: time) -> None:
        self.__valida_horarios(self.__hora_abertura, hora_fechamento)
        self.__hora_fechamento = hora_fechamento

    @property
    def profissionais(self) -> list:
        return self.__profissionais

    @property
    def atendimentos(self) -> list:
        return self.__atendimentos

    def adicionar_profissional(self, profissional: "ProfissionalSaude") -> None:
        from entidade.profissional_saude import ProfissionalSaude

        if not isinstance(profissional, ProfissionalSaude):
            raise DadoInvalidoException("profissional", "deve ser uma instância de ProfissionalSaude")

        if profissional not in self.__profissionais:
            self.__profissionais.append(profissional)

    def remover_profissional(self, profissional: "ProfissionalSaude") -> None:
        if profissional in self.__profissionais:
            self.__profissionais.remove(profissional)

    def adicionar_atendimento(self, atendimento) -> None:
        if atendimento not in self.__atendimentos:
            self.__atendimentos.append(atendimento)

    def remover_atendimento(self, atendimento) -> None:
        if atendimento in self.__atendimentos:
            self.__atendimentos.remove(atendimento)

    def horario_eh_valido(self, inicio_planejado: time, fim_planejado: time) -> bool:
        if not isinstance(inicio_planejado, time) or not isinstance(fim_planejado, time):
            return False
        return (
            self.__hora_abertura <= inicio_planejado
            and fim_planejado <= self.__hora_fechamento
            and inicio_planejado < fim_planejado
        )
