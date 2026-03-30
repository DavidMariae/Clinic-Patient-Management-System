"""
O objetivo é que a Interface (UI) não deve saber como salvar no arquivo JSON, e o Banco de Dados não deve saber o que é um "Paciente", por exemplo.
O Controller fica no meio, recebendo as ordens da tela e usando a classe Database para executar.
"""

from database import Database
from config import PATH_PACIENTES, PATH_ATENDIMENTOS
from src.models.paciente import Paciente
from src.models.atendimento import Atendimento
from datetime import datetime


class ClinicaController:
    def __init__(self):
        # Garante que os arquivos existam ao iniciar
        Database.inicializar_sistema()

    # --- LÓGICA DE PACIENTES ---
    def cadastrar_paciente(self, nome, data_nasc, telefone, email, documento):
        pacientes_dados = Database.ler_dados(PATH_PACIENTES)

        # Gerar ID automático (Pega o último ID + 1)
        novo_id = pacientes_dados[-1]["id"] + 1 if pacientes_dados else 1

        novo_paciente = Paciente(novo_id, nome, data_nasc, telefone, email, documento)
        pacientes_dados.append(novo_paciente.to_dict())

        Database.salvar_dados(PATH_PACIENTES, pacientes_dados)
        return novo_paciente

    def listar_todos_pacientes(self):
        dados = Database.ler_dados(PATH_PACIENTES)
        return [Paciente.from_dict(p) for p in dados]

    def buscar_paciente(self, termo):
        """Busca por nome ou documento"""
        termo = termo.lower()
        todos = self.listar_todos_pacientes()
        return [p for p in todos if termo in p.nome.lower() or termo in p.documento]

    # --- LÓGICA DE ATENDIMENTOS ---
    def registrar_atendimento(self, paciente_id, tipo, observacoes):
        atendimentos_dados = Database.ler_dados(PATH_ATENDIMENTOS)

        novo_id = atendimentos_dados[-1]["id"] + 1 if atendimentos_dados else 1
        data_hoje = datetime.now().strftime(
            "%d/%m/%Y"
        )  # cria um objeto que retorna a data e a hora local... .utcnow()?

        novo_atendimento = Atendimento(
            novo_id, paciente_id, data_hoje, tipo, observacoes
        )
        atendimentos_dados.append(novo_atendimento.to_dict())

        Database.salvar_dados(PATH_ATENDIMENTOS, atendimentos_dados)
        return novo_atendimento

    # --- LÓGICA DO DASHBOARD ---
    def buscar_estatisticas(self):
        pacientes = Database.ler_dados(PATH_PACIENTES)
        atendimentos = Database.ler_dados(PATH_ATENDIMENTOS)

        hoje = datetime.now().strftime("%d/%m/%Y")
        atendimentos_hoje = [a for a in atendimentos if a["data"] == hoje]

        return {
            "total_pacientes": len(pacientes),
            "total_atendimentos": len(atendimentos),
            "atendimentos_hoje": len(atendimentos_hoje),
        }
