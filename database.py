import json  # Módulo padrão do Python para ler e escrever arquivos JSON
import os    # Módulo para verificar se arquivos existem no sistema

# Importa os caminhos dos arquivos definidos centralmente no config
# Se mudar o nome ou local dos arquivos, muda só no config
from config import PACIENTES_FILE, ATENDIMENTOS_FILE, USUARIOS_FILE


# O "_" no início indica que são funções internas
# Não devem ser chamadas diretamente de fora deste arquivo

def _ler(arquivo):
    """
    Lê um arquivo JSON e retorna seu conteúdo como lista Python.
    Se o arquivo não existir, retorna lista vazia (não gera erro).
    """

    # Retornar [] ao invés de lançar erro porque na primeira execução os arquivos ainda não existem.
    # O sistema precisa funcionar mesmo sem dados anteriores.
    
    if not os.path.exists(arquivo):
        # Arquivo ainda não existe: sistema rodando pela primeira vez
        return []
    # Sem especificar encoding, o Windows pode usar cp1252 e corromper os dados
    with open(arquivo, "r", encoding="utf-8") as f:
        return json.load(f)   # Converte o JSON em lista de dicionários Python

def _salvar(arquivo, dados):
    """
    Sobrescreve o arquivo JSON com os dados fornecidos."""

    # Sobrescreve tudo ao invés de só adicionar porque JSON não suporta append de forma simples
    # Abordagem mais segura: ler → modificar → salvar tudo
    # Pode se tornar um problema dependendo do volume de dados da aplicação
    
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(
            dados, f,
            ensure_ascii=False,  # Preserva acentos — sem isso "João" viraria "Jo\u00e3o"
            indent=2             # Indenta o JSON — facilita leitura manual do arquivo
        )

# ── Pacientes ───────────────────────────────────────────────
def listar_pacientes() -> list:
    """Retorna todos os pacientes cadastrados como lista de dicionários."""
    return _ler(PACIENTES_FILE)


def salvar_paciente(paciente_dict: dict) -> None:
    """
    Adiciona um novo paciente ao arquivo JSON.
    Lê a lista atual, adiciona o novo e salva tudo de volta.
    """
    dados = _ler(PACIENTES_FILE)    # Carrega os existentes
    dados.append(paciente_dict)     # Adiciona o novo ao final
    _salvar(PACIENTES_FILE, dados)  # Salva a lista atualizada


def atualizar_paciente(paciente_dict: dict) -> None:
    """
    Substitui o paciente com o mesmo ID pelo novo dicionário
    Usa list comprehension para reconstruir a lista trocando só o alterado

    Como funciona:
    Para cada paciente p na lista:
        - Se p["id"] == o id do alterado → usa o novo dicionário
        - Caso contrário → mantém o original
    """
    dados = _ler(PACIENTES_FILE)
    dados = [
        paciente_dict if p["id"] == paciente_dict["id"] else p
        for p in dados
    ]
    _salvar(PACIENTES_FILE, dados)


def deletar_paciente(paciente_id: int) -> None:
    """
    Remove o paciente com o ID especificado
    Usa list comprehension para manter apenas os que NÃO têm aquele ID
    """
    dados = _ler(PACIENTES_FILE)
    dados = [p for p in dados if p["id"] != paciente_id]
    _salvar(PACIENTES_FILE, dados)

# ── Atendimentos ────────────────────────────────────────────
def listar_atendimentos() -> list:
    """Retorna todos os atendimentos registrados como lista de dicionários."""
    return _ler(ATENDIMENTOS_FILE)


def salvar_atendimento(atendimento_dict: dict) -> None:
    """Adiciona um novo atendimento ao arquivo JSON."""
    dados = _ler(ATENDIMENTOS_FILE)
    dados.append(atendimento_dict)
    _salvar(ATENDIMENTOS_FILE, dados)


def atualizar_atendimento(atendimento_dict: dict) -> None:
    """Substitui o atendimento com o mesmo ID pelo novo dicionário."""
    dados = _ler(ATENDIMENTOS_FILE)
    dados = [
        atendimento_dict if a["id"] == atendimento_dict["id"] else a
        for a in dados
    ]
    _salvar(ATENDIMENTOS_FILE, dados)


def deletar_atendimento(paciente_id: int = None, atendimento_id: int = None) -> None:
    """
    Remove atendimentos com base em um ou dois critérios:

    - paciente_id   → remove TODOS os atendimentos daquele paciente
                      (usado quando um paciente é excluído)
    - atendimento_id → remove UM atendimento específico
                      (usado na exclusão individual)
    """
    dados = _ler(ATENDIMENTOS_FILE)

    # Remove atendimentos do paciente (exclusão em cascata)
    if paciente_id is not None:
        dados = [a for a in dados if a.get("paciente_id") != paciente_id]

    # Remove um atendimento específico pelo seu próprio ID
    if atendimento_id is not None:
        dados = [a for a in dados if a["id"] != atendimento_id]

    _salvar(ATENDIMENTOS_FILE, dados)

# ── Usuários ────────────────────────────────────────────────
def listar_usuarios() -> list:
    """Retorna todos os usuários cadastrados como lista de dicionários."""
    return _ler(USUARIOS_FILE)


def salvar_usuario(usuario_dict: dict) -> None:
    """Adiciona um novo usuário ao arquivo JSON."""
    dados = _ler(USUARIOS_FILE)
    dados.append(usuario_dict)
    _salvar(USUARIOS_FILE, dados)