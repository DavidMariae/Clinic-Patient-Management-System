import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from database import (
    listar_pacientes, salvar_paciente,
    listar_atendimentos, salvar_atendimento,
    atualizar_paciente, atualizar_atendimento,
    deletar_paciente, deletar_atendimento,
    listar_usuarios, salvar_usuario
)
from src.models.paciente import Paciente
from src.models.atendimento import Atendimento
from exceptions import PacienteNaoEncontrado, AtendimentoInvalido
from datetime import date


class ClinicaController:
    """
    Controlador principal da clínica.
    Centraliza todas as regras de negócio da aplicação.
    Utiliza Programação Orientada a Objetos (POO).
    """

    # ══════════════════════════════════════════════════════════
    # UTILITÁRIOS PRIVADOS
    # ══════════════════════════════════════════════════════════

    @staticmethod
    def _proximo_id(lista: list) -> int:
        """Gera o próximo ID disponível baseado na lista atual."""
        if not lista:
            return 1
        return max(item["id"] for item in lista) + 1

    @staticmethod
    def _formatar_data_iso(data_br: str) -> str:
        """
        Converte data do formato brasileiro DD/MM/AAAA
        para o formato ISO AAAA-MM-DD usado no JSON.
        """
        try:
            d, m, a = data_br.strip().split("/")
            return f"{a}-{m.zfill(2)}-{d.zfill(2)}"
        except Exception:
            return data_br.strip()

    @staticmethod
    def _formatar_data_br(data_iso: str) -> str:
        """
        Converte data do formato ISO AAAA-MM-DD
        para o formato brasileiro DD/MM/AAAA para exibição.
        """
        try:
            a, m, d = data_iso.strip().split("-")
            return f"{d}/{m}/{a}"
        except Exception:
            return data_iso.strip()

    # ══════════════════════════════════════════════════════════
    # PACIENTES
    # ══════════════════════════════════════════════════════════

    def cadastrar_paciente(self, nome: str, data_nascimento: str,
                           telefone: str, email: str,
                           documento: str) -> Paciente:
        """
        Valida os dados e cadastra um novo paciente.
        Retorna o objeto Paciente criado.
        """
        self._validar_paciente(nome, data_nascimento, telefone, documento)

        pacientes = listar_pacientes()
        novo_id   = self._proximo_id(pacientes)

        # Converte data para ISO antes de salvar (formato internacional)
        data_iso = self._formatar_data_iso(data_nascimento)

        p = Paciente(
            id=novo_id,
            nome=nome.strip(),
            data_nascimento=data_iso,
            telefone=telefone.strip(),
            email=email.strip(),
            documento=documento.strip()
        )
        salvar_paciente(p.to_dict())
        return p

    def obter_pacientes(self) -> list:
        """Retorna todos os pacientes cadastrados."""
        return listar_pacientes()

    def obter_paciente_por_id(self, paciente_id: int) -> dict:
        """
        Busca e retorna um paciente pelo ID.
        Lança PacienteNaoEncontrado se não existir.
        """
        for p in listar_pacientes():
            if p["id"] == paciente_id:
                return p
        raise PacienteNaoEncontrado(
            f"Paciente com ID {paciente_id} não encontrado.")

    def buscar_pacientes(self, termo: str) -> list:
        """
        Busca pacientes por nome ou telefone.
        A busca é case-insensitive e parcial.
        """
        termo = termo.lower().strip()
        if not termo:
            return listar_pacientes()
        return [
            p for p in listar_pacientes()
            if termo in p.get("nome", "").lower()
            or termo in p.get("telefone", "")
        ]

    def atualizar_paciente(self, paciente_id: int, **campos) -> dict:
        """
        Atualiza campos de um paciente existente.
        Apenas os campos passados como kwargs são alterados.
        """
        paciente = self.obter_paciente_por_id(paciente_id)

        # Converte data se vier no formato BR
        if "data_nascimento" in campos:
            campos["data_nascimento"] = self._formatar_data_iso(
                campos["data_nascimento"])

        paciente.update(campos)
        atualizar_paciente(paciente)
        return paciente

    def deletar_paciente(self, paciente_id: int) -> None:
        """
        Remove um paciente e todos os seus atendimentos.
        Valida a existência antes de deletar.
        """
        self.obter_paciente_por_id(paciente_id)
        deletar_paciente(paciente_id)
        # Remove também todos os atendimentos do paciente
        todos = listar_atendimentos()
        for atend in todos:
            if atend.get("paciente_id") == paciente_id:
                deletar_atendimento(atendimento_id=atend["id"])

    # ══════════════════════════════════════════════════════════
    # USUÁRIOS
    # ══════════════════════════════════════════════════════════

    def cadastrar_usuario(self, nome: str, usuario: str,
                       senha: str, nivel: str) -> dict:
        """Valida e cadastra um novo usuário."""
        if not nome.strip():
            raise AtendimentoInvalido("Nome é obrigatório.")
        if not usuario.strip():
            raise AtendimentoInvalido("Usuário é obrigatório.")
        if len(senha) < 6:
            raise AtendimentoInvalido("Senha deve ter no mínimo 6 caracteres.")
        if nivel not in ["Administrador", "Recepcionista", "Médico"]:
            raise AtendimentoInvalido("Nível de acesso inválido.")

        usuarios = listar_usuarios()

        # Verifica se usuário já existe
        if any(u["usuario"].lower() == usuario.lower() for u in usuarios):
            raise AtendimentoInvalido("Este nome de usuário já está em uso.")

        novo_id = self._proximo_id(usuarios)
        novo    = {
            "id":      novo_id,
            "nome":    nome.strip(),
            "usuario": usuario.strip().lower(),
            "senha":   senha,
            "nivel":   nivel
        }
        salvar_usuario(novo)
        return novo

    def autenticar(self, usuario: str, senha: str) -> dict:
        """
        Valida credenciais de login.
        Retorna o usuário autenticado ou lança exceção.
        """
        if not usuario.strip() or not senha.strip():
            raise AtendimentoInvalido("Preencha usuário e senha.")

        usuarios = listar_usuarios()
        for u in usuarios:
            if u["usuario"].lower() == usuario.lower().strip() \
                    and u["senha"] == senha:
                return u

        raise AtendimentoInvalido("Usuário ou senha incorretos.")

    # ══════════════════════════════════════════════════════════
    # ATENDIMENTOS
    # ══════════════════════════════════════════════════════════

    def registrar_atendimento(self, paciente_id: int, data: str,
                               tipo: str, observacoes: str,
                               status: str) -> Atendimento:
        """
        Valida e registra um novo atendimento.
        Retorna o objeto Atendimento criado.
        """
        self._validar_atendimento(paciente_id, data, tipo, status)

        # Garante que o paciente existe
        self.obter_paciente_por_id(paciente_id)

        atendimentos = listar_atendimentos()
        novo_id      = self._proximo_id(atendimentos)

        # Converte data para ISO antes de salvar
        data_iso = self._formatar_data_iso(data) if "/" in data else data.strip()

        a = Atendimento(
            id=novo_id,
            paciente_id=paciente_id,
            data=data_iso,
            tipo=tipo.strip(),
            observacoes=observacoes.strip(),
            status=status.strip()
        )
        salvar_atendimento(a.to_dict())
        return a

    def obter_todos_atendimentos(self) -> list:
        """
        Retorna todos os atendimentos ordenados
        do mais recente para o mais antigo.
        """
        return sorted(
            listar_atendimentos(),
            key=lambda a: a.get("data", ""),
            reverse=True
        )

    def obter_atendimentos_do_paciente(self, paciente_id: int) -> list:
        """
        Retorna todos os atendimentos de um paciente
        ordenados do mais recente para o mais antigo.
        """
        return sorted(
            [a for a in listar_atendimentos()
             if a.get("paciente_id") == paciente_id],
            key=lambda a: a.get("data", ""),
            reverse=True
        )

    def obter_atendimentos_hoje(self) -> list:
        """Retorna os atendimentos do dia atual."""
        hoje = date.today().strftime("%Y-%m-%d")
        return [a for a in listar_atendimentos()
                if a.get("data") == hoje]

    def atualizar_atendimento(self, atendimento_id: int, **campos) -> dict:
        """
        Atualiza campos de um atendimento existente.
        Lança AtendimentoInvalido se não encontrar.
        """
        for a in listar_atendimentos():
            if a["id"] == atendimento_id:
                if "data" in campos and "/" in campos["data"]:
                    campos["data"] = self._formatar_data_iso(campos["data"])
                a.update(campos)
                atualizar_atendimento(a)
                return a
        raise AtendimentoInvalido(
            f"Atendimento com ID {atendimento_id} não encontrado.")

    # ══════════════════════════════════════════════════════════
    # DASHBOARD
    # ══════════════════════════════════════════════════════════

    def obter_resumo_dashboard(self) -> dict:
        """
        Retorna um dicionário com os dados
        resumidos para exibição no dashboard.
        """
        pacientes    = listar_pacientes()
        atendimentos = listar_atendimentos()
        hoje         = date.today().strftime("%Y-%m-%d")

        total_pacientes    = len(pacientes)
        total_atendimentos = len(atendimentos)
        atendimentos_hoje  = sum(
            1 for a in atendimentos if a.get("data") == hoje)
        em_acompanhamento  = sum(
            1 for a in atendimentos
            if "acompanhamento" in a.get("status", "").lower())

        return {
            "total_pacientes":    total_pacientes,
            "total_atendimentos": total_atendimentos,
            "atendimentos_hoje":  atendimentos_hoje,
            "em_acompanhamento":  em_acompanhamento,
        }

    # ══════════════════════════════════════════════════════════
    # VALIDAÇÕES PRIVADAS
    # ══════════════════════════════════════════════════════════

    @staticmethod
    def _validar_paciente(nome: str, data_nascimento: str,
                           telefone: str, documento: str) -> None:
        """Valida os campos obrigatórios do paciente."""
        if not nome or not nome.strip():
            raise AtendimentoInvalido("Nome do paciente é obrigatório.")
        if len(nome.strip()) < 3:
            raise AtendimentoInvalido(
                "Nome deve ter pelo menos 3 caracteres.")
        if not data_nascimento or not data_nascimento.strip():
            raise AtendimentoInvalido("Data de nascimento é obrigatória.")
        if not telefone or not telefone.strip():
            raise AtendimentoInvalido("Telefone é obrigatório.")
        if not documento or not documento.strip():
            raise AtendimentoInvalido("Documento é obrigatório.")

    @staticmethod
    def _validar_atendimento(paciente_id: int, data: str,
                              tipo: str, status: str) -> None:
        """Valida os campos obrigatórios do atendimento."""
        if not paciente_id:
            raise AtendimentoInvalido("Paciente não selecionado.")
        if not data or not data.strip():
            raise AtendimentoInvalido("Data do atendimento é obrigatória.")
        if not tipo or not tipo.strip():
            raise AtendimentoInvalido("Tipo do atendimento é obrigatório.")
        status_validos = ("Realizado", "Em acompanhamento")
        if status not in status_validos:
            raise AtendimentoInvalido(
                f"Status inválido. Use: {', '.join(status_validos)}.")


# ── Instância global — padrão Singleton simples ─────────────
controller = ClinicaController()