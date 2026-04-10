# ════════════════════════════════════════════════════════════════
# Este arquivo transforma a pasta "models" em um pacote Python.
# Sem ele, o Python não reconhece a pasta como módulo importável.

# Por que fazer os imports aqui?
# Permite importar os models de forma mais curta:

#   Com __init__.py:    from src.models import Paciente
#   Sem __init__.py:    from src.models.paciente import Paciente

# É uma conveniência — centraliza os imports públicos do pacote.
# Estudar melhor isso...
# ════════════════════════════════════════════════════════════════

from .paciente    import Paciente     # O ponto indica importação relativa (dentro do pacote)
from .atendimento import Atendimento  # Mesma lógica — importa da pasta atual