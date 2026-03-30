import json
import os
from config import DATA_DIR, PATH_PACIENTES, PATH_ATENDIMENTOS


# Criando uma classe que cuida de verificar se a pasta e os arquivos existem. Se não existirem, ela os cria vazios para o programa não dar erro ao abrir.
class Database:
    @staticmethod
    def inicializar_sistema():
        """Cria a pasta e os arquivos iniciais caso não existam."""

        # 1. Cria a pasta 'data' se ela não existir
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            print(f"Pasta criada: {DATA_DIR}")

        # 2. Cria os arquivos JSON com uma lista vazia []
        for arquivo in [PATH_PACIENTES, PATH_ATENDIMENTOS]:
            if not os.path.exists(arquivo):
                with open(arquivo, "w", encoding="utf-8") as f:
                    json.dump([], f, ensure_ascii=False, indent=4)
                print(f"Arquivo criado: {os.path.basename(arquivo)}")

    @staticmethod
    def salvar_dados(caminho, dados):
        """Salva uma lista de dicionários no arquivo JSON especificado."""
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

    @staticmethod
    def ler_dados(caminho):
        """Lê os dados de um arquivo JSON e retorna uma lista."""
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
