from datetime import time
from typing import Optional
from entidade.clinica import Clinica
from limite.tela_clinica import TelaClinica
from excecoes.clinica_ja_cadastrada_exception import ClinicaJaCadastradaException
from excecoes.clinica_nao_encontrada_exception import ClinicaNaoEncontradaException
from excecoes.horario_invalido_exception import HorarioInvalidoException
from excecoes.dado_invalido_exception import DadoInvalidoException


class ControladorClinica:
    def __init__(self, controlador_sistema=None):
        self.__controlador_sistema = controlador_sistema
        self.__clinicas: list[Clinica] = []
        self.__tela_clinica = TelaClinica()

    @property
    def controlador_sistema(self):
        return self.__controlador_sistema

    @property
    def clinicas(self) -> list[Clinica]:
        return self.__clinicas

    @property
    def tela_clinica(self) -> TelaClinica:
        return self.__tela_clinica

    def retornar(self) -> None:
        pass

    def buscar_clinica(self, nome: Optional[str] = None) -> Optional[Clinica]:
        """
        Busca clínica por nome. Se o nome não for fornecido, solicita através da tela,
        mantendo compatibilidade com a assinatura sem parâmetros do diagrama UML.
        """
        if nome is None:
            nome = self.__tela_clinica.buscar_clinica()

        if not nome:
            return None

        for clinica in self.__clinicas:
            if clinica.nome.strip().lower() == nome.strip().lower():
                return clinica
        return None

    def cadastrar_clinica(
        self,
        nome: str,
        cidade: str,
        descricao: str,
        hora_abertura: time,
        hora_fechamento: time,
    ) -> Clinica:
        if self.buscar_clinica(nome) is not None:
            raise ClinicaJaCadastradaException(nome)

        nova_clinica = Clinica(
            nome=nome,
            cidade=cidade,
            descricao=descricao,
            hora_abertura=hora_abertura,
            hora_fechamento=hora_fechamento,
        )
        self.__clinicas.append(nova_clinica)
        self.__tela_clinica.mostrar_mensagem("Clínica cadastrada com sucesso!")
        return nova_clinica

    def excluir_clinica(self, nome: Optional[str] = None) -> None:
        """
        Exclui uma clínica cadastrada. Aceita nome como parâmetro ou solicita via tela,
        respeitando a assinatura do diagrama e garantindo flexibilidade.
        """
        if nome is None:
            nome = self.__tela_clinica.buscar_clinica()

        clinica = self.buscar_clinica(nome)
        if clinica is None:
            raise ClinicaNaoEncontradaException(nome)

        # Desvincula profissionais associados a esta clínica
        for profissional in list(clinica.profissionais):
            clinica.remover_profissional(profissional)

        self.__clinicas.remove(clinica)
        self.__tela_clinica.mostrar_mensagem(f"Clínica '{clinica.nome}' excluída com sucesso!")

    def alterar_clinica(self, nome: str, novos_dados: dict) -> None:
        clinica = self.buscar_clinica(nome)
        if clinica is None:
            raise ClinicaNaoEncontradaException(nome)

        novo_nome = novos_dados.get("nome")
        if novo_nome and novo_nome.strip().lower() != clinica.nome.strip().lower():
            if self.buscar_clinica(novo_nome) is not None:
                raise ClinicaJaCadastradaException(novo_nome)
            clinica.nome = novo_nome

        if "cidade" in novos_dados and novos_dados["cidade"]:
            clinica.cidade = novos_dados["cidade"]

        if "descricao" in novos_dados and novos_dados["descricao"] is not None:
            clinica.descricao = novos_dados["descricao"]

        nova_abertura = novos_dados.get("hora_abertura")
        novo_fechamento = novos_dados.get("hora_fechamento")

        # Se ambos os horários foram alterados juntos
        if nova_abertura is not None and novo_fechamento is not None:
            if nova_abertura >= novo_fechamento:
                raise HorarioInvalidoException("A nova hora de abertura deve ser anterior ao novo fechamento.")
            # Atribui temporariamente ou valida
            clinica.hora_fechamento = time(23, 59, 59)
            clinica.hora_abertura = nova_abertura
            clinica.hora_fechamento = novo_fechamento
        elif nova_abertura is not None:
            clinica.hora_abertura = nova_abertura
        elif novo_fechamento is not None:
            clinica.hora_fechamento = novo_fechamento

        self.__tela_clinica.mostrar_mensagem("Clínica atualizada com sucesso!")

    def listar_clinica(self) -> list[Clinica]:
        """
        Lista todas as clínicas cadastradas.
        Mantém o nome do diagrama (listar_clinica) e provê o plural como alias.
        """
        if not self.__clinicas:
            self.__tela_clinica.mostrar_mensagem("Nenhuma clínica cadastrada no sistema.")
            return self.__clinicas

        self.__tela_clinica.mostra_cabecalho_lista()
        for clinica in self.__clinicas:
            dados = {
                "nome": clinica.nome,
                "cidade": clinica.cidade,
                "descricao": clinica.descricao,
                "hora_abertura": clinica.hora_abertura,
                "hora_fechamento": clinica.hora_fechamento,
                "profissionais": clinica.profissionais,
                "atendimentos": clinica.atendimentos,
            }
            self.__tela_clinica.mostra_clinica(dados)

        return self.__clinicas

    def listar_clinicas(self) -> list[Clinica]:
        return self.listar_clinica()

    # Fluxos de tela (interações com o usuário)
    def __incluir_clinica_fluxo(self) -> None:
        try:
            dados = self.__tela_clinica.coletar_dados()
            self.cadastrar_clinica(
                nome=dados["nome"],
                cidade=dados["cidade"],
                descricao=dados["descricao"],
                hora_abertura=dados["hora_abertura"],
                hora_fechamento=dados["hora_fechamento"],
            )
        except (ClinicaJaCadastradaException, HorarioInvalidoException, DadoInvalidoException) as e:
            self.__tela_clinica.mostrar_mensagem(f"Erro ao cadastrar clínica: {e}")

    def __excluir_clinica_fluxo(self) -> None:
        try:
            nome = self.__tela_clinica.buscar_clinica()
            self.excluir_clinica(nome)
        except ClinicaNaoEncontradaException as e:
            self.__tela_clinica.mostrar_mensagem(f"Erro ao excluir clínica: {e}")

    def __alterar_clinica_fluxo(self) -> None:
        try:
            nome = self.__tela_clinica.buscar_clinica()
            clinica = self.buscar_clinica(nome)
            if clinica is None:
                raise ClinicaNaoEncontradaException(nome)

            self.__tela_clinica.mostra_clinica({
                "nome": clinica.nome,
                "cidade": clinica.cidade,
                "descricao": clinica.descricao,
                "hora_abertura": clinica.hora_abertura,
                "hora_fechamento": clinica.hora_fechamento,
                "profissionais": clinica.profissionais,
                "atendimentos": clinica.atendimentos,
            })
            novos_dados = self.__tela_clinica.coletar_novos_dados()
            self.alterar_clinica(nome, novos_dados)
        except (ClinicaNaoEncontradaException, ClinicaJaCadastradaException, HorarioInvalidoException, DadoInvalidoException) as e:
            self.__tela_clinica.mostrar_mensagem(f"Erro ao alterar clínica: {e}")

    def __buscar_clinica_fluxo(self) -> None:
        nome = self.__tela_clinica.buscar_clinica()
        clinica = self.buscar_clinica(nome)
        if clinica is not None:
            self.__tela_clinica.mostra_clinica({
                "nome": clinica.nome,
                "cidade": clinica.cidade,
                "descricao": clinica.descricao,
                "hora_abertura": clinica.hora_abertura,
                "hora_fechamento": clinica.hora_fechamento,
                "profissionais": clinica.profissionais,
                "atendimentos": clinica.atendimentos,
            })
        else:
            self.__tela_clinica.mostrar_mensagem(f"Clínica '{nome}' não encontrada.")

    def abre_tela(self) -> None:
        opcoes = {
            1: self.__incluir_clinica_fluxo,
            2: self.__excluir_clinica_fluxo,
            3: self.__alterar_clinica_fluxo,
            4: self.listar_clinica,
            5: self.__buscar_clinica_fluxo,
            0: self.retornar,
        }

        while True:
            opcao_escolhida = self.__tela_clinica.opcoes_tela()
            funcao_escolhida = opcoes.get(opcao_escolhida)
            if funcao_escolhida:
                funcao_escolhida()
            if opcao_escolhida == 0:
                break
