class ProcedimentoJaCadastradoException(Exception):
    def __init__(self, identificador: str = ""):
        if identificador:
            mensagem = f"Já existe um procedimento cadastrado com o nome '{identificador}'."
        else:
            mensagem = "Já existe um procedimento cadastrado com estes dados."
        super().__init__(mensagem)
