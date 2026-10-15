class ProfissionalJaCadastradoException(Exception):
    def __init__(self, identificador: str = ""):
        if identificador:
             mensagem = f"Já existe um profissional cadastrado com o identificador '{identificador}'."
        else:
            mensagem = "Já existe um profissional de saúde cadastrado com estes dados."
        super().__init__(mensagem)

