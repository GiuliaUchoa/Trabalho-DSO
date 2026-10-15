class DadoInvalidoException(Exception):
    def __init__(self, campo: str = "", motivo: str = ""):
        if campo and motivo:
            mensagem = f"Dado inválido para o campo '{campo}': {motivo}."
        elif campo:
            mensagem = f"O campo '{campo}' contém um valor inválido."
        else:
            mensagem = "Um ou mais dados informados são inválidos."
        super().__init__(mensagem)
