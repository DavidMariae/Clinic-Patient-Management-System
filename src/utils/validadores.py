import re
from exceptions import AtendimentoInvalido


class Validador:
    """
    Classe utilitária com métodos estáticos de validação.
    Usada pelas views antes de chamar o controller.
    """

    # ══════════════════════════════════════════════════════════
    # NOME
    # ══════════════════════════════════════════════════════════

    @staticmethod
    def nome(valor: str) -> str:
        """
        Valida nome completo.
        Deve ter pelo menos 2 palavras e 3 caracteres.
        Retorna o nome limpo ou lança exceção.
        """
        valor = valor.strip()
        if not valor:
            raise AtendimentoInvalido("Nome é obrigatório.")
        if len(valor) < 3:
            raise AtendimentoInvalido(
                "Nome deve ter pelo menos 3 caracteres.")
        if len(valor.split()) < 2:
            raise AtendimentoInvalido(
                "Informe o nome completo (nome e sobrenome).")
        return valor

    # ══════════════════════════════════════════════════════════
    # DATA
    # ══════════════════════════════════════════════════════════

    @staticmethod
    def data_nascimento(valor: str) -> str:
        """
        Valida data no formato DD/MM/AAAA.
        Retorna a data limpa ou lança exceção.
        """
        valor = valor.strip()
        if not valor:
            raise AtendimentoInvalido("Data de nascimento é obrigatória.")

        padrao = r"^\d{2}/\d{2}/\d{4}$"
        if not re.match(padrao, valor):
            raise AtendimentoInvalido(
                "Data inválida. Use o formato DD/MM/AAAA.")

        try:
            d, m, a = int(valor[:2]), int(valor[3:5]), int(valor[6:])
            if not (1 <= m <= 12):
                raise AtendimentoInvalido("Mês inválido.")
            if not (1 <= d <= 31):
                raise AtendimentoInvalido("Dia inválido.")
            if a < 1900 or a > 2100:
                raise AtendimentoInvalido("Ano inválido.")
        except AtendimentoInvalido:
            raise
        except Exception:
            raise AtendimentoInvalido(
                "Data inválida. Use o formato DD/MM/AAAA.")

        return valor

    @staticmethod
    def data_atendimento(valor: str) -> str:
        """
        Valida data de atendimento no formato DD/MM/AAAA.
        Retorna a data limpa ou lança exceção.
        """
        valor = valor.strip()
        if not valor:
            raise AtendimentoInvalido("Data do atendimento é obrigatória.")

        padrao = r"^\d{2}/\d{2}/\d{4}$"
        if not re.match(padrao, valor):
            raise AtendimentoInvalido(
                "Data inválida. Use o formato DD/MM/AAAA.")
        return valor

    # ══════════════════════════════════════════════════════════
    # TELEFONE
    # ══════════════════════════════════════════════════════════

    @staticmethod
    def telefone(valor: str) -> str:
        """
        Valida telefone brasileiro.
        Aceita formatos: (88) 99999-9999, 88999999999, 9999-9999 etc.
        Retorna apenas os dígitos ou lança exceção.
        """
        valor = valor.strip()
        if not valor:
            raise AtendimentoInvalido("Telefone é obrigatório.")

        apenas_digitos = re.sub(r"\D", "", valor)
        if len(apenas_digitos) < 8 or len(apenas_digitos) > 11:
            raise AtendimentoInvalido(
                "Telefone inválido. Use o formato (88) 99999-9999.")
        return valor

    # ══════════════════════════════════════════════════════════
    # EMAIL
    # ══════════════════════════════════════════════════════════

    @staticmethod
    def email(valor: str) -> str:
        """
        Valida e-mail. Campo opcional — se vazio retorna string vazia.
        Se preenchido, valida o formato básico.
        """
        valor = valor.strip()
        if not valor:
            return ""

        padrao = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(padrao, valor):
            raise AtendimentoInvalido(
                "E-mail inválido. Ex: nome@email.com.")
        return valor

    # ══════════════════════════════════════════════════════════
    # DOCUMENTO
    # ══════════════════════════════════════════════════════════

    @staticmethod
    def documento(valor: str) -> str:
        """
        Valida CPF ou RG.
        Aceita formatos com ou sem pontuação.
        Retorna o documento limpo ou lança exceção.
        """
        valor = valor.strip()
        if not valor:
            raise AtendimentoInvalido("Documento (CPF ou RG) é obrigatório.")

        apenas_digitos = re.sub(r"\D", "", valor)
        if len(apenas_digitos) < 8:
            raise AtendimentoInvalido(
                "Documento inválido. Informe um CPF ou RG válido.")
        return valor

    # ══════════════════════════════════════════════════════════
    # CAMPOS GERAIS
    # ══════════════════════════════════════════════════════════

    @staticmethod
    def obrigatorio(valor: str, nome_campo: str) -> str:
        """
        Valida qualquer campo obrigatório genérico.
        Retorna o valor limpo ou lança exceção.
        """
        valor = valor.strip()
        if not valor:
            raise AtendimentoInvalido(f"{nome_campo} é obrigatório.")
        return valor

    @staticmethod
    def tipo_atendimento(valor: str) -> str:
        """
        Valida o tipo de atendimento.
        Deve ser um dos tipos aceitos pelo sistema.
        """
        tipos_validos = [
            "Consulta", "Retorno", "Exame",
            "Procedimento", "Urgência"
        ]
        if valor not in tipos_validos:
            raise AtendimentoInvalido(
                f"Tipo inválido. Escolha: {', '.join(tipos_validos)}.")
        return valor

    @staticmethod
    def status_atendimento(valor: str) -> str:
        """
        Valida o status do atendimento.
        Deve ser Realizado ou Em acompanhamento.
        """
        status_validos = ["Realizado", "Em acompanhamento"]
        if valor not in status_validos:
            raise AtendimentoInvalido(
                f"Status inválido. Use: {', '.join(status_validos)}.")
        return valor

    # ══════════════════════════════════════════════════════════
    # VALIDAÇÃO COMPLETA DE FORMULÁRIOS
    # ══════════════════════════════════════════════════════════

    @classmethod
    def formulario_paciente(cls, nome: str, data_nascimento: str,
                             telefone: str, email: str,
                             documento: str) -> dict:
        """
        Valida todos os campos do formulário de paciente de uma vez.
        Retorna um dicionário com os valores validados e limpos,
        ou lança AtendimentoInvalido com a mensagem do primeiro erro.
        """
        return {
            "nome":             cls.nome(nome),
            "data_nascimento":  cls.data_nascimento(data_nascimento),
            "telefone":         cls.telefone(telefone),
            "email":            cls.email(email),
            "documento":        cls.documento(documento),
        }

    @classmethod
    def formulario_atendimento(cls, paciente_id: int, data: str,
                                tipo: str, status: str) -> dict:
        """
        Valida todos os campos do formulário de atendimento de uma vez.
        Retorna um dicionário com os valores validados e limpos,
        ou lança AtendimentoInvalido com a mensagem do primeiro erro.
        """
        if not paciente_id:
            raise AtendimentoInvalido("Selecione um paciente.")
        return {
            "paciente_id": paciente_id,
            "data":        cls.data_atendimento(data),
            "tipo":        cls.tipo_atendimento(tipo),
            "status":      cls.status_atendimento(status),
        }


# ── Instância global ────────────────────────────────────────
validador = Validador()