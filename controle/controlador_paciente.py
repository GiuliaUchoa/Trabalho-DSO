from entidade.paciente import Paciente
from excecoes.paciente_ja_cadastrado import PacienteJaCadastradoException
from excecoes.paciente_nao_encontrado import PacienteNaoEncontradoException

class ControladorPaciente:
    def __init__(self):
        self.__pacientes = []

    @property
    def pacientes(self) -> list[Paciente]:
        return self.__pacientes

    def buscar_paciente_por_cpf(self, cpf) -> Paciente:
        for paciente in self.__pacientes:
            if paciente.cpf == cpf:
                return paciente
        return None

    def cadastrar_paciente(self, nome, celular, cpf, data_nascimento) -> Paciente:
        if self.buscar_paciente_por_cpf(cpf) is not None:
            raise PacienteJaCadastradoException(cpf)

        novo_paciente = Paciente(nome, celular, cpf, data_nascimento)
        self.__pacientes.append(novo_paciente)
        return novo_paciente

    def excluir_paciente(self, cpf) -> None:
        paciente = self.buscar_paciente_por_cpf(cpf)
        if paciente is None:
            raise PacienteNaoEncontradoException(cpf)
        self.__pacientes.remove(paciente)

    def alterar_paciente(self, cpf, dados) -> None:
        paciente = self.buscar_paciente_por_cpf(cpf)
        if paciente is None:
            raise PacienteNaoEncontradoException(cpf)

        if dados['nome'] != "":
            paciente.nome = dados['nome']
        if dados['celular'] != "":
            paciente.celular = dados['celular']
        if dados['cpf'] != "":
            paciente.cpf = dados['cpf']
        if dados['data_nascimento'] != "":
            paciente.data_nascimento = dados['data_nascimento']

    def listar_pacientes(self) -> list[Paciente]:
        return self.__pacientes

#espaço para testes, excluir apos conclusao
if __name__ == "__main__":
    controlador = ControladorPaciente()
    controlador.cadastrar_paciente("João Silva", "11999999999", "12345678901", "10/01/1990")
    controlador.cadastrar_paciente("Maria Souza", "21988888888", "98765432100", "15/05/1985")
    controlador.alterar_paciente("98765432100", {'nome': '11111', 'celular': '1111111', 'cpf': '1111111', 'data_nascimento': '11/11/2002'})
    print(controlador.listar_pacientes())