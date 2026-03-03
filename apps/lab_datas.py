"""
Laboratório de Datas (datetime e calendar)

"""
usuario = "bruno"
senha = "2285"

"""
O Usuário irá cadastrar sua despesa... ele pode colocar data da compra e data vencimento. Se não colocar a data de vencimento é pq está no cartão de crédito e, ele tem vencimento próprio.

- Método que pega data de fechamento e vencimento do cartão - Dado no bd example = fecha= 6 , venc = 12
    levar em consideração fechamento da fatura 6 dias nates do vencimento
    Returns: (6,12)

- Método que retorna o mês que a  divida precisa ser paga
        data = 20/02/26
        if data_dia > pega_fech_venc(id_user)[0]:
            data_venc = 12/03/26 

- Método que pega todas as dividas do mês seguinte:

- Método que pega as dividas do mês vigente:



"""

from models.banco_geral import(
    verifica_user, 
)
from datetime import datetime, timedelta
from dateutil import parser


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