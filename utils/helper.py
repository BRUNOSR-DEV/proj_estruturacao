from datetime import datetime

def str_para_data(data_str):
    """Converte 'DD/MM/AAAA' para objeto datetime."""
    try:
        return datetime.strptime(data_str, "%d/%m/%Y")
    except ValueError:
        print(f"Erro: Formato de data inválido ({data_str})")
        return None

def data_para_exibicao(data_obj):
    """Converte objeto date/datetime para 'DD/MM/AAAA'."""
    if data_obj:
        return data_obj.strftime("%d/%m/%Y")
    return ""

def data_para_mysql(data_obj):
    """Converte objeto date/datetime para 'YYYY-MM-DD'."""
    if data_obj:
        return data_obj.strftime("%Y-%m-%d")
    return None

def formatar_moeda(valor):
    """Auxiliar extra para formatar R$ 1.234,56."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")