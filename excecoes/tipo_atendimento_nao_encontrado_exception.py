class TipoAtendimentoNaoEncontradoException(Exception):
    def __init__(self, identificador: str = ""):
        if identificador:
            mensagem = f"O tipo de atendimento '{identificador}' não foi encontrado no sistema."
        else:
            mensagem = "Tipo de atendimento não encontrado no sistema."
        super().__init__(mensagem)
