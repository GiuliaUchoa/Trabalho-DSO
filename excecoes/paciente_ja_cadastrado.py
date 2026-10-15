class PacienteJaCadastradoException(Exception):
    def __init__(self, cpf):
        mensagem = f"O paciente com CPF {cpf} já está cadastrado no sistema."
        super().__init__(mensagem)