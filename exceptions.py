# ════════════════════════════════════════════════════════════════
# EXCEÇÕES CUSTOMIZADAS DO SISTEMA PANTOKRÁTOR

# Por que criar exceções próprias?

# O Python já tem exceções genéricas como ValueError e TypeError.
# Mas usar exceções específicas do domínio do sistema traz vantagens:

# 1. CLAREZA — "PacienteNaoEncontrado" é muito mais descritivo
#    do que um genérico "ValueError"

# 2. CONTROLE — podemos capturar apenas os erros que esperamos:
#    except PacienteNaoEncontrado → trata só este caso
#    except Exception → pegaria qualquer erro, inclusive bugs

# 3. SEMÂNTICA — o nome da exceção já documenta o que deu errado
# ════════════════════════════════════════════════════════════════


class PacienteNaoEncontrado(Exception):
    """
    Levantada quando buscamos um paciente pelo ID e ele não existe.

    Exemplo de uso no controller:
        raise PacienteNaoEncontrado(f"Paciente {id} não encontrado.")

    Exemplo de captura na view:
        try:
            controller.obter_paciente_por_id(42)
        except PacienteNaoEncontrado as e:
            print(e)  # "Paciente 42 não encontrado."
    """
    pass  # Herda tudo da classe Exception — só o nome muda


class AtendimentoInvalido(Exception):
    """
    Levantada quando dados de um formulário são inválidos
    ou quando uma operação não pode ser realizada.

    Usada tanto para erros de validação de campos
    (nome vazio, data no formato errado)
    quanto para erros de regra de negócio
    (usuário já existe, status inválido).

    Exemplo de uso no validador:
        if not nome.strip():
            raise AtendimentoInvalido("Nome é obrigatório.")

    Exemplo de captura na view:
        try:
            validador.nome(campo.get())
        except AtendimentoInvalido as e:
            label_erro.configure(text=str(e))
    """
    pass  # Herda tudo da classe Exception — só o nome muda