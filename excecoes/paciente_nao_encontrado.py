class PacienteNaoEncontradoException(Exception):
    def __init__(self, cpf):
        mensagem = f"O paciente com CPF {cpf} não foi encontrado no sistema."
        super().__init__(mensagem)