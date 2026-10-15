from controle.controlador import Controlador
from entidade.tipo_atendimento import TipoAtendimento
from limite.tela_tipo_atendimento import TelaTipoAtendimento
from excecoes.tipo_atendimento_ja_cadastrado_exception import TipoAtendimentoJaCadastradoException
from excecoes.tipo_atendimento_nao_encontrado_exception import TipoAtendimentoNaoEncontradoException
from excecoes.dado_invalido_exception import DadoInvalidoException


class ControladorTipoAtendimento(Controlador):
    def __init__(self, controlador_sistema=None):
        super().__init__(controlador_sistema)
        self.__tipos_atendimentos = []
        self.__tela_tipo_atendimento = TelaTipoAtendimento()

    @property
    def tipos_atendimentos(self):
        return self.__tipos_atendimentos

    @property
    def tela_tipo_atendimento(self):
        return self.__tela_tipo_atendimento

    def buscar_tipo_atendimento(self, nome_tipo: str):
        if not nome_tipo:
            return None
        for tipo in self.__tipos_atendimentos:
            if tipo.nome_tipo.lower() == nome_tipo.strip().lower():
                return tipo
        return None

    def cadastrar_tipo_atendimento(self, nome_tipo: str):
        if self.buscar_tipo_atendimento(nome_tipo) is not None:
            raise TipoAtendimentoJaCadastradoException(nome_tipo)

        novo_tipo = TipoAtendimento(nome_tipo)
        self.__tipos_atendimentos.append(novo_tipo)
        self.__tela_tipo_atendimento.mostra_mensagem("Tipo de atendimento cadastrado com sucesso!")
        return novo_tipo

    def excluir_tipo_atendimento(self, nome_tipo: str):
        tipo = self.buscar_tipo_atendimento(nome_tipo)
        if tipo is None:
            raise TipoAtendimentoNaoEncontradoException(nome_tipo)

        self.__tipos_atendimentos.remove(tipo)
        self.__tela_tipo_atendimento.mostra_mensagem("Tipo de atendimento excluído com sucesso!")

    def alterar_tipo_atendimento(self, nome_tipo: str, novo_nome: str):
        tipo = self.buscar_tipo_atendimento(nome_tipo)
        if tipo is None:
            raise TipoAtendimentoNaoEncontradoException(nome_tipo)

        if not novo_nome or not novo_nome.strip():
            raise DadoInvalidoException("nome_tipo", "deve ser um texto não vazio")

        outro = self.buscar_tipo_atendimento(novo_nome)
        if outro is not None and outro != tipo:
            raise TipoAtendimentoJaCadastradoException(novo_nome)

        tipo.nome_tipo = novo_nome
        self.__tela_tipo_atendimento.mostra_mensagem("Tipo de atendimento alterado com sucesso!")

    def listar_tipos(self):
        if not self.__tipos_atendimentos:
            self.__tela_tipo_atendimento.mostra_mensagem("Nenhum tipo de atendimento cadastrado no sistema.")
            return self.__tipos_atendimentos

        print("\n--- Lista de Tipos de Atendimento ---")
        for tipo in self.__tipos_atendimentos:
            self.__tela_tipo_atendimento.mostra_tipo_atendimento({"nome_tipo": tipo.nome_tipo})

        return self.__tipos_atendimentos

    listar_tipos_atendimento = listar_tipos

    # Fluxos de tela
    def __incluir_tipo_atendimento_fluxo(self):
        try:
            dados = self.__tela_tipo_atendimento.coletar_dados()
            self.cadastrar_tipo_atendimento(dados["nome_tipo"])
        except (TipoAtendimentoJaCadastradoException, DadoInvalidoException) as e:
            self.__tela_tipo_atendimento.mostra_mensagem(f"Erro ao cadastrar tipo de atendimento: {e}")

    def __excluir_tipo_atendimento_fluxo(self):
        try:
            nome_tipo = self.__tela_tipo_atendimento.seleciona_tipo_atendimento()
            self.excluir_tipo_atendimento(nome_tipo)
        except TipoAtendimentoNaoEncontradoException as e:
            self.__tela_tipo_atendimento.mostra_mensagem(f"Erro ao excluir tipo de atendimento: {e}")

    def __alterar_tipo_atendimento_fluxo(self):
        try:
            nome_tipo = self.__tela_tipo_atendimento.seleciona_tipo_atendimento()
            tipo = self.buscar_tipo_atendimento(nome_tipo)
            if tipo is None:
                raise TipoAtendimentoNaoEncontradoException(nome_tipo)

            self.__tela_tipo_atendimento.mostra_tipo_atendimento({"nome_tipo": tipo.nome_tipo})
            novo_nome = self.__tela_tipo_atendimento.coletar_novos_dados()
            if novo_nome:
                self.alterar_tipo_atendimento(nome_tipo, novo_nome)
        except (TipoAtendimentoNaoEncontradoException, TipoAtendimentoJaCadastradoException, DadoInvalidoException) as e:
            self.__tela_tipo_atendimento.mostra_mensagem(f"Erro ao alterar tipo de atendimento: {e}")

    def __buscar_tipo_atendimento_fluxo(self):
        try:
            nome_tipo = self.__tela_tipo_atendimento.seleciona_tipo_atendimento()
            tipo = self.buscar_tipo_atendimento(nome_tipo)
            if tipo is None:
                raise TipoAtendimentoNaoEncontradoException(nome_tipo)

            self.__tela_tipo_atendimento.mostra_tipo_atendimento({"nome_tipo": tipo.nome_tipo})
        except TipoAtendimentoNaoEncontradoException as e:
            self.__tela_tipo_atendimento.mostra_mensagem(f"Erro na busca: {e}")

    def abre_tela(self):
        opcoes = {
            1: self.__incluir_tipo_atendimento_fluxo,
            2: self.__excluir_tipo_atendimento_fluxo,
            3: self.__alterar_tipo_atendimento_fluxo,
            4: self.listar_tipos,
            5: self.__buscar_tipo_atendimento_fluxo,
            0: self.retornar,
        }

        while True:
            opcao_escolhida = self.__tela_tipo_atendimento.opcoes_tela()
            funcao_escolhida = opcoes.get(opcao_escolhida)
            if funcao_escolhida:
                funcao_escolhida()
            if opcao_escolhida == 0:
                break
