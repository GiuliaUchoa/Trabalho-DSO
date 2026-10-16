from typing import Optional
from entidade.paciente import Paciente
from limite.tela_paciente import TelaPaciente
from excecoes.paciente_ja_cadastrado import PacienteJaCadastradoException
from excecoes.paciente_nao_encontrado import PacienteNaoEncontradoException


class ControladorPaciente:
    def __init__(self, controlador_sistema=None):
        self.__controlador_sistema = controlador_sistema
        self.__pacientes: list[Paciente] = []
        self.__tela_paciente = TelaPaciente()

    @property
    def controlador_sistema(self):
        return self.__controlador_sistema

    @property
    def pacientes(self) -> list[Paciente]:
        return self.__pacientes

    @property
    def tela_paciente(self) -> TelaPaciente:
        return self.__tela_paciente

    def retornar(self) -> None:
        pass

    def buscar_paciente_por_cpf(self, cpf: str) -> Optional[Paciente]:
        if not cpf:
            return None
        for paciente in self.__pacientes:
            if paciente.cpf.strip() == str(cpf).strip():
                return paciente
        return None

    def buscar_paciente(self, cpf: Optional[str] = None) -> Optional[Paciente]:
        if cpf is None:
            cpf = self.__tela_paciente.buscar_paciente()
        return self.buscar_paciente_por_cpf(cpf)

    def cadastrar_paciente(self, nome: str, celular: str, cpf: str, data_nascimento) -> Paciente:
        if self.buscar_paciente_por_cpf(cpf) is not None:
            raise PacienteJaCadastradoException(cpf)

        novo_paciente = Paciente(nome, celular, cpf, data_nascimento)
        self.__pacientes.append(novo_paciente)
        self.__tela_paciente.mostrar_mensagem("Paciente cadastrado com sucesso!")
        return novo_paciente

    def excluir_paciente(self, cpf: str) -> None:
        paciente = self.buscar_paciente_por_cpf(cpf)
        if paciente is None:
            raise PacienteNaoEncontradoException(cpf)
        self.__pacientes.remove(paciente)
        self.__tela_paciente.mostrar_mensagem(f"Paciente com CPF '{cpf}' excluído com sucesso!")

    def alterar_paciente(self, cpf: str, dados: dict) -> None:
        paciente = self.buscar_paciente_por_cpf(cpf)
        if paciente is None:
            raise PacienteNaoEncontradoException(cpf)

        if dados.get("nome"):
            paciente.nome = dados["nome"]
        if dados.get("celular"):
            paciente.celular = dados["celular"]
        if dados.get("data_nascimento"):
            paciente.data_nascimento = dados["data_nascimento"]

        self.__tela_paciente.mostrar_mensagem("Paciente atualizado com sucesso!")

    def listar_pacientes(self) -> list[Paciente]:
        return self.__pacientes

    def listar_pacientes_tela(self) -> list[Paciente]:
        if not self.__pacientes:
            self.__tela_paciente.mostrar_mensagem("Nenhum paciente cadastrado no sistema.")
            return self.__pacientes

        self.__tela_paciente.mostra_cabecalho_lista()
        for paciente in self.__pacientes:
            self.__tela_paciente.mostra_paciente({
                "nome": paciente.nome,
                "cpf": paciente.cpf,
                "celular": paciente.celular,
                "data_nascimento": paciente.data_nascimento,
            })
        return self.__pacientes

    # Fluxos de tela
    def __incluir_paciente_fluxo(self) -> None:
        try:
            dados = self.__tela_paciente.coletar_dados()
            self.cadastrar_paciente(
                nome=dados["nome"],
                celular=dados["celular"],
                cpf=dados["cpf"],
                data_nascimento=dados["data_nascimento"],
            )
        except (PacienteJaCadastradoException, Exception) as e:
            self.__tela_paciente.mostrar_mensagem(f"Erro ao cadastrar paciente: {e}")

    def __excluir_paciente_fluxo(self) -> None:
        try:
            cpf = self.__tela_paciente.buscar_paciente()
            self.excluir_paciente(cpf)
        except PacienteNaoEncontradoException as e:
            self.__tela_paciente.mostrar_mensagem(f"Erro ao excluir paciente: {e}")

    def __alterar_paciente_fluxo(self) -> None:
        try:
            cpf = self.__tela_paciente.buscar_paciente()
            paciente = self.buscar_paciente_por_cpf(cpf)
            if paciente is None:
                raise PacienteNaoEncontradoException(cpf)

            self.__tela_paciente.mostra_paciente({
                "nome": paciente.nome,
                "cpf": paciente.cpf,
                "celular": paciente.celular,
                "data_nascimento": paciente.data_nascimento,
            })
            novos_dados = self.__tela_paciente.coletar_novos_dados()
            if novos_dados:
                self.alterar_paciente(cpf, novos_dados)
        except PacienteNaoEncontradoException as e:
            self.__tela_paciente.mostrar_mensagem(f"Erro ao alterar paciente: {e}")

    def __buscar_paciente_fluxo(self) -> None:
        cpf = self.__tela_paciente.buscar_paciente()
        paciente = self.buscar_paciente_por_cpf(cpf)
        if paciente is not None:
            self.__tela_paciente.mostra_paciente({
                "nome": paciente.nome,
                "cpf": paciente.cpf,
                "celular": paciente.celular,
                "data_nascimento": paciente.data_nascimento,
            })
        else:
            self.__tela_paciente.mostrar_mensagem(f"Paciente com CPF '{cpf}' não encontrado.")

    def abre_tela(self) -> None:
        opcoes = {
            1: self.__incluir_paciente_fluxo,
            2: self.__excluir_paciente_fluxo,
            3: self.__alterar_paciente_fluxo,
            4: self.listar_pacientes_tela,
            5: self.__buscar_paciente_fluxo,
            0: self.retornar,
        }

        while True:
            opcao_escolhida = self.__tela_paciente.opcoes_tela()
            funcao_escolhida = opcoes.get(opcao_escolhida)
            if funcao_escolhida:
                funcao_escolhida()
            if opcao_escolhida == 0:
                break