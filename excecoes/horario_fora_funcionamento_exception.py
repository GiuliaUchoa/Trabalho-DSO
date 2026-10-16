class HorarioForaFuncionamentoException(Exception):
    def __init__(self, mensagem="O horário do atendimento deve ocorrer estritamente dentro do período de funcionamento da clínica."):
        super().__init__(mensagem)
