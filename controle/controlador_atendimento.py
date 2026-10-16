from datetime import date, time
from typing import Optional

from entidade.atendimento import Atendimento
from entidade.pagamento_dinheiro import PagamentoDinheiro
from entidade.pagamento_pix import PagamentoPix
from entidade.pagamento_cartao import PagamentoCartao
from limite.tela_atendimento import TelaAtendimento

from excecoes.atendimento_nao_encontrado_exception import AtendimentoNaoEncontradoException
from excecoes.clinica_nao_encontrada_exception import ClinicaNaoEncontradaException
from excecoes.paciente_nao_encontrado import PacienteNaoEncontradoException
from excecoes.profissional_nao_encontrado_exception import ProfissionalNaoEncontradoException
from excecoes.tipo_atendimento_nao_encontrado_exception import TipoAtendimentoNaoEncontradoException
from excecoes.procedimento_nao_encontrado_exception import ProcedimentoNaoEncontradoException
from excecoes.paciente_menor_idade_exception import PacienteMenorIdadeException
from excecoes.horario_fora_funcionamento_exception import HorarioForaFuncionamentoException
from excecoes.pagamento_invalido_exception import PagamentoInvalidoException
from excecoes.dado_invalido_exception import DadoInvalidoException


class ControladorAtendimento:
    def __init__(
        self,
        controlador_clinica=None,
        controlador_paciente=None,
        controlador_profissionais=None,
        controlador_tipo_atendimento=None,
        controlador_procedimento=None,
    ):
        self.__controlador_clinica = controlador_clinica
        self.__controlador_paciente = controlador_paciente
        self.__controlador_profissionais = controlador_profissionais
        self.__controlador_tipo_atendimento = controlador_tipo_atendimento
        self.__controlador_procedimento = controlador_procedimento

        self.__atendimentos: list[Atendimento] = []
        self.__tela_atendimento = TelaAtendimento()
        self.__contador_id = 1

    @property
    def atendimentos(self) -> list[Atendimento]:
        return self.__atendimentos

    @property
    def tela_atendimento(self) -> TelaAtendimento:
        return self.__tela_atendimento

    def retornar(self) -> None:
        pass

    def buscar_atendimento_por_id(self, id_atendimento: int) -> Optional[Atendimento]:
        for atend in self.__atendimentos:
            if atend.id_atendimento == id_atendimento:
                return atend
        return None

    def buscar_atendimento(self, id_atendimento: Optional[int] = None) -> Optional[Atendimento]:
        if id_atendimento is None:
            id_atendimento = self.__tela_atendimento.buscar_atendimento()
        return self.buscar_atendimento_por_id(id_atendimento)

    def agendar_atendimento(
        self,
        nome_clinica: str,
        cpf_paciente: str,
        registro_profissional: str,
        nome_tipo: str,
        data_atendimento: date,
        horario_inicio: time,
        horario_fim: time,
        valor_total: float,
        menor_acompanhado: bool = False,
    ) -> Atendimento:
        clinica = None
        if self.__controlador_clinica is not None:
            clinica = self.__controlador_clinica.buscar_clinica(nome_clinica)
        if clinica is None:
            raise ClinicaNaoEncontradaException(nome_clinica)

        paciente = None
        if self.__controlador_paciente is not None:
            paciente = self.__controlador_paciente.buscar_paciente_por_cpf(cpf_paciente)
        if paciente is None:
            raise PacienteNaoEncontradoException(cpf_paciente)

        profissional = None
        if self.__controlador_profissionais is not None:
            profissional = self.__controlador_profissionais.buscar_profissional(registro_profissional)
        if profissional is None:
            raise ProfissionalNaoEncontradoException(registro_profissional)

        tipo = None
        if self.__controlador_tipo_atendimento is not None:
            tipo = self.__controlador_tipo_atendimento.buscar_tipo_atendimento(nome_tipo)
        if tipo is None:
            raise TipoAtendimentoNaoEncontradoException(nome_tipo)

        novo_atendimento = Atendimento(
            clinica=clinica,
            paciente=paciente,
            profissional=profissional,
            data=data_atendimento,
            horario_inicio=horario_inicio,
            horario_fim=horario_fim,
            tipo_atendimento=tipo,
            valor_total=valor_total,
            menor_acompanhado=menor_acompanhado,
            id_atendimento=self.__contador_id,
        )
        self.__contador_id += 1
        self.__atendimentos.append(novo_atendimento)
        self.__tela_atendimento.mostra_mensagem(
            f"Atendimento #{novo_atendimento.id_atendimento} agendado com sucesso para {data_atendimento.strftime('%d/%m/%Y')}!"
        )
        return novo_atendimento

    def excluir_atendimento(self, id_atendimento: int) -> None:
        atendimento = self.buscar_atendimento_por_id(id_atendimento)
        if atendimento is None:
            raise AtendimentoNaoEncontradoException(id_atendimento)

        if hasattr(atendimento.clinica, "remover_atendimento"):
            atendimento.clinica.remover_atendimento(atendimento)

        self.__atendimentos.remove(atendimento)
        self.__tela_atendimento.mostra_mensagem(f"Atendimento #{id_atendimento} cancelado/excluído com sucesso!")

    def alterar_atendimento(self, id_atendimento: int, novos_dados: dict) -> None:
        atendimento = self.buscar_atendimento_por_id(id_atendimento)
        if atendimento is None:
            raise AtendimentoNaoEncontradoException(id_atendimento)

        if "data" in novos_dados and novos_dados["data"]:
            atendimento.data = novos_dados["data"]

        novo_inicio = novos_dados.get("horario_inicio")
        novo_fim = novos_dados.get("horario_fim")
        if novo_inicio is not None and novo_fim is not None:
            atendimento.horario_inicio = novo_inicio
            atendimento.horario_fim = novo_fim

        if "valor_total" in novos_dados and novos_dados["valor_total"] is not None:
            atendimento.valor_total = novos_dados["valor_total"]

        self.__tela_atendimento.mostra_mensagem(f"Atendimento #{id_atendimento} atualizado com sucesso!")

    def listar_atendimentos(self) -> list[Atendimento]:
        return self.__atendimentos

    def registra_procedimento(self, id_atendimento: int, nome_procedimento: str) -> None:
        atendimento = self.buscar_atendimento_por_id(id_atendimento)
        if atendimento is None:
            raise AtendimentoNaoEncontradoException(id_atendimento)

        procedimento = None
        if self.__controlador_procedimento is not None:
            procedimento = self.__controlador_procedimento.buscar_procedimento(nome_procedimento)
        if procedimento is None:
            raise ProcedimentoNaoEncontradoException(nome_procedimento)

        atendimento.adicionar_procedimento(procedimento)
        self.__tela_atendimento.mostra_mensagem(
            f"Procedimento '{procedimento.nome}' (R$ {procedimento.custo:.2f}) registrado com sucesso no Atendimento #{id_atendimento}!"
        )

    def registrar_procedimento(self, id_atendimento: int, nome_procedimento: str) -> None:
        self.registra_procedimento(id_atendimento, nome_procedimento)

    def realizar_pagamento(
        self,
        id_atendimento: int,
        forma_pagamento: int,
        dados_pagamento: dict,
    ) -> None:
        atendimento = self.buscar_atendimento_por_id(id_atendimento)
        if atendimento is None:
            raise AtendimentoNaoEncontradoException(id_atendimento)

        paciente = atendimento.paciente
        valor_pago = dados_pagamento["valor_pago"]
        data_pagamento = dados_pagamento["data_pagamento"]

        if forma_pagamento == 1:  # Dinheiro
            pagamento = PagamentoDinheiro(
                paciente=paciente,
                data_pagamento=data_pagamento,
                valor_pago=valor_pago,
            )
        elif forma_pagamento == 2:  # PIX
            cpf_pagador = dados_pagamento.get("cpf_pagador") or paciente.cpf
            pagamento = PagamentoPix(
                paciente=paciente,
                data_pagamento=data_pagamento,
                valor_pago=valor_pago,
                cpf_pagador=cpf_pagador,
            )
        elif forma_pagamento == 3:  # Cartão
            numero_cartao = dados_pagamento.get("numero_cartao", "")
            bandeira = dados_pagamento.get("bandeira", "")
            pagamento = PagamentoCartao(
                paciente=paciente,
                data_pagamento=data_pagamento,
                valor_pago=valor_pago,
                numero_cartao=numero_cartao,
                bandeira=bandeira,
            )
        else:
            raise PagamentoInvalidoException("Modalidade de pagamento inválida.")

        atendimento.adicionar_pagamento(pagamento)
        self.__tela_atendimento.mostra_mensagem(
            f"Pagamento de R$ {valor_pago:.2f} registrado com sucesso! Saldo restante: R$ {atendimento.calcular_valor_a_pagar():.2f}."
        )

    def __montar_dados_atendimento_tela(self, atend: Atendimento) -> dict:
        procs = []
        for p in atend.procedimentos:
            procs.append({
                "nome": p.nome,
                "custo": p.custo,
                "responsavel": p.profissional_responsavel.nome if hasattr(p, "profissional_responsavel") and p.profissional_responsavel else "Não informado",
            })

        pags = []
        for pg in atend.pagamentos:
            tipo_nome = pg.__class__.__name__.replace("Pagamento", "")
            detalhe = ""
            if isinstance(pg, PagamentoPix):
                detalhe = f"CPF Pagador: {pg.cpf_pagador}"
            elif isinstance(pg, PagamentoCartao):
                detalhe = f"Cartão final {pg.numero_cartao[-4:] if len(pg.numero_cartao) >= 4 else pg.numero_cartao} ({pg.bandeira})"
            elif isinstance(pg, PagamentoDinheiro):
                detalhe = "Espécie"

            pags.append({
                "tipo": tipo_nome,
                "valor": pg.valor_pago,
                "data": pg.data_pagamento.strftime("%d/%m/%Y"),
                "detalhes": detalhe,
            })

        return {
            "id_atendimento": atend.id_atendimento,
            "clinica": atend.clinica.nome if hasattr(atend.clinica, "nome") else str(atend.clinica),
            "paciente": atend.paciente.nome if hasattr(atend.paciente, "nome") else str(atend.paciente),
            "cpf_paciente": atend.paciente.cpf if hasattr(atend.paciente, "cpf") else "",
            "profissional": atend.profissional.nome if hasattr(atend.profissional, "nome") else str(atend.profissional),
            "registro_profissional": atend.profissional.registro_profissional if hasattr(atend.profissional, "registro_profissional") else "",
            "tipo_atendimento": atend.tipo_atendimento.nome_tipo if hasattr(atend.tipo_atendimento, "nome_tipo") else str(atend.tipo_atendimento),
            "data": atend.data.strftime("%d/%m/%Y"),
            "horario_inicio": atend.horario_inicio.strftime("%H:%M"),
            "horario_fim": atend.horario_fim.strftime("%H:%M"),
            "valor_base": atend.valor_total,
            "custo_procedimentos": atend.calcular_custo_procedimentos(),
            "valor_total_geral": atend.calcular_valor_total_com_procedimentos(),
            "total_pago": atend.calcular_valor_pago(),
            "saldo_restante": atend.calcular_valor_a_pagar(),
            "procedimentos": procs,
            "pagamentos": pags,
        }

    # Fluxos de tela
    def __agendar_atendimento_fluxo(self) -> None:
        try:
            dados = self.__tela_atendimento.coletar_dados()

            # Verificação prévia da idade para questionar acompanhante se menor de idade
            menor_acompanhado = False
            if self.__controlador_paciente is not None:
                paciente = self.__controlador_paciente.buscar_paciente_por_cpf(dados["cpf_paciente"])
                if paciente is not None and hasattr(paciente, "calcular_idade"):
                    idade = paciente.calcular_idade(dados["data"])
                    if idade < 18:
                        menor_acompanhado = self.__tela_atendimento.perguntar_se_menor_esta_acompanhado()

            self.agendar_atendimento(
                nome_clinica=dados["nome_clinica"],
                cpf_paciente=dados["cpf_paciente"],
                registro_profissional=dados["registro_profissional"],
                nome_tipo=dados["nome_tipo"],
                data_atendimento=dados["data"],
                horario_inicio=dados["horario_inicio"],
                horario_fim=dados["horario_fim"],
                valor_total=dados["valor_total"],
                menor_acompanhado=menor_acompanhado,
            )
        except (
            ClinicaNaoEncontradaException,
            PacienteNaoEncontradoException,
            ProfissionalNaoEncontradoException,
            TipoAtendimentoNaoEncontradoException,
            PacienteMenorIdadeException,
            HorarioForaFuncionamentoException,
            DadoInvalidoException,
        ) as e:
            self.__tela_atendimento.mostra_mensagem(f"Erro ao agendar atendimento: {e}")

    def __excluir_atendimento_fluxo(self) -> None:
        try:
            id_atend = self.__tela_atendimento.buscar_atendimento()
            self.excluir_atendimento(id_atend)
        except AtendimentoNaoEncontradoException as e:
            self.__tela_atendimento.mostra_mensagem(f"Erro ao excluir atendimento: {e}")

    def __alterar_atendimento_fluxo(self) -> None:
        try:
            id_atend = self.__tela_atendimento.buscar_atendimento()
            atend = self.buscar_atendimento_por_id(id_atend)
            if atend is None:
                raise AtendimentoNaoEncontradoException(id_atend)

            self.__tela_atendimento.mostra_atendimento(self.__montar_dados_atendimento_tela(atend))
            novos_dados = self.__tela_atendimento.coletar_novos_dados()
            if novos_dados:
                self.alterar_atendimento(id_atend, novos_dados)
        except (AtendimentoNaoEncontradoException, HorarioForaFuncionamentoException, DadoInvalidoException) as e:
            self.__tela_atendimento.mostra_mensagem(f"Erro ao alterar atendimento: {e}")

    def __listar_atendimentos_fluxo(self) -> None:
        if not self.__atendimentos:
            self.__tela_atendimento.mostra_mensagem("Nenhum atendimento cadastrado no sistema.")
            return

        print("\n--- Lista de Atendimentos Cadastrados ---")
        for atend in self.__atendimentos:
            self.__tela_atendimento.mostra_atendimento(self.__montar_dados_atendimento_tela(atend))

    def __buscar_atendimento_fluxo(self) -> None:
        id_atend = self.__tela_atendimento.buscar_atendimento()
        atend = self.buscar_atendimento_por_id(id_atend)
        if atend is not None:
            self.__tela_atendimento.mostra_atendimento(self.__montar_dados_atendimento_tela(atend))
        else:
            self.__tela_atendimento.mostra_mensagem(f"Atendimento com código #{id_atend} não foi encontrado.")

    def __registrar_procedimento_fluxo(self) -> None:
        try:
            id_atend = self.__tela_atendimento.buscar_atendimento()
            atend = self.buscar_atendimento_por_id(id_atend)
            if atend is None:
                raise AtendimentoNaoEncontradoException(id_atend)

            self.__tela_atendimento.mostra_atendimento(self.__montar_dados_atendimento_tela(atend))
            nome_proc = self.__tela_atendimento.coletar_nome_procedimento()
            self.registra_procedimento(id_atend, nome_proc)
        except (AtendimentoNaoEncontradoException, ProcedimentoNaoEncontradoException, DadoInvalidoException) as e:
            self.__tela_atendimento.mostra_mensagem(f"Erro ao registrar procedimento: {e}")

    def __realizar_pagamento_fluxo(self) -> None:
        try:
            id_atend = self.__tela_atendimento.buscar_atendimento()
            atend = self.buscar_atendimento_por_id(id_atend)
            if atend is None:
                raise AtendimentoNaoEncontradoException(id_atend)

            saldo_restante = atend.calcular_valor_a_pagar()
            if saldo_restante <= 0:
                self.__tela_atendimento.mostra_mensagem(f"Atendimento #{id_atend} já está integralmente quitado!")
                return

            self.__tela_atendimento.mostra_atendimento(self.__montar_dados_atendimento_tela(atend))
            forma = self.__tela_atendimento.perguntar_forma_pagamento()
            if forma == 0:
                return

            dados_pag = self.__tela_atendimento.coletar_dados_pagamento(
                forma_pagamento=forma,
                valor_restante=saldo_restante,
                data_atendimento=atend.data,
            )
            self.realizar_pagamento(id_atend, forma, dados_pag)
        except (AtendimentoNaoEncontradoException, PagamentoInvalidoException, DadoInvalidoException) as e:
            self.__tela_atendimento.mostra_mensagem(f"Erro ao processar pagamento: {e}")

    def abre_tela(self) -> None:
        opcoes = {
            1: self.__agendar_atendimento_fluxo,
            2: self.__excluir_atendimento_fluxo,
            3: self.__alterar_atendimento_fluxo,
            4: self.__listar_atendimentos_fluxo,
            5: self.__buscar_atendimento_fluxo,
            6: self.__registrar_procedimento_fluxo,
            7: self.__realizar_pagamento_fluxo,
            0: self.retornar,
        }

        while True:
            opcao_escolhida = self.__tela_atendimento.opcoes_tela()
            funcao_escolhida = opcoes.get(opcao_escolhida)
            if funcao_escolhida:
                funcao_escolhida()
            if opcao_escolhida == 0:
                break
