from entidade.pessoa import Pessoa
from typing import TYPE_CHECKING, Optional

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
        self.__especialidade = especialidade
        self.__registro_profissional = registro_profissional
        self.__clinica = None
        if clinica is not None:
            self.clinica = clinica

    @property
    def especialidade(self) -> str:
        return self.__especialidade

    @especialidade.setter
    def especialidade(self, especialidade: str) -> None:
        if isinstance(especialidade, str):
            self.__especialidade = especialidade

    @property
    def registro_profissional(self) -> str:
        return self.__registro_profissional

    @registro_profissional.setter
    def registro_profissional(self, registro_profissional: str) -> None:
        if isinstance(registro_profissional, str):
            self.__registro_profissional = registro_profissional

    @property
    def clinica(self) -> Optional["Clinica"]:
        return self.__clinica

    @clinica.setter
    def clinica(self, clinica: Optional["Clinica"]) -> None:
        # Se estiver desvinculando da clínica atual
        if clinica is None:
            antiga = self.__clinica
            self.__clinica = None
            if antiga is not None and self in antiga.profissionais:
                antiga.remover_profissional(self)
            return

        from entidade.clinica import Clinica

        if isinstance(clinica, Clinica):
            antiga = self.__clinica
            self.__clinica = clinica
            if antiga is not None and antiga != clinica and self in antiga.profissionais:
                antiga.remover_profissional(self)
            if self not in clinica.profissionais:
                clinica.adicionar_profissional(self)

    def possui_clinica(self) -> bool:
        return self.__clinica is not None
