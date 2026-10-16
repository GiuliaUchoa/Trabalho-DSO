class PagamentoInvalidoException(Exception):
    def __init__(self, mensagem="Erro ao processar pagamento."):
        super().__init__(mensagem)
