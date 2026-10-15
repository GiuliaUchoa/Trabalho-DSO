class HorarioInvalidoException(Exception):
    def __init__(self, mensagem: str = "O horário informado é inválido para o funcionamento da clínica."):
        super().__init__(mensagem)
