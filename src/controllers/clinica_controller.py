import os
from datetime import datetime
from database import Database
from config import PATH_PACIENTES, PATH_ATENDIMENTOS
from src.models.paciente import Paciente
from src.models.atendimento import Atendimento


class ClinicaController:
    def __init__(self):
        # O Controller garante que o sistema de arquivos esteja pronto ao iniciar
        Database.inicializar_sistema()

    # --- LÓGICA DE PACIENTES ---
    def cadastrar_paciente(self, dados):
        """
        Recebe um dicionário de dados da View, transforma em Objeto e salva via Database.
        """
        pacientes_dados = Database.ler_dados(PATH_PACIENTES)

        # Geração de ID automático: busca o maior ID existente e soma 1
        novo_id = 1
        if pacientes_dados:
            novo_id = max(p["id"] for p in pacientes_dados) + 1

        # Criação do objeto de modelo para garantir a estrutura correta
        novo_paciente = Paciente(
            id=novo_id,
            nome=dados["nome"],
            data_nasc=dados["nasc"],
            telefone=dados["tel"],
            email=dados["email"],
            documento=dados["doc"],
        )

        # Converte para dicionário antes de enviar ao Banco (que só entende JSON)
        pacientes_dados.append(novo_paciente.to_dict())
        Database.salvar_dados(PATH_PACIENTES, pacientes_dados)

        return novo_paciente

    def listar_todos_pacientes(self):
        """Converte a lista 'burra' do JSON em uma lista de objetos Paciente."""
        dados = Database.ler_dados(PATH_PACIENTES)
        return [Paciente.from_dict(p) for p in dados]

    def buscar_paciente(self, termo):
        """Filtra pacientes por nome ou documento de forma case-insensitive."""
        termo = termo.lower()
        todos = self.listar_todos_pacientes()
        return [p for p in todos if termo in p.nome.lower() or termo in p.documento]

    # --- LÓGICA DE ATENDIMENTOS ---
    def registrar_atendimento(self, paciente_id, tipo, observacoes):
        """Registra uma nova atividade médica vinculada a um paciente."""
        atendimentos_dados = Database.ler_dados(PATH_ATENDIMENTOS)

        novo_id = 1
        if atendimentos_dados:
            novo_id = max(a["id"] for a in atendimentos_dados) + 1

        # Uso do datetime.now() para horário local (ideal para clínicas regionais)
        data_hoje = datetime.now().strftime("%d/%m/%Y")

        novo_atendimento = Atendimento(
            id=novo_id,
            paciente_id=paciente_id,
            data=data_hoje,
            tipo=tipo,
            observacoes=observacoes,
        )

        atendimentos_dados.append(novo_atendimento.to_dict())
        Database.salvar_dados(PATH_ATENDIMENTOS, atendimentos_dados)

        return novo_atendimento

    # --- LÓGICA DO DASHBOARD ---
    def buscar_estatisticas(self):
        """Calcula os números para os cards do Dashboard em tempo real."""
        pacientes = Database.ler_dados(PATH_PACIENTES)
        atendimentos = Database.ler_dados(PATH_ATENDIMENTOS)

        hoje = datetime.now().strftime("%d/%m/%Y")
        atendimentos_hoje = [a for a in atendimentos if a["data"] == hoje]

        return {
            "total_pacientes": len(pacientes),
            "total_atendimentos": len(atendimentos),
            "atendimentos_hoje": len(atendimentos_hoje),
        }
