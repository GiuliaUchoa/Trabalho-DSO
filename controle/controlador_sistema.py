from limite.tela_sistema import TelaSistema
from controle.controlador_clinica import ControladorClinica
from controle.controlador_paciente import ControladorPaciente
from controle.controlador_profissionais import ControladorProfissionais
from controle.controlador_procedimento import ControladorProcedimento
from controle.controlador_tipo_atendimento import ControladorTipoAtendimento


class ControladorSistema:
    def __init__(self):
        self.__controlador_clinica = ControladorClinica()
        self.__controlador_paciente = ControladorPaciente()
        self.__controlador_profissionais = ControladorProfissionais()
        self.__controlador_procedimento = ControladorProcedimento(controlador_profissionais=self.__controlador_profissionais)
        self.__controlador_tipo_atendimento = ControladorTipoAtendimento()
        self.__tela_sistema = TelaSistema()

    @property
    def controlador_clinica(self) -> ControladorClinica:
        return self.__controlador_clinica

    @property
    def controlador_paciente(self) -> ControladorPaciente:
        return self.__controlador_paciente

    @property
    def controlador_profissionais(self) -> ControladorProfissionais:
        return self.__controlador_profissionais

    @property
    def controlador_profissional(self) -> ControladorProfissionais:
        return self.__controlador_profissionais

    @property
    def controlador_procedimento(self) -> ControladorProcedimento:
        return self.__controlador_procedimento

    @property
    def controlador_tipo_atendimento(self) -> ControladorTipoAtendimento:
        return self.__controlador_tipo_atendimento

    @property
    def tela_sistema(self) -> TelaSistema:
        return self.__tela_sistema

    def inicializa_sistema(self) -> None:
        self.abre_tela()

    def abre_clinicas(self) -> None:
        self.__controlador_clinica.abre_tela()

    def abre_pacientes(self) -> None:
        self.__controlador_paciente.abre_tela()

    def abre_profissionais(self) -> None:
        self.__controlador_profissionais.abre_tela()

    def abre_procedimentos(self) -> None:
        self.__controlador_procedimento.abre_tela()

    def abre_tipos_atendimento(self) -> None:
        self.__controlador_tipo_atendimento.abre_tela()

    def encerra_sistema(self) -> None:
        self.__tela_sistema.mostra_mensagem("Sistema encerrado com sucesso.")
        exit(0)

    def abre_tela(self) -> None:
        opcoes = {
            1: self.abre_clinicas,
            2: self.abre_pacientes,
            3: self.abre_profissionais,
            4: self.abre_procedimentos,
            5: self.abre_tipos_atendimento,
            0: self.encerra_sistema,
        }

        while True:
            opcao_escolhida = self.__tela_sistema.opcoes_tela()
            funcao_escolhida = opcoes.get(opcao_escolhida)
            if funcao_escolhida:
                funcao_escolhida()
