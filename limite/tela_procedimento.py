class TelaProcedimento:
    def opcoes_tela(self):
        print("\n" + "=" * 30)
        print("        PROCEDIMENTOS")
        print("=" * 30)
        print("1 - Cadastrar Procedimento")
        print("2 - Excluir Procedimento")
        print("3 - Alterar Procedimento")
        print("4 - Listar Procedimentos")
        print("5 - Buscar Procedimento")
        print("0 - Retornar")
        print("=" * 30)
        return self.le_numero_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4, 5])

    def tela_opcoes(self):
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

    def seleciona_procedimento(self):
        print("\n--- Selecionar Procedimento ---")
        return input("Digite o nome do procedimento: ").strip()

    def coletar_dados(self):
        print("\n--- Cadastro de Procedimento ---")
        nome = input("Nome: ").strip()
        descricao = input("Descrição: ").strip()
        custo = float(input("Custo (R$): "))
        registro_profissional = input("Registro Profissional do Responsável: ").strip()

        return {
            "nome": nome,
            "descricao": descricao,
            "custo": custo,
            "registro_profissional": registro_profissional,
        }

    def coletar_novos_dados(self):
        print("\n--- Alteração de Procedimento ---")
        print("(Deixe em branco os campos que não deseja alterar)")
        nome = input("Novo Nome: ").strip()
        descricao = input("Nova Descrição: ").strip()
        custo_str = input("Novo Custo (R$): ").strip()
        registro_profissional = input("Novo Registro do Responsável: ").strip()

        novos_dados = {}
        if nome:
            novos_dados["nome"] = nome
        if descricao:
            novos_dados["descricao"] = descricao
        if custo_str:
            novos_dados["custo"] = float(custo_str)
        if registro_profissional:
            novos_dados["registro_profissional"] = registro_profissional

        return novos_dados

    def mostra_procedimento(self, dados):
        print("-" * 35)
        print(f"Nome: {dados.get('nome')}")
        print(f"Descrição: {dados.get('descricao')}")
        print(f"Custo: R$ {dados.get('custo')}")
        prof = dados.get("profissional_responsavel")
        if prof:
            print(f"Profissional Responsável: {prof.nome} (Registro: {prof.registro_profissional})")
        else:
            print("Profissional Responsável: Não informado")
        print("-" * 35)
