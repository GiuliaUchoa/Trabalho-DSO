class AtendimentoNaoEncontradoException(Exception):
    def __init__(self, identificador=""):
        if identificador:
            mensagem = f"O atendimento '{identificador}' não foi encontrado no sistema."
        else:
            mensagem = "O atendimento informado não foi encontrado."
        super().__init__(mensagem)
