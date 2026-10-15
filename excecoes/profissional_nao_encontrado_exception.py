class ProfissionalNaoEncontradoException(Exception):
    def __init__(self, identificador: str = ""):
        if identificador:
            mensagem = f"O profissional '{identificador}' não foi encontrado no sistema."
        else:
            mensagem = "Profissional de saúde não encontrado no sistema."
        super().__init__(mensagem)
