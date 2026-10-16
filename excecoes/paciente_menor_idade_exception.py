class PacienteMenorIdadeException(Exception):
    def __init__(self, mensagem="Somente pacientes com mais de 18 anos completos podem realizar atendimentos de forma independente."):
        super().__init__(mensagem)
