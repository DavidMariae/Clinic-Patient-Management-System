import customtkinter as ctk  # Necessário para criar objetos CTkFont
from config import FONTE      # Importa o nome da fonte base definido no config

# ════════════════════════════════════════════════════════════════
# ctk.CTkFont() só pode ser criado DEPOIS que uma janela já existe.

# Se tentarmos criar fontes no config.py (que é importado antes
# da janela existir), o Python levanta este erro:
#   RuntimeError: Too early to use font: no default root window

# A solução é criar fontes sob demanda — só quando chamadas,
# o que sempre acontece depois da janela estar ativa.
# ════════════════════════════════════════════════════════════════

# Dicionário que funciona como cache de fontes já criadas
# Chave: (tamanho, peso) | Valor: objeto CTkFont
# Evita criar a mesma fonte várias vezes — economia de memória
_cache: dict = {}


def font(size: int, weight: str = "normal") -> ctk.CTkFont:
    """
    Função central de criação de fontes.
    Retorna uma CTkFont cacheada — cria apenas uma vez por combinação.

    Parâmetros:
        size   → tamanho em pontos (ex: 13, 22)
        weight → "normal" ou "bold"

    Exemplo de uso:
        ctk.CTkLabel(parent, font=F.font(13, "bold"))
    """
    chave = (size, weight)  # Tupla usada como chave única no cache

    # Se esta combinação ainda não foi criada, cria e guarda no cache
    if chave not in _cache:
        _cache[chave] = ctk.CTkFont(family=FONTE, size=size, weight=weight)

    # Retorna a fonte — seja recém-criada ou a que já estava no cache
    return _cache[chave]


# ════════════════════════════════════════════════════════════════
# ATALHOS SEMÂNTICOS
# Em vez de chamar F.font(22, "bold") em todo lugar,usa nomes que descrevem o propósito da fonte.
# Exemplo: F.titulo() é mais fácil de padronizar que F.font(22, "bold")
# ════════════════════════════════════════════════════════════════

# — Textos estruturais —
def titulo():        return font(22, "bold")   # Título principal de cada tela
def subtitulo():     return font(15, "bold")   # Título de seção dentro de card
def secao():         return font(10, "bold")   # Rótulo de seção em maiúsculas
def label():         return font(11, "bold")   # Label de campo de formulário

# — Textos de conteúdo —
def corpo():         return font(13)           # Texto geral — campos, tabelas
def corpo_bold():    return font(13, "bold")   # Texto geral em negrito
def pequena():       return font(12)           # Textos menores
def pequena_bold():  return font(12, "bold")   # Textos menores em negrito
def mini():          return font(11)           # Textos pequenos
def mini_bold():     return font(11, "bold")   # Textos pequenos em negrito
def micro():         return font(10)           # Textos mínimos
def micro_bold():    return font(10, "bold")   # Textos mínimos em negrito

# — Componentes específicos da interface —
def nav():           return font(13)           # Itens do menu lateral
def logo():          return font(14, "bold")   # Nome "Pantokrátor" no header
def logo_sub():      return font(10)           # Subtítulo do logo ("Gestão de...")
def avatar():        return font(11, "bold")   # Iniciais dentro do círculo do avatar

# — Cards do dashboard —
def card_valor():    return font(28, "bold")   # Número grande (ex: "128 pacientes")
def card_label():    return font(12)           # Rótulo abaixo do número

# — Botões —
def btn():           return font(13)           # Botão padrão
def btn_bold():      return font(13, "bold")   # Botão de ação principal
def btn_pequeno():   return font(12, "bold")   # Botão pequeno dentro de tabelas

# — Tabelas —
def tabela_head():   return font(11, "bold")   # Cabeçalho da coluna
def tabela_body():   return font(13)           # Conteúdo da célula
def tabela_bold():   return font(13, "bold")   # Conteúdo da célula em negrito
def tabela_sub():    return font(11)           # Texto secundário na célula

# — Elementos especiais —
def pill():          return font(11, "bold")   # Pills de status (Realizado, Em acompanhamento)
def badge():         return font(12, "bold")   # Badge contador (ex: "12 pacientes")
def feedback():      return font(12)           # Mensagens de sucesso e erro nos formulários