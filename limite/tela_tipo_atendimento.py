class TelaTipoAtendimento:
    def opcoes_tela(self):
        print("\n" + "=" * 30)
        print("    TIPOS DE ATENDIMENTO")
        print("=" * 30)
        print("1 - Cadastrar Tipo de Atendimento")
        print("2 - Excluir Tipo de Atendimento")
        print("3 - Alterar Tipo de Atendimento")
        print("4 - Listar Tipos de Atendimento")
        print("5 - Buscar Tipo de Atendimento")
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

    def seleciona_tipo_atendimento(self):
        print("\n--- Selecionar Tipo de Atendimento ---")
        return input("Digite o nome do tipo de atendimento: ").strip()

    def coletar_dados(self):
        print("\n--- Cadastro de Tipo de Atendimento ---")
        nome_tipo = input("Nome do tipo (ex: Consulta, Exame, Retorno): ").strip()
        return {"nome_tipo": nome_tipo}

    def coletar_novos_dados(self):
        print("\n--- Alteração de Tipo de Atendimento ---")
        return input("Novo nome do tipo de atendimento: ").strip()

    def mostra_tipo_atendimento(self, dados):
        print("-" * 35)
        print(f"Tipo de Atendimento: {dados.get('nome_tipo')}")
        print("-" * 35)
