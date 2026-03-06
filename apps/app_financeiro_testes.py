"""
Laboratório de Datas (datetime e calendar)

"""
import sys
import os

# Adiciona a pasta raiz (PROJ_ESTRUTURACAO) ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.banco_geral import(
    pega_despesas_geral, pega_despesas_cartao
)
from utils.helper import (
    str_para_data, data_para_exibicao, data_para_mysql, formatar_moeda, mysql_para_obj, ret_str_parcelas
)
from datetime import datetime, timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta

usuario = "bruno"
senha = "2285"
id_user = 1
id_card = 1

"""
O Usuário irá cadastrar sua despesa... ele pode colocar data da compra e data vencimento. Se não colocar a data de vencimento é pq está no cartão de crédito e, ele tem vencimento próprio.

- Método que pega data de fechamento e vencimento do cartão - Dado no bd example = fecha= 6 , venc = 12
    levar em consideração fechamento da fatura 6 dias nates do vencimento
    Returns: (6,12)

- Método que retorna o mês que a  divida precisa ser paga
        data = 20/02/26
        if data_dia > pega_fech_venc(id_user)[0]:
            data_venc = 12/03/26 

            💡----- IDEIAS ---- 💡
- Método que retorna despesas de cada cartão utilizado pelo usuario ✅

    - O método precisa retornar despesas do vigente e do mês seguinte
    - O método precisa retornar só despesas que precisam ser pagas ✅
    - O método precisa retornar o total do que precisa ser pago  no mês

- Método que retorna as despesas não cadastradas no cartão (despesas_avulsas)

    - O método retorna somente as despesas a serem pagas no mês e no mês seguinte
    - O método precisa retornar o total do que precisa ser  pago no mês

- Método que pega soma de todas as dividas do mês vigente
    - Método que retona o calculo das somas de cada fatura e total de despesas avulsas






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

def nome_card(dict):
    for i in dict:
        return i.get('nome_cartao')    

def depesas_um_cartao(id_user, id_card):
    """
    Método que mostra as despesas de um único cartão cadastrado

        returns pega_despesas_cartao: [
            'despesa_id', 'local', 'valor_total', 'parcelas', 'data_compra', 
            'nome_cartao', 'limite_cartao', 'fechamento_fatura', 'vencimento_fatura'
        ]
    """

    des_card = pega_despesas_cartao(id_user, id_card)
    data_teste = mysql_para_obj('2026-06-02')

    total_fatura = 0
    data_atual = data_atual = datetime.now()

    if des_card:

        mes_fatura = None

        print(f" Analizando fatura do cartão {nome_card(des_card)}")

        for i, v in enumerate(des_card):
            # 1. Pegamos os dados individuais DESTA despesa específica 'v'
            fechamento = v.get('fechamento_fatura')
        
            # Garante que a data é um objeto (use seu helper aqui se precisar)
            data_compra = mysql_para_obj(v.get('data_compra'))
        
            # 2. Chamamos nossa super função!
            str_parcela = ret_str_parcelas(data_compra, fechamento, v.get('parcelas'), data_teste)


            if str_parcela[1]:
                    valor_mensal = v.get('valor_total') / v.get('parcelas')
                    total_fatura += valor_mensal

                    # 3. Exibimos o resultado
                    print(f"[{i+1}] - Local: {v.get('local')}")
                    print(f"      Valor Mensal: {formatar_moeda(valor_mensal)}")
                    print(f"      Andamento: {str_parcela[0]}")
                    print("-" * 30)

            dia_venc = int(v.get('vencimento_fatura'))

            if str_parcela[2]:
                mes_fatura = str_parcela[2].replace(day=dia_venc)
            else:
                data_atual = data_teste
                mes_fatura = data_atual.replace(day=dia_venc)

        print(F'TOTAL DA FATURA: {formatar_moeda(total_fatura)} Vencimento: {data_para_exibicao(mes_fatura)} ')
    else:
        print('Não tem despesas no cartão informado! ')
            


depesas_um_cartao(id_user, id_card)

          
    


def despesas_gerais(id_user):
    pass


















'''#data_usuario = input("Digite uma data: ")
data_input = input("Digite a data (DD/MM/AAAA)")

try:
    data_valida = datetime.strptime(data_input, "%d/%m/%Y")
    print(f'Sucesso: {data_valida}')
    """data_obj = parser.parse(data_usuario, dayfirst=True, fuzzy=True)
    print(f'Data interpretada: {data_obj}')"""
except ValueError:
    print("Formato de data invalido!")'''

















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