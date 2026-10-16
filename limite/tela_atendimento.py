from datetime import date, datetime, time
from typing import Optional


class TelaAtendimento:
    def opcoes_tela(self) -> int:
        print("\n" + "=" * 32)
        print("          ATENDIMENTOS")
        print("=" * 32)
        print("1 - Agendar Atendimento")
        print("2 - Excluir Atendimento")
        print("3 - Alterar Atendimento")
        print("4 - Listar Atendimentos")
        print("5 - Buscar Atendimento")
        print("6 - Registrar Procedimento no Atendimento")
        print("7 - Realizar Pagamento")
        print("0 - Retornar")
        print("=" * 32)
        return self.le_numero_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4, 5, 6, 7])

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

    def le_numero_float(self, mensagem: str = "Valor: ", minimo: float = 0.0) -> float:
        while True:
            try:
                entrada = input(mensagem).strip().replace(",", ".")
                valor = float(entrada)
                if valor < minimo:
                    print(f"O valor não pode ser menor que {minimo:.2f}!")
                    continue
                return valor
            except ValueError:
                print("Valor inválido! Digite um número decimal válido (ex: 150.00).")

    def le_data(self, mensagem: str = "Data (DD/MM/AAAA): ") -> date:
        while True:
            texto = input(mensagem).strip()
            try:
                return datetime.strptime(texto, "%d/%m/%Y").date()
            except ValueError:
                print("Formato de data inválido! Digite no padrão DD/MM/AAAA (ex: 20/10/2026).")

    def le_horario(self, mensagem: str) -> time:
        while True:
            entrada = input(f"{mensagem} (HH:MM): ").strip()
            try:
                partes = entrada.split(":")
                if len(partes) != 2:
                    raise ValueError
                hora = int(partes[0])
                minuto = int(partes[1])
                return time(hour=hora, minute=minuto)
            except (ValueError, TypeError):
                print("Horário inválido! Utilize o formato HH:MM (ex: 09:30).")

    def buscar_atendimento(self) -> int:
        print("\n--- Selecionar Atendimento ---")
        return self.le_numero_inteiro("Digite o código (ID) do atendimento: ")

    def perguntar_se_menor_esta_acompanhado(self) -> bool:
        print("\n[Atenção] O paciente selecionado é menor de 18 anos.")
        resposta = input("O paciente estará acompanhado de um responsável legal? (S/N): ").strip().upper()
        return resposta in ("S", "SIM")

    def coletar_dados(self) -> dict:
        print("\n--- Agendamento de Atendimento ---")
        nome_clinica = input("Nome da Clínica: ").strip()
        cpf_paciente = input("CPF do Paciente: ").strip()
        registro_profissional = input("Registro do Profissional (CRM): ").strip()
        nome_tipo = input("Nome do Tipo de Atendimento (ex: Consulta, Exame): ").strip()
        data_atendimento = self.le_data("Data do Atendimento (DD/MM/AAAA): ")
        hora_inicio = self.le_horario("Horário de Início")
        hora_fim = self.le_horario("Horário de Término")
        valor = self.le_numero_float("Valor base do atendimento (R$): ", minimo=0.0)

        return {
            "nome_clinica": nome_clinica,
            "cpf_paciente": cpf_paciente,
            "registro_profissional": registro_profissional,
            "nome_tipo": nome_tipo,
            "data": data_atendimento,
            "horario_inicio": hora_inicio,
            "horario_fim": hora_fim,
            "valor_total": valor,
        }

    def coletar_novos_dados(self) -> dict:
        print("\n--- Alteração de Atendimento ---")
        print("(Deixe em branco os campos que não deseja alterar)")
        data_str = input("Nova Data (DD/MM/AAAA ou Enter para manter): ").strip()
        nova_data = None
        if data_str:
            while True:
                try:
                    nova_data = datetime.strptime(data_str, "%d/%m/%Y").date()
                    break
                except ValueError:
                    print("Data inválida!")
                    data_str = input("Nova Data (DD/MM/AAAA): ").strip()

        mudar_horarios = input("Deseja alterar os horários? (S/N): ").strip().upper() in ("S", "SIM")
        novo_inicio = None
        novo_fim = None
        if mudar_horarios:
            novo_inicio = self.le_horario("Novo Horário de Início")
            novo_fim = self.le_horario("Novo Horário de Término")

        valor_str = input("Novo Valor Base (ou Enter para manter): ").strip().replace(",", ".")
        novo_valor = None
        if valor_str:
            try:
                novo_valor = float(valor_str)
            except ValueError:
                pass

        novos_dados = {}
        if nova_data is not None:
            novos_dados["data"] = nova_data
        if novo_inicio is not None and novo_fim is not None:
            novos_dados["horario_inicio"] = novo_inicio
            novos_dados["horario_fim"] = novo_fim
        if novo_valor is not None:
            novos_dados["valor_total"] = novo_valor

        return novos_dados

    def coletar_nome_procedimento(self) -> str:
        print("\n--- Registro de Procedimento no Atendimento ---")
        return input("Nome do Procedimento a incluir: ").strip()

    def perguntar_forma_pagamento(self) -> int:
        print("\n--- Forma de Pagamento ---")
        print("1 - Dinheiro")
        print("2 - PIX")
        print("3 - Cartão de Crédito")
        print("0 - Cancelar")
        return self.le_numero_inteiro("Escolha a modalidade: ", [0, 1, 2, 3])

    def coletar_dados_pagamento(self, forma_pagamento: int, valor_restante: float, data_atendimento: date) -> dict:
        print(f"\nValor restante a pagar: R$ {valor_restante:.2f}")
        valor_pago = self.le_numero_float("Valor a pagar agora (R$): ", minimo=0.01)
        data_pagamento = self.le_data(f"Data do pagamento (máximo {data_atendimento.strftime('%d/%m/%Y')}): ")

        dados = {
            "valor_pago": valor_pago,
            "data_pagamento": data_pagamento,
        }

        if forma_pagamento == 2:  # PIX
            cpf_pagador = input("CPF do Pagador: ").strip()
            dados["cpf_pagador"] = cpf_pagador
        elif forma_pagamento == 3:  # Cartão
            numero_cartao = input("Número do Cartão: ").strip()
            bandeira = input("Bandeira do Cartão (ex: Visa, Mastercard): ").strip()
            dados["numero_cartao"] = numero_cartao
            dados["bandeira"] = bandeira

        return dados

    def mostra_cabecalho_lista(self) -> None:
        print("\n--- Lista de Atendimentos Cadastrados ---")

    def mostra_atendimento(self, dados: dict) -> None:
        print("\n" + "=" * 45)
        print(f"ATENDIMENTO #{dados.get('id_atendimento')}")
        print("=" * 45)
        print(f"Clínica: {dados.get('clinica')}")
        print(f"Paciente: {dados.get('paciente')} (CPF: {dados.get('cpf_paciente')})")
        print(f"Profissional: {dados.get('profissional')} ({dados.get('registro_profissional')})")
        print(f"Tipo: {dados.get('tipo_atendimento')}")
        print(f"Data: {dados.get('data')}")
        print(f"Horário: {dados.get('horario_inicio')} às {dados.get('horario_fim')}")
        print(f"Valor Base: R$ {dados.get('valor_base'):.2f}")

        procedimentos = dados.get("procedimentos", [])
        if procedimentos:
            print("\nProcedimentos Realizados:")
            for proc in procedimentos:
                print(f"  - {proc.get('nome')}: R$ {proc.get('custo'):.2f} (Resp: {proc.get('responsavel')})")
            print(f"Custo Total Procedimentos: R$ {dados.get('custo_procedimentos'):.2f}")
        else:
            print("Procedimentos Realizados: Nenhum procedimento registrado")

        print(f"\nValor Total Geral: R$ {dados.get('valor_total_geral'):.2f}")
        print(f"Total Pago: R$ {dados.get('total_pago'):.2f}")
        print(f"Saldo Restante: R$ {dados.get('saldo_restante'):.2f}")
        status_pag = "QUITADO" if dados.get("saldo_restante", 0) <= 0 else "PENDENTE"
        print(f"Status do Pagamento: {status_pag}")

        pagamentos = dados.get("pagamentos", [])
        if pagamentos:
            print("\nHistórico de Pagamentos:")
            for pag in pagamentos:
                print(f"  - {pag.get('tipo')}: R$ {pag.get('valor'):.2f} em {pag.get('data')} ({pag.get('detalhes')})")
        print("=" * 45)
