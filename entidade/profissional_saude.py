from typing import TYPE_CHECKING, Optional
from entidade.pessoa import Pessoa
from excecoes.dado_invalido_exception import DadoInvalidoException

if TYPE_CHECKING:
    from entidade.clinica import Clinica


class ProfissionalSaude(Pessoa):
    def __init__(
        self,
        nome: str,
        celular: str,
        cpf: str,
        especialidade: str,
        registro_profissional: str,
        clinica: Optional["Clinica"] = None,
    ):
        super().__init__(nome, celular, cpf)
        self.especialidade = especialidade
        self.registro_profissional = registro_profissional
        self.__clinica = None
        if clinica is not None:
            self.clinica = clinica

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

    @property
    def clinica(self) -> Optional["Clinica"]:
        return self.__clinica

    @clinica.setter
    def clinica(self, clinica: Optional["Clinica"]) -> None:
        if clinica is None:
            antiga = self.__clinica
            self.__clinica = None
            if antiga is not None and self in antiga.profissionais:
                antiga.remover_profissional(self)
            return

        from entidade.clinica import Clinica

        if not isinstance(clinica, Clinica):
            raise DadoInvalidoException("clinica", "deve ser uma instância válida de Clinica")

        antiga = self.__clinica
        self.__clinica = clinica
        if antiga is not None and antiga != clinica and self in antiga.profissionais:
            antiga.remover_profissional(self)
        if self not in clinica.profissionais:
            clinica.adicionar_profissional(self)

    def possui_clinica(self) -> bool:
        return self.__clinica is not None
