import MySQLdb

import configparser # Modulo nativo do Py. Ele cria, lê,atualiza e gerencia arq/ de conf/


def ler_configuracao_bd():
    """
    Lê as credenciais do banco de dados do arquivo 'config.ini'.
    
    Busca pela seção [mysql] para garantir que as credenciais 
    não fiquem expostas no código-fonte (Pratica de de segurança).
    
    Returns:
        dict: Dicionário contendo host, user, passwd e db se sucesso.
        None: Caso o arquivo não exista ou a seção esteja ausente.
    """

    config = configparser.ConfigParser() # Instanciando o objeto config
    
    # Tenta ler o arquivo de configuração
    try:
        config.read('config.ini')
        if 'mysql' not in config:
            raise ValueError("Seção [mysql] não encontrada em config.ini")
            
        bd_config = config['mysql']
        return {
            'host': bd_config.get('host', 'localhost'), # se não for "host" define como "localhost"
            'user': bd_config.get('user'),
            'passwd': bd_config.get('passwd'),
            'db': bd_config.get('db')
        }
    except FileNotFoundError:
        print("Erro: Arquivo 'config.ini' não encontrado.")
        return None
    except ValueError as e:
        print(f"Erro de configuração: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado ao ler o arquivo de configuração: {e}")
        return None


def conectar_bd_original():
    """
    Estabelece a conexão com o servidor MySQL utilizando as credenciais.
    
    Returns:
        MySQLdb.connections.Connection: Objeto de conexão se bem-sucedido.
        None: Em caso de falha de leitura de configuração ou recusa do servidor.
    """

    bd_config = ler_configuracao_bd()
    if not bd_config:
        # Se as credenciais não puderam ser lidas, não tente conectar
        print("Não foi possível conectar ao banco de dados devido a um erro de configuração.")
        return None
    
    try:
        conn = MySQLdb.connect(
            db=bd_config['db'],
            host=bd_config['host'],
            user=bd_config['user'],
            passwd=bd_config['passwd']
        )
        return conn

    except MySQLdb.Error as e:
        print(f'Erro na conexão ao MySql Server: {e}')


def desconectar(conn):
    """ 
    Encerra a conexão com o banco de dados de forma segura.
    
    Args:
        conn (MySQLdb.connections.Connection): A conexão ativa atual.
    """
    if conn:
        conn.close()


#--------------- Tabelas de testes dos apps -----------------------

def verifica_user(user, senha, conn=None):
    pass

