"""
Laboratório de Datas (datetime e calendar)

"""

from datetime import datetime, timedelta


# 1. Pegando a data de hoje
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
    print("✅ Pagamento em dia.")