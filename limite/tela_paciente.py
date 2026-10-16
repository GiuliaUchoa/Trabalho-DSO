from datetime import date, datetime
from typing import Optional


class TelaPaciente:
    def opcoes_tela(self) -> int:
        print("\n" + "=" * 30)
        print("          PACIENTES")
        print("=" * 30)
        print("1 - Cadastrar Paciente")
        print("2 - Excluir Paciente")
        print("3 - Alterar Paciente")
        print("4 - Listar Pacientes")
        print("5 - Buscar Paciente")
        print("0 - Retornar")
        print("=" * 30)
        return self.le_numero_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4, 5])

    def mostrar_mensagem(self, mensagem: str) -> None:
        print(f"\n{mensagem}")

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

    def le_data(self, mensagem: str = "Data de Nascimento (DD/MM/AAAA): ") -> str:
        while True:
            texto = input(mensagem).strip()
            try:
                data_obj = datetime.strptime(texto, "%d/%m/%Y").date()
                if data_obj > date.today():
                    print("A data de nascimento não pode estar no futuro!")
                    continue
                return texto
            except ValueError:
                print("Formato de data inválido! Digite no padrão DD/MM/AAAA (ex: 15/06/2006).")

    def coletar_dados(self) -> dict:
        print("\n--- Cadastro de Paciente ---")
        nome = input("Nome: ").strip()
        celular = input("Celular: ").strip()
        cpf = input("CPF: ").strip()
        data_nasc = self.le_data("Data de Nascimento (DD/MM/AAAA): ")
        return {
            "nome": nome,
            "celular": celular,
            "cpf": cpf,
            "data_nascimento": data_nasc,
        }

    def buscar_paciente(self) -> str:
        print("\n--- Busca de Paciente ---")
        return input("Digite o CPF do paciente: ").strip()

    def coletar_novos_dados(self) -> dict:
        print("\n--- Atualização de Paciente ---")
        print("(Deixe em branco os campos que não deseja alterar)")
        nome = input("Novo Nome: ").strip()
        celular = input("Novo Celular: ").strip()
        data_str = input("Nova Data de Nascimento (DD/MM/AAAA ou Enter para manter): ").strip()
        data_nasc = None
        if data_str:
            while True:
                try:
                    data_obj = datetime.strptime(data_str, "%d/%m/%Y").date()
                    if data_obj > date.today():
                        print("A data de nascimento não pode estar no futuro!")
                        data_str = input("Nova Data de Nascimento (DD/MM/AAAA): ").strip()
                        continue
                    data_nasc = data_str
                    break
                except ValueError:
                    print("Formato de data inválido! Digite no formato DD/MM/AAAA.")
                    data_str = input("Nova Data de Nascimento (DD/MM/AAAA): ").strip()

        novos_dados = {}
        if nome:
            novos_dados["nome"] = nome
        if celular:
            novos_dados["celular"] = celular
        if data_nasc is not None:
            novos_dados["data_nascimento"] = data_nasc

        return novos_dados

    def mostra_cabecalho_lista(self) -> None:
        print("\n--- Lista de Pacientes ---")

    def mostra_paciente(self, dados: dict) -> None:
        print("-" * 35)
        print(f"Nome: {dados.get('nome')}")
        print(f"CPF: {dados.get('cpf')}")
        print(f"Celular: {dados.get('celular')}")
        data_nasc = dados.get("data_nascimento")
        if isinstance(data_nasc, date):
            data_formatada = data_nasc.strftime("%d/%m/%Y")
        else:
            data_formatada = str(data_nasc)
        print(f"Data de Nascimento: {data_formatada}")
        print("-" * 35)
