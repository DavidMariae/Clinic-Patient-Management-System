class Paciente:
    def __init__(self, id_paciente, nome, data_nascimento, telefone, email, documento):
        self.id = id_paciente
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.email = email
        self.documento = documento  # CPF ou RG conforme o PDF

    def to_dict(self):
        """Converte o objeto para dicionário (para salvar no JSON)."""
        return {
            "id": self.id,
            "nome": self.nome,
            "data_nascimento": self.data_nascimento,
            "telefone": self.telefone,
            "email": self.email,
            "documento": self.documento,
        }

    @classmethod  # Chama o método da classe sem precisar instanciar, recebendo a classe como referência, diferente do staticmethod
    def from_dict(cls, dados):
        """Cria um objeto Paciente a partir de um dicionário (vindo do JSON)."""
        return cls(
            id_paciente=dados["id"],
            nome=dados["nome"],
            data_nascimento=dados["data_nascimento"],
            telefone=dados["telefone"],
            email=dados["email"],
            documento=dados["documento"],
        )
