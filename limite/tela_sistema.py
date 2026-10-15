class TelaSistema:
    def opcoes_tela(self) -> int:
        print("\n" + "=" * 32)
        print("       SISTEMA DE CLÍNICAS")
        print("=" * 32)
        print("1 - Gerenciar Clínicas")
        print("2 - Gerenciar Pacientes")
        print("3 - Gerenciar Profissionais de Saúde")
        print("4 - Gerenciar Procedimentos")
        print("5 - Gerenciar Tipos de Atendimento")
        print("0 - Finalizar Sistema")
        print("=" * 32)
        return self.le_numero_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4, 5])

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
