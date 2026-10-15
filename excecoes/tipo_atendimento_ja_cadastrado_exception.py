class TipoAtendimentoJaCadastradoException(Exception):
    def __init__(self, identificador: str = ""):
        if identificador:
            mensagem = f"Já existe um tipo de atendimento cadastrado com o nome '{identificador}'."
        else:
            mensagem = "Já existe um tipo de atendimento cadastrado com estes dados."
        super().__init__(mensagem)
