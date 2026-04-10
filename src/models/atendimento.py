# ════════════════════════════════════════════════════════════════
# Representa um atendimento clínico realizado para um paciente.
# A ligação entre Atendimento e Paciente é feita pelo paciente_id - Chave estrangeira?
# ════════════════════════════════════════════════════════════════

class Atendimento:
    """
    Representa um atendimento registrado no sistema.
    Sempre está vinculado a um Paciente através do paciente_id.
    """

    def __init__(self, id: int, paciente_id: int, data: str,
                 tipo: str, observacoes: str, status: str):
        """
        Construtor do Atendimento.

        Parâmetros:
            id          → identificador único numérico
            paciente_id → ID do paciente atendido (referência ao Paciente)
            data        → data no formato ISO: AAAA-MM-DD
            tipo        → tipo do atendimento (Consulta, Retorno, Exame, etc.)
            observacoes → anotações clínicas do profissional
            status      → "Realizado" ou "Em acompanhamento"
        """
        self.id          = id
        self.paciente_id = paciente_id  # Chave de ligação com o Paciente
        self.data        = data
        self.tipo        = tipo
        self.observacoes = observacoes
        self.status      = status

    def to_dict(self) -> dict:
        """
        Converte o objeto Atendimento em dicionário para salvar no JSON.
        Segue o mesmo padrão do Paciente.to_dict().
        """
        return {
            "id":          self.id,
            "paciente_id": self.paciente_id,
            "data":        self.data,
            "tipo":        self.tipo,
            "observacoes": self.observacoes,
            "status":      self.status
        }