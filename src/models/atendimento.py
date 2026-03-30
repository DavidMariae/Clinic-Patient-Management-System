class Atendimento:
    def __init__(
        self,
        id_atendimento,
        paciente_id,
        data,
        tipo,
        observacoes,
        status="Em acompanhamento",
    ):
        self.id = id_atendimento
        self.paciente_id = paciente_id
        self.data = data
        self.tipo = tipo
        self.observacoes = observacoes
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "paciente_id": self.paciente_id,
            "data": self.data,
            "tipo": self.tipo,
            "observacoes": self.observacoes,
            "status": self.status,
        }

    @classmethod  # Chama o método da classe sem precisar instanciar, recebendo a classe como referência, diferente do staticmethod
    def from_dict(cls, dados):
        return cls(
            id_atendimento=dados["id"],
            paciente_id=dados["paciente_id"],
            data=dados["data"],
            tipo=dados["tipo"],
            observacoes=dados["observacoes"],
            status=dados["status"],
        )
