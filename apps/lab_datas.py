"""
Laboratório de Datas (datetime e calendar)

"""
import sys
import os

# Adiciona a pasta raiz (PROJ_ESTRUTURACAO) ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.banco_geral import(
    pega_cartoes, pega_despesas
)
from utils.helper import
from datetime import datetime, timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta

usuario = "bruno"
senha = "2285"
id_user = 1

"""
O Usuário irá cadastrar sua despesa... ele pode colocar data da compra e data vencimento. Se não colocar a data de vencimento é pq está no cartão de crédito e, ele tem vencimento próprio.

- Método que pega data de fechamento e vencimento do cartão - Dado no bd example = fecha= 6 , venc = 12
    levar em consideração fechamento da fatura 6 dias nates do vencimento
    Returns: (6,12)

- Método que retorna o mês que a  divida precisa ser paga
        data = 20/02/26
        if data_dia > pega_fech_venc(id_user)[0]:
            data_venc = 12/03/26 

- Método que retorna despesas de cada cartão utilizado pelo usuario

- Método que pega a soma todas as dividas do mês seguinte

- Método que pega soma de todas as dividas do mês vigente

- Método que retorna as despesas não cadastradas no cartão.


"""




def definir_vencimento_real(data_compra_str, dia_fechamento, dia_vencimento):
    # 1. Converte a entrada do usuário
    data_compra = datetime.strptime(data_compra_str, "%d/%m/%Y")
    
    # 2. Lógica: A fatura já fechou?
    if data_compra.day > dia_fechamento:
        # Se sim, o vencimento é no PRÓXIMO mês
        vencimento = data_compra + relativedelta(months=1)
    else:
        # Se não, o vencimento é no MÊS ATUAL
        vencimento = data_compra
    
    # 3. Ajusta o dia para o dia oficial de vencimento do cartão
    vencimento_final = vencimento.replace(day=dia_vencimento)
    
    return vencimento_final


def depesas_do_usuario(id_user):
    """
    Método que mostra as despesas do usuário
    """
    for i in pega_despesas(id_user):
        print(i.get('local'))


    




















#data_usuario = input("Digite uma data: ")
data_input = input("Digite a data (DD/MM/AAAA)")

try:
    data_valida = datetime.strptime(data_input, "%d/%m/%Y")
    print(f'Sucesso: {data_valida}')
    """data_obj = parser.parse(data_usuario, dayfirst=True, fuzzy=True)
    print(f'Data interpretada: {data_obj}')"""
except ValueError:
    print("Formato de data invalido!")

















"""# 1. Pegando a data de hoje
hoje = datetime.now()
print(f"Hoje é: {hoje.strftime('%d/%m/%Y')}")

# 2. Lógica de Vencimento (Adicionando 30 dias para uma conta)
vencimento = hoje + timedelta(days=30)
print(f"O boleto vence em: {vencimento.strftime('%d/%m/%Y')}")

# 3. Comparação (O boleto está atrasado?)
data_pagamento = datetime(2025, 3, 10) # Simulando um pagamento futuro
if data_pagamento > vencimento:
    print("⚠️ Cuidado! Pagamento após o vencimento.")
else:
    print("✅ Pagamento em dia.")"""