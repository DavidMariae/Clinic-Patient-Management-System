class ClinicError(Exception):
    """Classe base para exceções do sistema."""

    pass


class PacienteNaoEncontradoError(ClinicError):
    """Erro lançado quando um CPF/ID não existe no JSON."""

    def __init__(self, identificador):
        super().__init__(
            f"Paciente com ID/Documento '{identificador}' não foi localizado."
        )


class ErroGravacaoDados(ClinicError):
    """Erro ao tentar escrever no arquivo JSON."""

    pass
