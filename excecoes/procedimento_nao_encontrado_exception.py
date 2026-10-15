class ProcedimentoNaoEncontradoException(Exception):
    def __init__(self, identificador: str = ""):
        if identificador:
            mensagem = f"O procedimento '{identificador}' não foi encontrado no sistema."
        else:
            mensagem = "Procedimento não encontrado no sistema."
        super().__init__(mensagem)
