class TelaRelatorios:
    def opcoes_tela(self) -> int:
        print("\n" + "=" * 45)
        print("           RELATÓRIOS DO SISTEMA")
        print("=" * 45)
        print("1 - Clínicas com maior número de atendimentos")
        print("2 - Atendimentos mais caros e mais baratos")
        print("3 - Procedimentos mais realizados (populares)")
        print("4 - Procedimentos mais caros e mais baratos")
        print("0 - Retornar")
        print("=" * 45)
        return self.le_numero_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4])

    def tela_opcoes(self) -> int:
        return self.opcoes_tela()

    def mostra_mensagem(self, mensagem: str) -> None:
        print(f"\n{mensagem}")

    def mostrar_mensagem(self, mensagem: str) -> None:
        self.mostra_mensagem(mensagem)

    def le_numero_inteiro(self, mensagem: str = "Escolha a opção: ", intervalo_valido: list[int] = None) -> int:
        while True:
            try:
                valor = int(input(mensagem))
                if intervalo_valido is not None and valor not in intervalo_valido:
                    print(f"Opção inválida! Escolha entre {intervalo_valido}.")
                    continue
                return valor
            except ValueError:
                print("Valor inválido! Digite apenas números inteiros.")

    def mostra_relatorio_clinicas(self, dados: list[dict]) -> None:
        print("\n" + "=" * 65)
        print("       RELATÓRIO: CLÍNICAS COM MAIOR NÚMERO DE ATENDIMENTOS")
        print("=" * 65)

        if not dados:
            print("Nenhuma clínica ou atendimento cadastrado para gerar o relatório.")
            print("=" * 65)
            return

        print(f"{'Pos.':<5} {'Clínica':<25} {'Cidade':<15} {'Atendimentos':<12}")
        print("-" * 65)
        for i, item in enumerate(dados, start=1):
            nome = item.get("nome", "")[:24]
            cidade = item.get("cidade", "")[:14]
            total = item.get("total_atendimentos", 0)
            print(f"{i:<5} {nome:<25} {cidade:<15} {total:<12}")

        print("=" * 65)
        total_geral = sum(item.get("total_atendimentos", 0) for item in dados)
        print(f"Total geral de atendimentos registrados no sistema: {total_geral}")
        print("=" * 65)

    def mostra_relatorio_atendimentos(self, dados: dict) -> None:
        print("\n" + "=" * 75)
        print("         RELATÓRIO: ATENDIMENTOS MAIS CAROS E MAIS BARATOS")
        print("=" * 75)

        lista = dados.get("mais_caros", [])
        if not lista:
            print("Nenhum atendimento cadastrado para gerar o relatório.")
            print("=" * 75)
            return

        mais_caro = dados.get("destaque_mais_caro")
        mais_barato = dados.get("destaque_mais_barato")

        if mais_caro:
            print(">> ATENDIMENTO MAIS CARO:")
            print(f"   ID: #{mais_caro['id']} | Data: {mais_caro['data']} | Valor Total: R$ {mais_caro['valor_total']:.2f}")
            print(f"   Paciente: {mais_caro['paciente']} | Profissional: {mais_caro['profissional']}")
            print(f"   Clínica: {mais_caro['clinica']} | Tipo: {mais_caro['tipo']}")

        if mais_barato:
            print("\n>> ATENDIMENTO MAIS BARATO:")
            print(f"   ID: #{mais_barato['id']} | Data: {mais_barato['data']} | Valor Total: R$ {mais_barato['valor_total']:.2f}")
            print(f"   Paciente: {mais_barato['paciente']} | Profissional: {mais_barato['profissional']}")
            print(f"   Clínica: {mais_barato['clinica']} | Tipo: {mais_barato['tipo']}")

        print("\n" + "-" * 75)
        print("LISTAGEM GERAL DE ATENDIMENTOS ORDENADA POR VALOR (DECRESCENTE):")
        print(f"{'ID':<6} {'Data':<12} {'Paciente':<18} {'Clínica':<16} {'Valor Total':<12} {'Status':<10}")
        print("-" * 75)

        for item in lista:
            id_str = f"#{item['id']}"
            data_str = item.get("data", "")[:10]
            pac_str = item.get("paciente", "")[:17]
            cli_str = item.get("clinica", "")[:15]
            val_str = f"R$ {item.get('valor_total', 0.0):.2f}"
            status_str = "Quitado" if item.get("saldo_restante", 0.0) == 0 else "Pendente"
            print(f"{id_str:<6} {data_str:<12} {pac_str:<18} {cli_str:<16} {val_str:<12} {status_str:<10}")

        print("=" * 75)
        print(f"Total de atendimentos analisados: {dados.get('total_atendimentos', 0)}")
        print(f"Valor médio por atendimento: R$ {dados.get('valor_medio', 0.0):.2f}")
        print(f"Faturamento total de atendimentos: R$ {dados.get('valor_total_acumulado', 0.0):.2f}")
        print("=" * 75)

    def mostra_relatorio_procedimentos_populares(self, dados: list[dict]) -> None:
        print("\n" + "=" * 70)
        print("       RELATÓRIO: PROCEDIMENTOS MAIS REALIZADOS (MAIS POPULARES)")
        print("=" * 70)

        if not dados:
            print("Nenhum procedimento cadastrado ou realizado para gerar o relatório.")
            print("=" * 70)
            return

        print(f"{'Pos.':<5} {'Procedimento':<25} {'Custo Unit.':<14} {'Qtd Realizada':<14} {'Total Gerado':<12}")
        print("-" * 70)

        for i, item in enumerate(dados, start=1):
            nome = item.get("nome", "")[:24]
            custo = f"R$ {item.get('custo', 0.0):.2f}"
            qtd = item.get("quantidade_realizada", 0)
            total_gerado = f"R$ {item.get('valor_total_gerado', 0.0):.2f}"
            print(f"{i:<5} {nome:<25} {custo:<14} {qtd:<14} {total_gerado:<12}")

        print("=" * 70)
        total_procs = sum(item.get("quantidade_realizada", 0) for item in dados)
        total_faturado = sum(item.get("valor_total_gerado", 0.0) for item in dados)
        print(f"Total de execuções de procedimentos: {total_procs}")
        print(f"Faturamento total em procedimentos: R$ {total_faturado:.2f}")
        print("=" * 70)

    def mostra_relatorio_procedimentos_valores(self, dados: dict) -> None:
        print("\n" + "=" * 70)
        print("       RELATÓRIO: PROCEDIMENTOS MAIS CAROS E MAIS BARATOS")
        print("=" * 70)

        lista = dados.get("mais_caros", [])
        if not lista:
            print("Nenhum procedimento cadastrado para gerar o relatório.")
            print("=" * 70)
            return

        mais_caro = dados.get("destaque_mais_caro")
        mais_barato = dados.get("destaque_mais_barato")

        if mais_caro:
            print(">> PROCEDIMENTO MAIS CARO:")
            print(f"   Nome: {mais_caro['nome']} | Custo: R$ {mais_caro['custo']:.2f}")
            print(f"   Descrição: {mais_caro['descricao']}")
            print(f"   Profissional: {mais_caro['profissional']}")

        if mais_barato:
            print("\n>> PROCEDIMENTO MAIS BARATO:")
            print(f"   Nome: {mais_barato['nome']} | Custo: R$ {mais_barato['custo']:.2f}")
            print(f"   Descrição: {mais_barato['descricao']}")
            print(f"   Profissional: {mais_barato['profissional']}")

        print("\n" + "-" * 70)
        print("LISTAGEM DE PROCEDIMENTOS ORDENADA POR CUSTO (DECRESCENTE):")
        print(f"{'Pos.':<5} {'Nome':<25} {'Custo (R$)':<15} {'Profissional Responsável':<25}")
        print("-" * 70)

        for i, item in enumerate(lista, start=1):
            nome = item.get("nome", "")[:24]
            custo = f"R$ {item.get('custo', 0.0):.2f}"
            prof = item.get("profissional", "")[:24]
            print(f"{i:<5} {nome:<25} {custo:<15} {prof:<25}")

        print("=" * 70)
        print(f"Total de procedimentos cadastrados: {dados.get('total_procedimentos', 0)}")
        print(f"Custo médio dos procedimentos: R$ {dados.get('custo_medio', 0.0):.2f}")
        print("=" * 70)
