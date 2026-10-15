class ClinicaJaCadastradaException(Exception):
    def __init__(self, nome: str = ""):
        if nome:
            mensagem = f"A clínica '{nome}' já está cadastrada no sistema."
        else:
            mensagem = "Já existe uma clínica cadastrada com este nome."
        super().__init__(mensagem)
