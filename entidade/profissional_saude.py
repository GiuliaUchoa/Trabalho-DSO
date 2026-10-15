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
        self.__especialidade = especialidade
        self.__registro_profissional = registro_profissional
        self.__esta_empregado = False

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
    def esta_empregado(self):
        return self.__esta_empregado
    @esta_empregado.setter
    def esta_empregado(self, esta_empregado):
        self.__esta_empregado = esta_empregado

    def __repr__(self):
        return f"Profissional(Nome: {self.nome}, Celular: {self.celular}, CPF: {self.cpf}, Especialidade: {self.__especialidade}, Registro profissional: {self.__registro_profissional})"

if __name__ == '__main__':
    profissional = ProfissionalSaude('Fulano', '55 123', '001', 'dente', 'crm')
    profissional.especialidade = 'queixo'
    profissional.esta_empregado = True
    print(profissional.especialidade, profissional.registro_profissional, profissional.esta_empregado)