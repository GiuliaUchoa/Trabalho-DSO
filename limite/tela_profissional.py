from limite.tela import Tela


class TelaProfissional(Tela):
    def opcoes_tela(self) -> int:
        print("\n" + "=" * 30)
        print("    PROFISSIONAIS DE SAÚDE")
        print("=" * 30)
        print("1 - Cadastrar Profissional")
        print("2 - Excluir Profissional")
        print("3 - Atualizar Profissional")
        print("4 - Listar Profissionais")
        print("5 - Buscar Profissional")
        print("0 - Retornar")
        print("=" * 30)
        return self.le_numero_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4, 5])

    def tela_opcoes(self) -> int:
        # Garante compatibilidade com a assinatura abstrata da superclasse Tela
        return self.opcoes_tela()

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

    def buscar_por_cpf(self) -> str:
        return input("Digite o CPF do Profissional: ").strip()

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
        clinica = dados.get("clinica")
        nome_clinica = clinica.nome if clinica else "Nenhuma clínica vinculada"
        print(f"Clínica: {nome_clinica}")
        print("-" * 35)
