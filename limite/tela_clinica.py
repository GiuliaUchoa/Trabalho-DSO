from datetime import time


class TelaClinica:
    def opcoes_tela(self) -> int:
        print("\n" + "=" * 30)
        print("           CLÍNICAS")
        print("=" * 30)
        print("1 - Cadastrar Clínica")
        print("2 - Excluir Clínica")
        print("3 - Alterar Clínica")
        print("4 - Listar Clínicas")
        print("5 - Buscar Clínica")
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

    def le_horario(self, mensagem: str, default: time = None) -> time:
        while True:
            sufixo_default = f" [padrão: {default.strftime('%H:%M')}]: " if default else ": "
            entrada = input(f"{mensagem}{sufixo_default}").strip()
            if not entrada and default is not None:
                return default
            try:
                partes = entrada.split(":")
                if len(partes) != 2:
                    raise ValueError
                hora = int(partes[0])
                minuto = int(partes[1])
                return time(hour=hora, minute=minuto)
            except (ValueError, TypeError):
                print("Horário inválido! Utilize o formato HH:MM (ex: 08:00).")

    def coletar_dados(self) -> dict:
        print("\n--- Cadastro de Clínica ---")
        nome = input("Nome da Clínica: ").strip()
        cidade = input("Cidade: ").strip()
        descricao = input("Descrição: ").strip()
        hora_abertura = self.le_horario("Hora de Abertura (HH:MM)", default=time(8, 0))
        hora_fechamento = self.le_horario("Hora de Fechamento (HH:MM)", default=time(18, 0))

        return {
            "nome": nome,
            "cidade": cidade,
            "descricao": descricao,
            "hora_abertura": hora_abertura,
            "hora_fechamento": hora_fechamento,
        }

    def buscar_clinica(self) -> str:
        print("\n--- Busca de Clínica ---")
        return input("Digite o nome da clínica: ").strip()

    def buscar_profissional(self) -> str:
        """
        Método presente no diagrama UML sob TelaClinica (provável erro de cópia de TelaProfissional).
        Redireciona para buscar_clinica() mantendo total fidelidade à assinatura do diagrama.
        """
        return self.buscar_clinica()

    def coletar_novos_dados(self) -> dict:
        print("\n--- Alteração de Clínica ---")
        print("(Deixe em branco os campos que não deseja alterar)")
        nome = input("Novo Nome: ").strip()
        cidade = input("Nova Cidade: ").strip()
        descricao = input("Nova Descrição: ").strip()

        novos_dados = {}
        if nome:
            novos_dados["nome"] = nome
        if cidade:
            novos_dados["cidade"] = cidade
        if descricao:
            novos_dados["descricao"] = descricao

        alterar_horarios = input("Deseja alterar os horários de funcionamento? (s/N): ").strip().lower()
        if alterar_horarios == "s":
            hora_abertura = self.le_horario("Nova Hora de Abertura (HH:MM)")
            hora_fechamento = self.le_horario("Nova Hora de Fechamento (HH:MM)")
            novos_dados["hora_abertura"] = hora_abertura
            novos_dados["hora_fechamento"] = hora_fechamento

        return novos_dados

    def mostra_clinica(self, dados: dict) -> None:
        print("-" * 35)
        print(f"Nome: {dados.get('nome')}")
        print(f"Cidade: {dados.get('cidade')}")
        print(f"Descrição: {dados.get('descricao')}")
        abertura = dados.get("hora_abertura")
        fechamento = dados.get("hora_fechamento")
        str_abertura = abertura.strftime("%H:%M") if hasattr(abertura, "strftime") else str(abertura)
        str_fechamento = fechamento.strftime("%H:%M") if hasattr(fechamento, "strftime") else str(fechamento)
        print(f"Horário de Funcionamento: {str_abertura} às {str_fechamento}")

        profissionais = dados.get("profissionais", [])
        if profissionais:
            nomes_profissionais = [p.nome for p in profissionais]
            print(f"Profissionais ({len(profissionais)}): {', '.join(nomes_profissionais)}")
        else:
            print("Profissionais: Nenhum profissional vinculado")

        atendimentos = dados.get("atendimentos", [])
        print(f"Atendimentos registrados: {len(atendimentos)}")
        print("-" * 35)
