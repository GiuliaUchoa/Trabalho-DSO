class ProfissionalJaCadastradoException(Exception):
    def __init__(self, identificador: str = ""):
        if identificador:
            mensagem = f"Já existe um profissional cadastrado com o identificador '{identificador}'."
        else:
            mensagem = "Já existe um profissional de saúde cadastrado com estes dados."
        super().__init__(mensagem)


class RegistroJaCadastradoException(ProfissionalJaCadastradoException):
    def __init__(self, registro: str = ""):
        if registro:
            mensagem = f"Já existe um profissional cadastrado com o Registro Profissional '{registro}'."
        else:
            mensagem = "Já existe um profissional cadastrado com este Registro Profissional."
        super().__init__(mensagem)


class CpfJaCadastradoException(ProfissionalJaCadastradoException):
    def __init__(self, cpf: str = ""):
        if cpf:
            mensagem = f"Já existe um profissional cadastrado com o CPF '{cpf}'."
        else:
            mensagem = "Já existe um profissional cadastrado com este CPF."
        super().__init__(mensagem)
