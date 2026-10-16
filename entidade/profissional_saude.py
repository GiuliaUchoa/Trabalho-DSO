from entidade.pessoa import Pessoa
from excecoes.dado_invalido_exception import DadoInvalidoException


class ProfissionalSaude(Pessoa):
    def __init__(
        self,
        nome: str,
        celular: str,
        cpf: str,
        especialidade: str,
        registro_profissional: str,
    ):
        super().__init__(nome, celular, cpf)
        if not isinstance(especialidade, str) or not especialidade.strip():
            raise DadoInvalidoException("especialidade", "deve ser um texto não vazio")
        self.__especialidade = especialidade.strip()

        if not isinstance(registro_profissional, str) or not registro_profissional.strip():
            raise DadoInvalidoException("registro_profissional", "deve ser um texto não vazio")
        self.__registro_profissional = registro_profissional.strip()

    @property
    def especialidade(self) -> str:
        return self.__especialidade

    @especialidade.setter
    def especialidade(self, especialidade: str) -> None:
        if not isinstance(especialidade, str) or not especialidade.strip():
            raise DadoInvalidoException("especialidade", "deve ser um texto não vazio")
        self.__especialidade = especialidade.strip()

    @property
    def registro_profissional(self) -> str:
        return self.__registro_profissional

    @registro_profissional.setter
    def registro_profissional(self, registro_profissional: str) -> None:
        if not isinstance(registro_profissional, str) or not registro_profissional.strip():
            raise DadoInvalidoException("registro_profissional", "deve ser um texto não vazio")
        self.__registro_profissional = registro_profissional.strip()

    def __repr__(self) -> str:
        return (
            f"ProfissionalSaude(Nome: {self.nome}, Celular: {self.celular}, "
            f"CPF: {self.cpf}, Especialidade: {self.__especialidade}, "
            f"Registro: {self.__registro_profissional})"
        )

    def repr(self) -> str:
        return self.__repr__()
