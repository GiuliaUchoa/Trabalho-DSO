from abc import ABC, abstractmethod


class Controlador(ABC):
    def __init__(self, controlador_sistema=None):
        self.__controlador_sistema = controlador_sistema

    @property
    def controlador_sistema(self):
        return self.__controlador_sistema

    @abstractmethod
    def abre_tela(self) -> None:
        pass

    def retornar(self) -> None:
        if self.__controlador_sistema is not None:
            self.__controlador_sistema.abre_tela()
