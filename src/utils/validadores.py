import re
from datetime import datetime


def validar_cpf(cpf: str) -> bool:
    # Limpa o CPF (remove pontos e traços)
    cpf = "".join(filter(str.isdigit, cpf))

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Cálculo dos dígitos verificadores
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(i))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True


def validar_email(email):
    # Regex básica para verificar formato nome@dominio.com
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(padrao, email) is not None


def validar_data_nascimento(data_str):
    try:
        # Tenta converter a string no formato brasileiro
        data_obj = datetime.strptime(data_str, "%d/%m/%Y")
        # Verifica se a data não é no futuro
        return data_obj <= datetime.now()
    except ValueError:
        return False
