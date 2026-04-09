import os                                  # Módulo padrão do Python para interagir com o sistema operacional
import customtkinter as ctk                # Biblioteca de interface gráfica moderna, baseada no Tkinter

# ── Caminhos ────────────────────────────────────────────────
# "GPS" do sistema. Se mudar a pasta de lugar, se atualiza sozinho. Estudar mais isso

# Descobre o caminho ABSOLUTO da pasta onde este arquivo (config.py) está
# __file__ → caminho do script atual
# os.path.abspath() → transforma em caminho absoluto completo
# os.path.dirname() → pega só a pasta pai, removendo o nome do arquivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Une BASE_DIR com "data" para formar o caminho da pasta de dados
# os.path.join() garante que o separador correto seja usado
# (barra \ no Windows, / no Linux/Mac)
DATA_DIR   = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Caminhos completos para cada arquivo JSON de persistência
# Usar variáveis evita repetir strings espalhadas pelo código
PACIENTES_FILE    = os.path.join(DATA_DIR, "pacientes.json")
ATENDIMENTOS_FILE = os.path.join(DATA_DIR, "atendimentos.json")
USUARIOS_FILE     = os.path.join(DATA_DIR, "usuarios.json")

NIVEIS_ACESSO = ["Administrador", "Recepcionista", "Médico"]

# ── Janela ──────────────────────────────────────────────────
APP_TITLE         = "Pantokrátor — Gestão de Atendimentos"
APP_GEOMETRY      = "1100x660"
APP_MIN_WIDTH     = 900
APP_MIN_HEIGHT    = 580
SIDEBAR_WIDTH     = 220

# ── Tema ────────────────────────────────────────────────────
# "light" = fundo claro | "dark" = fundo escuro | "system" = segue o SO
APPEARANCE_MODE   = "light"

# Tema de cores padrão do CustomTkinter — usado como base antes das cores personalizadas sobrescreverem o visual
COLOR_THEME       = "blue"

# ── Logo ────────────────────────────────────────────────────
LOGO = "✛"
'''☨ ✛ ✠'''

# ── Paleta Bizantina ────────────────────────────────────────
# Azuis
AZUL_PROFUNDO     = "#0D2347"   # fundo sidebar escuro
AZUL_ESCURO       = "#1A3A6B"   # sidebar principal
AZUL_MEDIO        = "#2A5298"   # hover sidebar
AZUL_CLARO        = "#5A7BAA"   # texto muted sidebar
AZUL_PALE         = "#E8F0FB"   # fundo pale / badges

# Dourados
DOURADO_FORTE     = "#C9A84C"   # destaque principal
DOURADO_CLARO     = "#E8D5A0"   # texto sobre fundo escuro
DOURADO_PALE      = "#FDF6E3"   # fundo suave dourado
DOURADO_BORDA     = "#D4B86A"   # bordas douradas

# Fundos
FUNDO_APP         = "#F0EDFF"   # fundo geral levemente lilás-azulado
FUNDO_INPUT       = "#F8F7FE"   # fundo campos
FUNDO_ALT         = "#F5F4FB"   # linhas alternadas tabela
BRANCO            = "#FFFFFF"
BORDA             = "#DDD8F0"   # bordas gerais

# Textos
TEXTO_TITULO      = "#0D2347"   # títulos principais
TEXTO_BODY        = "#2C3A5A"   # texto geral
TEXTO_MUTED       = "#7A8BA8"   # texto secundário

# Semânticas
VERDE_BG          = "#EAF3DE"
VERDE_TEXT        = "#3B6D11"
AMBER_BG          = "#FDF3DC"
AMBER_TEXT        = "#8A5C00"
TEAL_BG           = "#E1F5EE"
TEAL_TEXT         = "#0F6E56"
ERRO_BG           = "#FDECEA"
ERRO_TEXT         = "#B91C1C"

# ── Tipografia ──────────────────────────────────────────────
# Fontes são criadas sob demanda em src/ui/fonts.py
# Aqui ficam apenas os tamanhos e o nome da fonte base

FONTE             = "Arial"

TAM_TITULO        = 22
TAM_SUBTITULO     = 15
TAM_SECAO         = 10
TAM_LABEL         = 11
TAM_CORPO         = 13
TAM_PEQUENA       = 12
TAM_MINI          = 11
TAM_MICRO         = 10

# ── Bordas e raios ──────────────────────────────────────────
# corner_radius define o quanto as bordas são arredondadas (em pixels)

RAIO_CARD         = 14
RAIO_BTN          = 8
RAIO_INPUT        = 8
RAIO_PILL         = 20
RAIO_AVATAR       = 20
RAIO_ICONE        = 10

# ── Tamanhos ────────────────────────────────────────────────
# Alturas fixas garantem consistência visual em toda a aplicação


ALTURA_INPUT      = 38
ALTURA_BTN        = 36
ALTURA_BTN_SMALL  = 28
ALTURA_BTN_NAV    = 36
ALTURA_TOPBAR_BTN = 34

# ── Espaçamentos ────────────────────────────────────────────
# Paddings usados para manter consistência entre as telas
PAD_LATERAL       = 28
PAD_CARD          = 22
PAD_TOPO          = 22

# ── Paginação ────────────────────────────────────────────────
ITENS_POR_PAGINA  = 8  # Quantidade de linhas exibidas por vez nas tabelas