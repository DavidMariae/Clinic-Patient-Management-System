class Paciente:
    def __init__(self, id, nome, data_nasc, telefone, email, documento):
        self.id = id  # Esta linha é a que está faltando!
        self.nome = nome
        self.data_nasc = data_nasc
        self.telefone = telefone
        self.email = email
        self.documento = documento

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "data_nasc": self.data_nasc,
            "telefone": self.telefone,
            "email": self.email,
            "documento": self.documento,
        }

    @classmethod  # Chama o método da classe sem precisar instanciar, recebendo a classe como referência, diferente do staticmethod
    def from_dict(dados):
        """Cria um objeto Paciente a partir de um dicionário (vindo do JSON)."""
        return Paciente(
            id=dados["id"],
            nome=dados["nome"],
            data_nasc=dados["data_nasc"],
            telefone=dados["telefone"],
            email=dados["email"],
            documento=dados["doc"],
        )
