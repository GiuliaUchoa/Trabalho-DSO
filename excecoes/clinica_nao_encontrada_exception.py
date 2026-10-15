class ClinicaNaoEncontradaException(Exception):
    def __init__(self, nome: str = ""):
        if nome:
            mensagem = f"A clínica '{nome}' não foi encontrada."
        else:
            mensagem = "A clínica informada não foi encontrada no sistema."
        super().__init__(mensagem)
