# 📝 Projeto de estruturação (APP Python - MySQL)
Aplicação para estruturação da linguagem python, praticas de lógica de progamação, métodos internos, bibliotecas etc. Utilização do banco de dados MySQL construindo querys avançadas...


# 🚀 Funcionalidades Principais
pass

# 🛠 Tecnologias e Bibliotecas
Core: Python 3.13

UI/UX: CustomTkinter

Database: MySQL 8.0

Connector: mysql-connector-python

DevOps/Infra: configparser (para gestão de credenciais via config.ini) e venv.

# 📁 Destaques da Estrutura

main.py: Ponto de entrada e controlador.

models/banco_geral.py: Camada de persistência (Data Access Object).

models/test_banco_geral.py: Script de Diagnóstico independente para validar a saúde da conexão com o banco de dados antes da execução do sistema.

utils/helper.py: Funções utilitárias reutilizáveis para lógica de apoio.

# 🔧 Instalação e Testes
Clone o repositório:

Bash

git clone https://github.com/BRUNOSR-DEV/proj_estruturacao.git
Prepare o Ambiente:

Bash

.\vir_proj_es\Scripts\activate
pip install customtkinter mysql-connector-python
Validação de Infraestrutura:
Antes de iniciar o app, rode o script de teste para garantir que suas credenciais no example_config.ini estão corretas ("config.ini.example" terá as credenciais no BD original. "teste_config.ini" com credenciais do BD de testes):

Bash

python test_banco_geral.py
Execução:

Bash

python main.py