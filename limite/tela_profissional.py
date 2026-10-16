class TelaProfissional:
    def opcoes_tela(self) -> int:
        print("\n" + "=" * 30)
        print("    PROFISSIONAIS DE SAÚDE")
        print("=" * 30)
        print("1 - Cadastrar Profissional")
        print("2 - Excluir Profissional")
        print("3 - Alterar Profissional")
        print("4 - Listar Profissionais")
        print("5 - Buscar Profissional")
        print("0 - Retornar")
        print("=" * 30)
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

    def coletar_dados(self) -> dict:
        print("\n--- Cadastro de Profissional de Saúde ---")
        nome = input("Nome: ").strip()
        celular = input("Celular: ").strip()
        cpf = input("CPF: ").strip()
        especialidade = input("Especialidade: ").strip()
        registro = input("Registro Profissional (ex: CRM 12345): ").strip()
        return {
            "nome": nome,
            "celular": celular,
            "cpf": cpf,
            "especialidade": especialidade,
            "registro": registro,
        }

    def buscar_profissional(self) -> str:
        print("\n--- Busca de Profissional ---")
        return input("Digite o Registro Profissional: ").strip()

    def coletar_novos_dados(self) -> dict:
        print("\n--- Atualização de Profissional ---")
        print("(Deixe em branco os campos que não deseja alterar)")
        nome = input("Novo Nome: ").strip()
        celular = input("Novo Celular: ").strip()
        especialidade = input("Nova Especialidade: ").strip()
        registro = input("Novo Registro Profissional: ").strip()

        novos_dados = {}
        if nome:
            novos_dados["nome"] = nome
        if celular:
            novos_dados["celular"] = celular
        if especialidade:
            novos_dados["especialidade"] = especialidade
        if registro:
            novos_dados["registro"] = registro

        return novos_dados

    def mostra_profissional(self, dados: dict) -> None:
        print("-" * 35)
        print(f"Nome: {dados.get('nome')}")
        print(f"CPF: {dados.get('cpf')}")
        print(f"Celular: {dados.get('celular')}")
        print(f"Especialidade: {dados.get('especialidade')}")
        print(f"Registro Profissional: {dados.get('registro_profissional')}")
        print("-" * 35)
