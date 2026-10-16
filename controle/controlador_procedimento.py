from entidade.procedimento import Procedimento
from limite.tela_procedimento import TelaProcedimento
from excecoes.procedimento_ja_cadastrado_exception import ProcedimentoJaCadastradoException
from excecoes.procedimento_nao_encontrado_exception import ProcedimentoNaoEncontradoException
from excecoes.profissional_nao_encontrado_exception import ProfissionalNaoEncontradoException
from excecoes.dado_invalido_exception import DadoInvalidoException


class ControladorProcedimento:
    def __init__(self, controlador_profissionais=None, controlador_sistema=None):
        if hasattr(controlador_profissionais, "buscar_profissional"):
            self.__controlador_profissionais = controlador_profissionais
            self.__controlador_sistema = controlador_sistema
        else:
            self.__controlador_sistema = controlador_profissionais or controlador_sistema
            self.__controlador_profissionais = None
        self.__procedimentos = []
        self.__tela_procedimento = TelaProcedimento()

    @property
    def controlador_profissionais(self):
        if self.__controlador_profissionais is not None:
            return self.__controlador_profissionais
        if self.__controlador_sistema is not None:
            return getattr(self.__controlador_sistema, "controlador_profissional", None) or getattr(self.__controlador_sistema, "controlador_profissionais", None)
        return None

    @property
    def controlador_sistema(self):
        return self.__controlador_sistema

    @property
    def procedimentos(self):
        return self.__procedimentos

    @property
    def tela_procedimento(self):
        return self.__tela_procedimento

    def retornar(self) -> None:
        pass

    def buscar_procedimento(self, nome: str):
        if not nome:
            return None
        for proc in self.__procedimentos:
            if proc.nome.lower() == nome.lower():
                return proc
        return None

    def cadastrar_procedimento(self, nome: str, descricao: str, custo: float, profissional_responsavel):
        if self.buscar_procedimento(nome) is not None:
            raise ProcedimentoJaCadastradoException(nome)

        novo_procedimento = Procedimento(nome, descricao, custo, profissional_responsavel)
        self.__procedimentos.append(novo_procedimento)
        self.__tela_procedimento.mostrar_mensagem("Procedimento cadastrado com sucesso!")
        return novo_procedimento

    def excluir_procedimento(self, nome: str):
        procedimento = self.buscar_procedimento(nome)
        if procedimento is None:
            raise ProcedimentoNaoEncontradoException(nome)

        self.__procedimentos.remove(procedimento)
        self.__tela_procedimento.mostrar_mensagem("Procedimento excluído com sucesso!")

    def alterar_procedimento(self, nome: str, novos_dados: dict):
        procedimento = self.buscar_procedimento(nome)
        if procedimento is None:
            raise ProcedimentoNaoEncontradoException(nome)

        if "nome" in novos_dados and novos_dados["nome"]:
            novo_nome = novos_dados["nome"]
            outro = self.buscar_procedimento(novo_nome)
            if outro is not None and outro != procedimento:
                raise ProcedimentoJaCadastradoException(novo_nome)
            procedimento.nome = novo_nome

        if "descricao" in novos_dados and novos_dados["descricao"]:
            procedimento.descricao = novos_dados["descricao"]

        if "custo" in novos_dados and novos_dados["custo"] is not None:
            procedimento.custo = novos_dados["custo"]

        if "profissional_responsavel" in novos_dados and novos_dados["profissional_responsavel"] is not None:
            procedimento.profissional_responsavel = novos_dados["profissional_responsavel"]

        self.__tela_procedimento.mostrar_mensagem("Procedimento alterado com sucesso!")

    def listar_procedimentos(self):
        if not self.__procedimentos:
            self.__tela_procedimento.mostrar_mensagem("Nenhum procedimento cadastrado no sistema.")
            return self.__procedimentos

        self.__tela_procedimento.mostra_cabecalho_lista()
        for proc in self.__procedimentos:
            dados = {
                "nome": proc.nome,
                "descricao": proc.descricao,
                "custo": proc.custo,
                "profissional_responsavel": proc.profissional_responsavel,
            }
            self.__tela_procedimento.mostra_procedimento(dados)

        return self.__procedimentos

    # Fluxos de tela
    def __incluir_procedimento_fluxo(self):
        try:
            dados = self.__tela_procedimento.coletar_dados()
            registro = dados["registro_profissional"]

            profissional = None
            ctrl_prof = self.controlador_profissionais
            if ctrl_prof is not None:
                profissional = ctrl_prof.buscar_profissional(registro)

            if profissional is None:
                raise ProfissionalNaoEncontradoException(registro)

            self.cadastrar_procedimento(
                dados["nome"],
                dados["descricao"],
                dados["custo"],
                profissional,
            )
        except (ProcedimentoJaCadastradoException, ProfissionalNaoEncontradoException, DadoInvalidoException, ValueError) as e:
            self.__tela_procedimento.mostrar_mensagem(f"Erro ao cadastrar procedimento: {e}")

    def __excluir_procedimento_fluxo(self):
        try:
            nome = self.__tela_procedimento.seleciona_procedimento()
            self.excluir_procedimento(nome)
        except ProcedimentoNaoEncontradoException as e:
            self.__tela_procedimento.mostrar_mensagem(f"Erro ao excluir procedimento: {e}")

    def __alterar_procedimento_fluxo(self):
        try:
            nome = self.__tela_procedimento.seleciona_procedimento()
            procedimento = self.buscar_procedimento(nome)
            if procedimento is None:
                raise ProcedimentoNaoEncontradoException(nome)

            self.__tela_procedimento.mostra_procedimento({
                "nome": procedimento.nome,
                "descricao": procedimento.descricao,
                "custo": procedimento.custo,
                "profissional_responsavel": procedimento.profissional_responsavel,
            })
            novos_dados = self.__tela_procedimento.coletar_novos_dados()

            if "registro_profissional" in novos_dados:
                registro = novos_dados["registro_profissional"]
                profissional = None
                ctrl_prof = self.controlador_profissionais
                if ctrl_prof is not None:
                    profissional = ctrl_prof.buscar_profissional(registro)

                if profissional is None:
                    raise ProfissionalNaoEncontradoException(registro)
                novos_dados["profissional_responsavel"] = profissional

            self.alterar_procedimento(nome, novos_dados)
        except (
            ProcedimentoNaoEncontradoException,
            ProcedimentoJaCadastradoException,
            ProfissionalNaoEncontradoException,
            DadoInvalidoException,
            ValueError,
        ) as e:
            self.__tela_procedimento.mostrar_mensagem(f"Erro ao alterar procedimento: {e}")

    def __buscar_procedimento_fluxo(self):
        try:
            nome = self.__tela_procedimento.seleciona_procedimento()
            procedimento = self.buscar_procedimento(nome)
            if procedimento is None:
                raise ProcedimentoNaoEncontradoException(nome)

            self.__tela_procedimento.mostra_procedimento({
                "nome": procedimento.nome,
                "descricao": procedimento.descricao,
                "custo": procedimento.custo,
                "profissional_responsavel": procedimento.profissional_responsavel,
            })
        except ProcedimentoNaoEncontradoException as e:
            self.__tela_procedimento.mostrar_mensagem(f"Erro na busca: {e}")

    def abre_tela(self):
        opcoes = {
            1: self.__incluir_procedimento_fluxo,
            2: self.__excluir_procedimento_fluxo,
            3: self.__alterar_procedimento_fluxo,
            4: self.listar_procedimentos,
            5: self.__buscar_procedimento_fluxo,
            0: self.retornar,
        }

        while True:
            opcao_escolhida = self.__tela_procedimento.opcoes_tela()
            funcao_escolhida = opcoes.get(opcao_escolhida)
            if funcao_escolhida:
                funcao_escolhida()
            if opcao_escolhida == 0:
                break
