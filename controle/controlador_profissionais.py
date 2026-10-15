from entidade.profissional_saude import ProfissionalSaude
from excecoes.profissional_ja_cadastrado_exception import (
    ProfissionalJaCadastradoException
    )
from excecoes.profissional_nao_encontrado_exception import ProfissionalNaoEncontradoException
from excecoes.dado_invalido_exception import DadoInvalidoException


class ControladorProfissionais():
    def __init__(self, controlador_sistema=None):
        self.__profissionais = []
        self.__controlador_sistema = controlador_sistema

    @property
    def profissionais(self) -> list[ProfissionalSaude]:
        return self.__profissionais

    def buscar_profissional(self, registro_profissional: str):
        if not registro_profissional:
            raise DadoInvalidoException('registro_profissional', 'o valor é vazio')
        for prof in self.__profissionais:
            if prof.registro_profissional.strip().lower() == registro_profissional.strip().lower():
                return prof
        return None

    def buscar_profissional_por_cpf(self, cpf: str):
        if not cpf:
            raise DadoInvalidoException('cpf', 'o valor é vazio')
        for prof in self.__profissionais:
            if prof.cpf.strip() == cpf.strip():
                return prof
        return None

    def cadastrar_profissional(
        self,
        nome: str,
        celular: str,
        cpf: str,
        especialidade: str,
        registro: str,
    ) -> ProfissionalSaude:
        if self.buscar_profissional(registro) is not None and self.buscar_profissional_por_cpf(cpf) is not None:
            raise ProfissionalJaCadastradoException()

        novo_profissional = ProfissionalSaude(
            nome=nome,
            celular=celular,
            cpf=cpf,
            especialidade=especialidade,
            registro_profissional=registro,
        )
        self.__profissionais.append(novo_profissional)

    def excluir_profissional(self, registro_profissional: str) -> None:
        profissional = self.buscar_profissional(registro_profissional)
        if profissional is None:
            raise ProfissionalNaoEncontradoException(registro_profissional)

        self.__profissionais.remove(profissional)

    def alterar_profissional(self, registro_profissional: str, dados: dict) -> None:
        profissional = self.buscar_profissional(registro_profissional)
        if profissional is None:
            raise ProfissionalNaoEncontradoException(registro_profissional)
        
        if dados['nome'] != "":
            profissional.nome = dados['nome']
        if dados['celular'] != "":
            profissional.celular = dados['celular']
        if dados['cpf'] != "":
            profissional.cpf = dados['cpf']
        if dados['especialidade'] != "":
            profissional.especialidade = dados['especialidade']
        if dados['registro_profissional'] != '':
            profissional.registro_profissional = dados['registro_profissional']

    def listar_profissionais(self) -> list[ProfissionalSaude]:
        return self.__profissionais

if __name__ == '__main__':
    controlador = ControladorProfissionais()
    controlador.cadastrar_profissional('nome', '55 69', '001', 'dente', 'crm')
    print(controlador.listar_profissionais())
    controlador.alterar_profissional('crm', {'nome': '11111', 'celular': '1111111', 'cpf': '1111111', 'especialidade': 'testando', 'registro_profissional': 'galera'})
    print(controlador.buscar_profissional(''))
    controlador.excluir_profissional('galera')
    print(controlador.buscar_profissional_por_cpf('001'))
    print(controlador.listar_profissionais())
