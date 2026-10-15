from entidade.profissional_saude import ProfissionalSaude
from excecoes.dado_invalido_exception import DadoInvalidoException


class Procedimento:
    def __init__(self, nome: str, descricao: str, custo: float, profissional_responsavel: ProfissionalSaude):
        self.nome = nome
        self.descricao = descricao
        self.custo = custo
        self.profissional_responsavel = profissional_responsavel

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if not isinstance(nome, str) or not nome.strip():
            raise DadoInvalidoException("nome", "deve ser um texto não vazio")
        self.__nome = nome.strip()

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str):
        if not isinstance(descricao, str) or not descricao.strip():
            raise DadoInvalidoException("descricao", "deve ser um texto não vazio")
        self.__descricao = descricao.strip()

    @property
    def custo(self):
        return self.__custo

    @custo.setter
    def custo(self, custo: float):
        if not isinstance(custo, (int, float)):
            raise DadoInvalidoException("custo", "deve ser um valor numérico")
        if custo < 0:
            raise DadoInvalidoException("custo", "não pode ser negativo")
        self.__custo = float(custo)

    @property
    def profissional_responsavel(self):
        return self.__profissional_responsavel

    @profissional_responsavel.setter
    def profissional_responsavel(self, profissional_responsavel: ProfissionalSaude):
        if not isinstance(profissional_responsavel, ProfissionalSaude):
            raise DadoInvalidoException("profissional_responsavel", "deve ser um profissional de saúde válido")
        self.__profissional_responsavel = profissional_responsavel
