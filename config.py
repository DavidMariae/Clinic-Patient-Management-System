import os

# "GPS" do sistema. Se mudar a pasta de lugar, se atualiza sozinho. Não entendi bem

# Descobre o caminho da pasta onde este arquivo (config.py) está
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# os.path.abspath(__file__) retorna o caminho absoluto completo (do diretório raiz) de arquivo Python que está sendo executado atualmente.
# (__file__) é variável especial que contém o caminho do script atual
# os.path.dirname Pega o caminho e extrai apenas a pasta pai, removendo o nome do arquivo

# Define o caminho da pasta 'data' e 'assets'
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
# os.path.join Une um ou mais segmentos de caminho, criando um único caminho válido
# independente do sistema operacional

# Define o caminho completo para os arquivos JSON
PATH_PACIENTES = os.path.join(DATA_DIR, "pacientes.json")
PATH_ATENDIMENTOS = os.path.join(DATA_DIR, "atendimentos.json")

# --- DEFINIÇÕES DE UI (INTERFACE) ---
LARGURA_JANELA = 1200
ALTURA_JANELA = 750
LARGURA_MENU = 240

# Cores
COR_FUNDO = "#EBEBEB"
COR_SIDEBAR = "#212121"
COR_CARD = "#FFFFFF"
COR_TEXTO_DARK = "#1A1A1A"
COR_TEXTO_LIGHT = "#FFFFFF"
COR_PRINCIPAL = "#24a0ed"
COR_SUCESSO = "#2ecc71"
COR_AVISO = "#f1c40f"
COR_PERIGO = "#e74c3c"
COR_BOTAO_HOVER_SIDEBAR = "#333333"

# Cores para Status Pills (Tabela)
COR_STATUS_REALIZADO = "#a8e6cf"
COR_STATUS_REALIZADO_TEXT = "#1b5e20"
COR_STATUS_ACOMPANHAMENTO = "#ffecb3"
COR_STATUS_ACOMPANHAMENTO_TEXT = "#5d4037"

# Fontes e Tamanhos
FONTE_FAMILIA = "Segoe UI"  # Fonte padrão moderna do Windows
FONTE_H1 = (FONTE_FAMILIA, 28, "bold")
FONTE_H2 = (FONTE_FAMILIA, 20, "bold")
FONTE_CORPO = (FONTE_FAMILIA, 14)
FONTE_CARD_VALOR = (FONTE_FAMILIA, 34, "bold")
FONTE_PILL = (FONTE_FAMILIA, 12, "bold")

# --- ESTILOS CTK ---
TEMA_APARENCIA = "System"  # Light, Dark, System
TEMA_COR = "blue"  # blue, green, dark-blue
