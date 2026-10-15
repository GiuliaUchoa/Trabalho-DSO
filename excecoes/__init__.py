from excecoes.clinica_ja_cadastrada_exception import ClinicaJaCadastradaException
from excecoes.clinica_nao_encontrada_exception import ClinicaNaoEncontradaException
from excecoes.horario_invalido_exception import HorarioInvalidoException
from excecoes.dado_invalido_exception import DadoInvalidoException
from excecoes.profissional_ja_cadastrado_exception import (
    ProfissionalJaCadastradoException,
    RegistroJaCadastradoException,
    CpfJaCadastradoException,
)
from excecoes.profissional_nao_encontrado_exception import ProfissionalNaoEncontradoException
from excecoes.procedimento_ja_cadastrado_exception import ProcedimentoJaCadastradoException
from excecoes.procedimento_nao_encontrado_exception import ProcedimentoNaoEncontradoException

__all__ = [
    "ClinicaJaCadastradaException",
    "ClinicaNaoEncontradaException",
    "HorarioInvalidoException",
    "DadoInvalidoException",
    "ProfissionalJaCadastradoException",
    "RegistroJaCadastradoException",
    "CpfJaCadastradoException",
    "ProfissionalNaoEncontradoException",
    "ProcedimentoJaCadastradoException",
    "ProcedimentoNaoEncontradoException",
]
