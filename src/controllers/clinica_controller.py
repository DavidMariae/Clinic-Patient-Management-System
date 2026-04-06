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
        # 1. Carrega os dados brutos
        pacientes = self.obter_todos_pacientes()
        atendimentos = Database.ler_dados(
            PATH_ATENDIMENTOS
        )  # Use o caminho correto do seu JSON

        # 2. Calcula atendimentos de hoje
        hoje = datetime.now().strftime("%d/%m/%Y")
        atendimentos_hoje = [a for a in atendimentos if a.get("data") == hoje]

        return {
            "total_pacientes": len(pacientes),
            "total_atendimentos": len(atendimentos),
            "atendimentos_hoje": len(atendimentos_hoje),
            "lista_recente": atendimentos[-5:],  # Pega os últimos 5 para a tabela
        }

    def obter_todos_pacientes(self):
        """Retorna a lista completa de objetos Paciente vindos do JSON"""
        dados = Database.ler_dados(PATH_PACIENTES)
        if not dados:
            return []
        return [Paciente.from_dict(p) for p in dados]

    def obter_todos_atendimentos(self):
        # Retorna a lista completa do JSON ou uma lista vazia se não existir
        atendimentos = Database.ler_dados(PATH_ATENDIMENTOS)
        return atendimentos[::-1]  # Retorna do mais recente para o mais antigo

    def buscar_pacientes(self, termo):
        """Filtra pacientes por nome ou telefone"""
        termo = termo.lower()
        todos = self.obter_todos_pacientes()
        return [p for p in todos if termo in p.nome.lower() or termo in p.telefone]

    def excluir_paciente(self, paciente_id):
        """Remove um paciente pelo ID e salva o arquivo novamente"""
        pacientes = Database.ler_dados(PATH_PACIENTES)
        # Cria uma nova lista sem o paciente que queremos deletar
        pacientes_atualizados = [p for p in pacientes if p["id"] != paciente_id]

        Database.salvar_dados(PATH_PACIENTES, pacientes_atualizados)
        return True

    def obter_nomes_pacientes(self):
        # Retorna uma lista de strings formatadas: 'Nome (ID)'
        pacientes = self.obter_todos_pacientes()
        return [f"{p.nome} (ID: {p.id})" for p in pacientes]

    def salvar_atendimento(self, dados_atendimento):
        # Carrega a lista atual, adiciona o novo e salva no atendimentos.json
        atendimentos = Database.ler_dados(PATH_ATENDIMENTOS)
        atendimentos.append(dados_atendimento)
        Database.salvar_dados(PATH_ATENDIMENTOS, atendimentos)
        return True

    def filtrar_atendimentos_por_paciente(self, paciente_id):
        # Carrega todos os atendimentos do JSON
        todos_atendimentos = Database.ler_dados(PATH_ATENDIMENTOS)

        # Filtra mantendo apenas os que batem com o ID do paciente
        # Convertemos para string para garantir a comparação correta
        historico = [
            a
            for a in todos_atendimentos
            if str(a.get("paciente_id")) == str(paciente_id)
        ]

        # Retorna do mais recente para o mais antigo
        return historico[::-1]
