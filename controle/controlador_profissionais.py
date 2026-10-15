from typing import Optional
from entidade.profissional_saude import ProfissionalSaude
from limite.tela_profissional import TelaProfissional
from excecoes.profissional_ja_cadastrado_exception import (
    ProfissionalJaCadastradoException,
    RegistroJaCadastradoException,
    CpfJaCadastradoException,
)
from excecoes.profissional_nao_encontrado_exception import ProfissionalNaoEncontradoException
from excecoes.dado_invalido_exception import DadoInvalidoException


class ControladorProfissionais:
    def __init__(self, controlador_sistema=None):
        self.__controlador_sistema = controlador_sistema
        self.__profissionais: list[ProfissionalSaude] = []
        self.__tela_profissional = TelaProfissional()

    @property
    def controlador_sistema(self):
        return self.__controlador_sistema

    @property
    def profissionais(self) -> list[ProfissionalSaude]:
        return self.__profissionais

    @property
    def tela_profissional(self) -> TelaProfissional:
        return self.__tela_profissional

    def retornar(self) -> None:
        pass

    def buscar_profissional(self, registro_profissional: str) -> Optional[ProfissionalSaude]:
        if not registro_profissional:
            return None
        for prof in self.__profissionais:
            if prof.registro_profissional.strip().lower() == registro_profissional.strip().lower():
                return prof
        return None

    def __buscar_por_cpf(self, cpf: str) -> Optional[ProfissionalSaude]:
        if not cpf:
            return None
        for prof in self.__profissionais:
            if prof.cpf.strip() == cpf.strip():
                return prof
        return None

    def buscar_profissional_por_cpf(self, cpf: str) -> Optional[ProfissionalSaude]:
        """
        Método legado mantido para compatibilidade interna.
        A busca principal deve sempre utilizar buscar_profissional(registro_profissional).
        """
        return self.__buscar_por_cpf(cpf)

    def cadastrar_profissional(
        self,
        nome: str,
        celular: str,
        cpf: str,
        especialidade: str,
        registro: str,
        clinica=None,
    ) -> ProfissionalSaude:
        if self.buscar_profissional(registro) is not None:
            raise RegistroJaCadastradoException(registro)

        if self.__buscar_por_cpf(cpf) is not None:
            raise CpfJaCadastradoException(cpf)

        novo_profissional = ProfissionalSaude(
            nome=nome,
            celular=celular,
            cpf=cpf,
            especialidade=especialidade,
            registro_profissional=registro,
            clinica=clinica,
        )
        self.__profissionais.append(novo_profissional)
        self.__tela_profissional.mostra_mensagem("Profissional cadastrado com sucesso!")
        return novo_profissional

    def excluir_profissional(self, registro_profissional: str) -> None:
        profissional = self.buscar_profissional(registro_profissional)
        if profissional is None:
            raise ProfissionalNaoEncontradoException(registro_profissional)

        if profissional.possui_clinica():
            profissional.clinica = None
        self.__profissionais.remove(profissional)
        self.__tela_profissional.mostra_mensagem("Profissional excluído com sucesso!")

    def alterar_profissional(self, registro_profissional: str, novos_dados: dict) -> None:
        profissional = self.buscar_profissional(registro_profissional)
        if profissional is None:
            raise ProfissionalNaoEncontradoException(registro_profissional)

        novo_registro = novos_dados.get("registro") or novos_dados.get("registro_profissional")
        if novo_registro and novo_registro.strip().lower() != profissional.registro_profissional.strip().lower():
            outro_prof = self.buscar_profissional(novo_registro)
            if outro_prof is not None and outro_prof != profissional:
                raise RegistroJaCadastradoException(novo_registro)
            profissional.registro_profissional = novo_registro

        novo_cpf = novos_dados.get("cpf")
        if novo_cpf and novo_cpf.strip() != profissional.cpf.strip():
            outro_prof = self.__buscar_por_cpf(novo_cpf)
            if outro_prof is not None and outro_prof != profissional:
                raise CpfJaCadastradoException(novo_cpf)
            profissional.cpf = novo_cpf

        if "nome" in novos_dados and novos_dados["nome"]:
            profissional.nome = novos_dados["nome"]
        if "celular" in novos_dados and novos_dados["celular"]:
            profissional.celular = novos_dados["celular"]
        if "especialidade" in novos_dados and novos_dados["especialidade"]:
            profissional.especialidade = novos_dados["especialidade"]
        if "clinica" in novos_dados:
            profissional.clinica = novos_dados["clinica"]

        self.__tela_profissional.mostra_mensagem("Profissional alterado com sucesso!")

    atualizar_profissional = alterar_profissional

    def listar_profissionais(self) -> list[ProfissionalSaude]:
        if not self.__profissionais:
            self.__tela_profissional.mostra_mensagem("Nenhum profissional cadastrado no sistema.")
            return self.__profissionais

        print("\n--- Lista de Profissionais de Saúde ---")
        for prof in self.__profissionais:
            dados = {
                "nome": prof.nome,
                "cpf": prof.cpf,
                "celular": prof.celular,
                "especialidade": prof.especialidade,
                "registro_profissional": prof.registro_profissional,
                "clinica": prof.clinica,
            }
            self.__tela_profissional.mostra_profissional(dados)

        return self.__profissionais

    # Fluxos de interação com a tela
    def __incluir_profissional_fluxo(self) -> None:
        try:
            dados = self.__tela_profissional.coletar_dados()
            self.cadastrar_profissional(
                nome=dados["nome"],
                celular=dados["celular"],
                cpf=dados["cpf"],
                especialidade=dados["especialidade"],
                registro=dados["registro"],
                clinica=None,
            )
        except (ProfissionalJaCadastradoException, DadoInvalidoException) as e:
            self.__tela_profissional.mostra_mensagem(f"Erro ao cadastrar profissional: {e}")

    def __excluir_profissional_fluxo(self) -> None:
        try:
            registro = self.__tela_profissional.buscar_profissional()
            self.excluir_profissional(registro)
        except ProfissionalNaoEncontradoException as e:
            self.__tela_profissional.mostra_mensagem(f"Erro ao excluir profissional: {e}")

    def __alterar_profissional_fluxo(self) -> None:
        try:
            registro = self.__tela_profissional.buscar_profissional()
            profissional = self.buscar_profissional(registro)
            if profissional is None:
                raise ProfissionalNaoEncontradoException(registro)

            self.__tela_profissional.mostra_profissional({
                "nome": profissional.nome,
                "cpf": profissional.cpf,
                "celular": profissional.celular,
                "especialidade": profissional.especialidade,
                "registro_profissional": profissional.registro_profissional,
                "clinica": profissional.clinica,
            })
            novos_dados = self.__tela_profissional.coletar_novos_dados()
            self.alterar_profissional(registro, novos_dados)
        except (ProfissionalNaoEncontradoException, ProfissionalJaCadastradoException, DadoInvalidoException) as e:
            self.__tela_profissional.mostra_mensagem(f"Erro ao alterar profissional: {e}")

    def __buscar_profissional_fluxo(self) -> None:
        try:
            registro = self.__tela_profissional.buscar_profissional()
            profissional = self.buscar_profissional(registro)
            if profissional is None:
                raise ProfissionalNaoEncontradoException(registro)

            self.__tela_profissional.mostra_profissional({
                "nome": profissional.nome,
                "cpf": profissional.cpf,
                "celular": profissional.celular,
                "especialidade": profissional.especialidade,
                "registro_profissional": profissional.registro_profissional,
                "clinica": profissional.clinica,
            })
        except ProfissionalNaoEncontradoException as e:
            self.__tela_profissional.mostra_mensagem(f"Erro na busca: {e}")

    def abre_tela(self) -> None:
        opcoes = {
            1: self.__incluir_profissional_fluxo,
            2: self.__excluir_profissional_fluxo,
            3: self.__alterar_profissional_fluxo,
            4: self.listar_profissionais,
            5: self.__buscar_profissional_fluxo,
            0: self.retornar,
        }

        while True:
            opcao_escolhida = self.__tela_profissional.opcoes_tela()
            funcao_escolhida = opcoes.get(opcao_escolhida)
            if funcao_escolhida:
                funcao_escolhida()
            if opcao_escolhida == 0:
                break


# Alias para garantir 100% de compatibilidade com a modelagem do diagrama UML
ControladorProfissionalSaude = ControladorProfissionais
