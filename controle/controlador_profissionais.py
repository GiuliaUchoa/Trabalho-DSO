from typing import Optional
from controle.controlador import Controlador
from entidade.profissional_saude import ProfissionalSaude
from limite.tela_profissional import TelaProfissional


class ControladorProfissionais(Controlador):
    def __init__(self, controlador_sistema=None):
        super().__init__(controlador_sistema)
        self.__profissionais: list[ProfissionalSaude] = []
        self.__tela_profissional = TelaProfissional()

    @property
    def profissionais(self) -> list[ProfissionalSaude]:
        return self.__profissionais

    @property
    def tela_profissional(self) -> TelaProfissional:
        return self.__tela_profissional

    def buscar_profissional(self, registro_profissional: str) -> Optional[ProfissionalSaude]:
        for prof in self.__profissionais:
            if prof.registro_profissional.strip().lower() == registro_profissional.strip().lower():
                return prof
        return None

    def buscar_profissional_por_cpf(self, cpf: str) -> Optional[ProfissionalSaude]:
        for prof in self.__profissionais:
            if prof.cpf.strip() == cpf.strip():
                return prof
        return None

    def cadastrar_profissional(
        self,
        nome: str,
        celular: str,
        cpf: str,
        especialidade: str,
        registro: str,
        clinica=None,
    ) -> None:
        if self.buscar_profissional_por_cpf(cpf) is not None:
            self.__tela_profissional.mostra_mensagem("Atenção: Já existe um profissional cadastrado com este CPF!")
            return

        if self.buscar_profissional(registro) is not None:
            self.__tela_profissional.mostra_mensagem("Atenção: Já existe um profissional cadastrado com este Registro Profissional!")
            return

        novo_profissional = ProfissionalSaude(
            nome=nome,
            celular=celular,
            cpf=cpf,
            especialidade=especialidade,
            registro_profissional=registro,
            clinica=clinica,
        )
        self.__profissionais.append(novo_profissional)
        self.__tela_profissional.mostra_mensagem("Profissional cadastrado com sucesso!")

    def excluir_profissional(self, cpf: str) -> None:
        profissional = self.buscar_profissional_por_cpf(cpf)
        if profissional is not None:
            if profissional.possui_clinica():
                profissional.clinica = None
            self.__profissionais.remove(profissional)
            self.__tela_profissional.mostra_mensagem("Profissional excluído com sucesso!")
        else:
            self.__tela_profissional.mostra_mensagem("Erro: Não foi encontrado profissional com o CPF informado.")

    def atualizar_profissional(self, cpf: str, novos_dados: dict) -> None:
        profissional = self.buscar_profissional_por_cpf(cpf)
        if profissional is None:
            self.__tela_profissional.mostra_mensagem("Erro: Não foi encontrado profissional com o CPF informado.")
            return

        if "nome" in novos_dados and novos_dados["nome"]:
            profissional.nome = novos_dados["nome"]
        if "celular" in novos_dados and novos_dados["celular"]:
            profissional.celular = novos_dados["celular"]
        if "especialidade" in novos_dados and novos_dados["especialidade"]:
            profissional.especialidade = novos_dados["especialidade"]
        if "registro" in novos_dados and novos_dados["registro"]:
            outro_prof = self.buscar_profissional(novos_dados["registro"])
            if outro_prof is not None and outro_prof != profissional:
                self.__tela_profissional.mostra_mensagem("Atenção: Já existe outro profissional com esse Registro!")
                return
            profissional.registro_profissional = novos_dados["registro"]
        if "clinica" in novos_dados:
            profissional.clinica = novos_dados["clinica"]

        self.__tela_profissional.mostra_mensagem("Profissional atualizado com sucesso!")

    def listar_profissionais(self) -> list[ProfissionalSaude]:
        if not self.__profissionais:
            self.__tela_profissional.mostra_mensagem("Nenhum profissional cadastrado no sistema.")
            return self.__profissionais

        print("\n--- Lista de Profissionais de Saúde ---")
        for prof in self.__profissionais:
            dados = {
                "nome": prof.nome,
                "cpf": prof.cpf,
                "celular": prof.celular,
                "especialidade": prof.especialidade,
                "registro_profissional": prof.registro_profissional,
                "clinica": prof.clinica,
            }
            self.__tela_profissional.mostra_profissional(dados)

        return self.__profissionais

    # Fluxos de interação com a tela
    def __incluir_profissional_fluxo(self) -> None:
        dados = self.__tela_profissional.coletar_dados()
        if not dados["nome"] or not dados["cpf"] or not dados["registro"]:
            self.__tela_profissional.mostra_mensagem("Erro: Nome, CPF e Registro Profissional são obrigatórios.")
            return
        self.cadastrar_profissional(
            nome=dados["nome"],
            celular=dados["celular"],
            cpf=dados["cpf"],
            especialidade=dados["especialidade"],
            registro=dados["registro"],
            clinica=None,
        )

    def __excluir_profissional_fluxo(self) -> None:
        cpf = self.__tela_profissional.buscar_por_cpf()
        self.excluir_profissional(cpf)

    def __atualizar_profissional_fluxo(self) -> None:
        cpf = self.__tela_profissional.buscar_por_cpf()
        profissional = self.buscar_profissional_por_cpf(cpf)
        if profissional is not None:
            self.__tela_profissional.mostra_profissional({
                "nome": profissional.nome,
                "cpf": profissional.cpf,
                "celular": profissional.celular,
                "especialidade": profissional.especialidade,
                "registro_profissional": profissional.registro_profissional,
                "clinica": profissional.clinica,
            })
            novos_dados = self.__tela_profissional.coletar_novos_dados()
            self.atualizar_profissional(cpf, novos_dados)
        else:
            self.__tela_profissional.mostra_mensagem("Erro: Não foi encontrado profissional com o CPF informado.")

    def __buscar_profissional_fluxo(self) -> None:
        registro = self.__tela_profissional.buscar_profissional()
        profissional = self.buscar_profissional(registro)
        if profissional is not None:
            self.__tela_profissional.mostra_profissional({
                "nome": profissional.nome,
                "cpf": profissional.cpf,
                "celular": profissional.celular,
                "especialidade": profissional.especialidade,
                "registro_profissional": profissional.registro_profissional,
                "clinica": profissional.clinica,
            })
        else:
            self.__tela_profissional.mostra_mensagem("Profissional com o Registro informado não foi encontrado.")

    def abre_tela(self) -> None:
        opcoes = {
            1: self.__incluir_profissional_fluxo,
            2: self.__excluir_profissional_fluxo,
            3: self.__atualizar_profissional_fluxo,
            4: self.listar_profissionais,
            5: self.__buscar_profissional_fluxo,
            0: self.retornar,
        }

        while True:
            opcao_escolhida = self.__tela_profissional.opcoes_tela()
            funcao_escolhida = opcoes.get(opcao_escolhida)
            if funcao_escolhida:
                funcao_escolhida()
            if opcao_escolhida == 0:
                break
