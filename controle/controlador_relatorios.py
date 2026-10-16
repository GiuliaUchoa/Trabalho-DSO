from limite.tela_relatorios import TelaRelatorios


class ControladorRelatorios:
    def __init__(
        self,
        controlador_clinica=None,
        controlador_atendimento=None,
        controlador_procedimento=None,
    ):
        self.__controlador_clinica = controlador_clinica
        self.__controlador_atendimento = controlador_atendimento
        self.__controlador_procedimento = controlador_procedimento
        self.__tela_relatorios = TelaRelatorios()

    @property
    def controlador_clinica(self):
        return self.__controlador_clinica

    @property
    def controlador_atendimento(self):
        return self.__controlador_atendimento

    @property
    def controlador_procedimento(self):
        return self.__controlador_procedimento

    @property
    def tela_relatorios(self) -> TelaRelatorios:
        return self.__tela_relatorios

    def retornar(self) -> None:
        pass

    def clinicas_maior_num_atendimentos(self) -> list[dict]:
        """
        Relatório 1: Clínicas com maior número de atendimentos.
        Ordena as clínicas cadastradas pelo total de atendimentos registrados (ordem decrescente).
        """
        contagem: dict[str, dict] = {}

        # 1. Carrega todas as clínicas cadastradas com 0 atendimentos inicialmente
        if self.__controlador_clinica is not None:
            for clinica in self.__controlador_clinica.clinicas:
                contagem[clinica.nome] = {
                    "nome": clinica.nome,
                    "cidade": clinica.cidade,
                    "total_atendimentos": 0,
                    "faturamento_total": 0.0,
                }

        # 2. Computa a contagem de atendimentos registrados
        if self.__controlador_atendimento is not None:
            for atend in self.__controlador_atendimento.atendimentos:
                cli = atend.clinica
                cli_nome = cli.nome if hasattr(cli, "nome") else str(cli)
                cli_cidade = cli.cidade if hasattr(cli, "cidade") else ""

                if cli_nome not in contagem:
                    contagem[cli_nome] = {
                        "nome": cli_nome,
                        "cidade": cli_cidade,
                        "total_atendimentos": 0,
                        "faturamento_total": 0.0,
                    }

                contagem[cli_nome]["total_atendimentos"] += 1
                contagem[cli_nome]["faturamento_total"] += atend.calcular_valor_total_com_procedimentos()

        # 3. Converte para lista e ordena decrescente pelo número de atendimentos
        resultado = list(contagem.values())
        resultado.sort(key=lambda item: (-item["total_atendimentos"], -item["faturamento_total"], item["nome"]))

        self.__tela_relatorios.mostra_relatorio_clinicas(resultado)
        return resultado

    def atendimentos_mais_caros_e_baratos(self) -> dict:
        """
        Relatório 2: Atendimentos mais caros e mais baratos.
        Ordena os atendimentos registrados por valor total (base + procedimentos),
        apresentando os extremos e a listagem ordenada.
        """
        atendimentos = []
        if self.__controlador_atendimento is not None:
            atendimentos = self.__controlador_atendimento.atendimentos

        if not atendimentos:
            resultado = {
                "mais_caros": [],
                "mais_baratos": [],
                "destaque_mais_caro": None,
                "destaque_mais_barato": None,
                "total_atendimentos": 0,
                "valor_medio": 0.0,
                "valor_total_acumulado": 0.0,
            }
            self.__tela_relatorios.mostra_relatorio_atendimentos(resultado)
            return resultado

        dados_formatados = []
        for atend in atendimentos:
            valor_total = atend.calcular_valor_total_com_procedimentos()
            pac_nome = atend.paciente.nome if hasattr(atend.paciente, "nome") else str(atend.paciente)
            prof_nome = atend.profissional.nome if hasattr(atend.profissional, "nome") else str(atend.profissional)
            cli_nome = atend.clinica.nome if hasattr(atend.clinica, "nome") else str(atend.clinica)
            tipo_obj = atend.tipo_atendimento
            if hasattr(tipo_obj, "nome_tipo"):
                tipo_nome = tipo_obj.nome_tipo
            elif hasattr(tipo_obj, "nome"):
                tipo_nome = tipo_obj.nome
            else:
                tipo_nome = str(tipo_obj)
            data_str = atend.data.strftime("%d/%m/%Y") if hasattr(atend.data, "strftime") else str(atend.data)

            dados_formatados.append({
                "id": atend.id_atendimento,
                "data": data_str,
                "paciente": pac_nome,
                "profissional": prof_nome,
                "clinica": cli_nome,
                "tipo": tipo_nome,
                "valor_base": atend.valor_total,
                "custo_procedimentos": atend.calcular_custo_procedimentos(),
                "valor_total": valor_total,
                "valor_pago": atend.calcular_valor_pago(),
                "saldo_restante": atend.calcular_valor_a_pagar(),
            })

        # Ordenações
        mais_caros = sorted(dados_formatados, key=lambda x: -x["valor_total"])
        mais_baratos = sorted(dados_formatados, key=lambda x: x["valor_total"])

        total_acumulado = sum(item["valor_total"] for item in dados_formatados)
        valor_medio = total_acumulado / len(dados_formatados) if dados_formatados else 0.0

        resultado = {
            "mais_caros": mais_caros,
            "mais_baratos": mais_baratos,
            "destaque_mais_caro": mais_caros[0] if mais_caros else None,
            "destaque_mais_barato": mais_baratos[0] if mais_baratos else None,
            "total_atendimentos": len(dados_formatados),
            "valor_medio": valor_medio,
            "valor_total_acumulado": total_acumulado,
        }

        self.__tela_relatorios.mostra_relatorio_atendimentos(resultado)
        return resultado

    def procedimentos_mais_realizados(self) -> list[dict]:
        """
        Relatório 3: Procedimentos mais realizados (mais populares).
        Conta a ocorrência de cada procedimento em todos os atendimentos cadastrados
        e ordena do mais executado para o menos executado.
        """
        contagem: dict[str, dict] = {}

        # 1. Inicializa com todos os procedimentos conhecidos do controlador_procedimento
        if self.__controlador_procedimento is not None:
            for proc in self.__controlador_procedimento.procedimentos:
                prof_nome = proc.profissional_responsavel.nome if hasattr(proc.profissional_responsavel, "nome") else ""
                contagem[proc.nome] = {
                    "nome": proc.nome,
                    "descricao": proc.descricao,
                    "custo": proc.custo,
                    "profissional": prof_nome,
                    "quantidade_realizada": 0,
                    "valor_total_gerado": 0.0,
                }

        # 2. Contabiliza execuções nos atendimentos registrados
        if self.__controlador_atendimento is not None:
            for atend in self.__controlador_atendimento.atendimentos:
                for proc in atend.procedimentos:
                    proc_nome = proc.nome if hasattr(proc, "nome") else str(proc)
                    proc_custo = proc.custo if hasattr(proc, "custo") else 0.0
                    proc_desc = proc.descricao if hasattr(proc, "descricao") else ""
                    prof_nome = ""
                    if hasattr(proc, "profissional_responsavel") and proc.profissional_responsavel is not None:
                        prof_nome = getattr(proc.profissional_responsavel, "nome", "")

                    if proc_nome not in contagem:
                        contagem[proc_nome] = {
                            "nome": proc_nome,
                            "descricao": proc_desc,
                            "custo": proc_custo,
                            "profissional": prof_nome,
                            "quantidade_realizada": 0,
                            "valor_total_gerado": 0.0,
                        }

                    contagem[proc_nome]["quantidade_realizada"] += 1
                    contagem[proc_nome]["valor_total_gerado"] += proc_custo

        resultado = list(contagem.values())
        resultado.sort(key=lambda item: (-item["quantidade_realizada"], -item["valor_total_gerado"], item["nome"]))

        self.__tela_relatorios.mostra_relatorio_procedimentos_populares(resultado)
        return resultado

    def procedimentos_mais_caros_e_baratos(self) -> dict:
        """
        Relatório 4: Procedimentos mais caros e mais baratos.
        Ordena os procedimentos cadastrados pelo atributo custo, apresentando
        os extremos e listagem decrescente.
        """
        procedimentos = []
        if self.__controlador_procedimento is not None:
            procedimentos = self.__controlador_procedimento.procedimentos

        if not procedimentos:
            resultado = {
                "mais_caros": [],
                "mais_baratos": [],
                "destaque_mais_caro": None,
                "destaque_mais_barato": None,
                "total_procedimentos": 0,
                "custo_medio": 0.0,
            }
            self.__tela_relatorios.mostra_relatorio_procedimentos_valores(resultado)
            return resultado

        dados_formatados = []
        for proc in procedimentos:
            prof_nome = proc.profissional_responsavel.nome if hasattr(proc.profissional_responsavel, "nome") else ""
            dados_formatados.append({
                "nome": proc.nome,
                "descricao": proc.descricao,
                "custo": proc.custo,
                "profissional": prof_nome,
            })

        mais_caros = sorted(dados_formatados, key=lambda x: -x["custo"])
        mais_baratos = sorted(dados_formatados, key=lambda x: x["custo"])

        total_custo = sum(item["custo"] for item in dados_formatados)
        custo_medio = total_custo / len(dados_formatados) if dados_formatados else 0.0

        resultado = {
            "mais_caros": mais_caros,
            "mais_baratos": mais_baratos,
            "destaque_mais_caro": mais_caros[0] if mais_caros else None,
            "destaque_mais_barato": mais_baratos[0] if mais_baratos else None,
            "total_procedimentos": len(dados_formatados),
            "custo_medio": custo_medio,
        }

        self.__tela_relatorios.mostra_relatorio_procedimentos_valores(resultado)
        return resultado

    def abre_tela(self) -> None:
        opcoes = {
            1: self.clinicas_maior_num_atendimentos,
            2: self.atendimentos_mais_caros_e_baratos,
            3: self.procedimentos_mais_realizados,
            4: self.procedimentos_mais_caros_e_baratos,
            0: self.retornar,
        }

        while True:
            opcao_escolhida = self.__tela_relatorios.opcoes_tela()
            funcao_escolhida = opcoes.get(opcao_escolhida)
            if funcao_escolhida:
                funcao_escolhida()
            if opcao_escolhida == 0:
                break
