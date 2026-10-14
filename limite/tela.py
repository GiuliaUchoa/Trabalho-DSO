from abc import ABC, abstractmethod


class Tela(ABC):
    @abstractmethod
    def tela_opcoes(self) -> int:
        pass

    def mostra_mensagem(self, mensagem: str) -> None:
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
