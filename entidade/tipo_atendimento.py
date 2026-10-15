from excecoes.dado_invalido_exception import DadoInvalidoException


class TipoAtendimento:
    def __init__(self, nome_tipo: str):
        self.nome_tipo = nome_tipo

    @property
    def nome_tipo(self):
        return self.__nome_tipo

    @nome_tipo.setter
    def nome_tipo(self, nome_tipo: str):
        if not isinstance(nome_tipo, str) or not nome_tipo.strip():
            raise DadoInvalidoException("nome_tipo", "deve ser um texto não vazio")
        self.__nome_tipo = nome_tipo.strip()
