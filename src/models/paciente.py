# ════════════════════════════════════════════════════════════════
# Representação de um objeto do mundo real dentro do código.
# A classe Paciente define quais dados um paciente tem e como esses dados podem ser manipulados.

# Dicionário é genérico: {"nome": "Maria", "telefone": "88..."}
# Classe é semântica: paciente.nome, paciente.telefone
# Classe garante que todo paciente tem os mesmos campos
# O método to_dict() centraliza a serialização para JSON
# ════════════════════════════════════════════════════════════════

class Paciente:
    """
    Representa um paciente cadastrado no sistema.
    Armazena os dados pessoais e de contato do paciente.
    """

    def __init__(self, id: int, nome: str, data_nascimento: str,
                 telefone: str, email: str, documento: str):
        """
        Construtor — chamado ao criar um novo objeto Paciente.
        Define e inicializa todos os atributos da instância.

        Parâmetros:
            id                → identificador único numérico
            nome              → nome completo
            data_nascimento   → data no formato ISO: AAAA-MM-DD
            telefone          → número de telefone
            email             → endereço de e-mail (opcional)
            documento         → CPF ou RG
        """
        # self. indica que são atributos do objeto (não variáveis locais)
        self.id              = id
        self.nome            = nome
        self.data_nascimento = data_nascimento
        self.telefone        = telefone
        self.email           = email
        self.documento       = documento

    def to_dict(self) -> dict:
        """
        Converte o objeto Paciente em um dicionário Python.
        Necessário para salvar no JSON, que não aceita objetos Python diretamente.

        Princípio do encapsulamento — cada classe é responsável
        pelos seus próprios dados. Se adicionarmos um campo novo
        ao Paciente, atualizamos só aqui, não no controller.

        Retorna:
            Dicionário com todos os campos do paciente
        """
        return {
            "id":               self.id,
            "nome":             self.nome,
            "data_nascimento":  self.data_nascimento,
            "telefone":         self.telefone,
            "email":            self.email,
            "documento":        self.documento
        }