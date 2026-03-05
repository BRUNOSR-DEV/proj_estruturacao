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

def verifica_login(usuario, senha, conn=None):
    """
    Verificar usuario e senha no BD e confirmar login.
    
    Args:
        usuario (str): Nome do usuário a ser pesquisado
        senha (str): Senha do usuário a ser pesquisado
        conn (MySQLdb.connections.Connection, optional): Conexão ativa com o banco. 
            Se não fornecida, a função abre e gerencia sua própria conexão.

    Returns:
        True: Se o usuário e senha estiver correto e no BD, confirma o acesso 
        None: Se o usuário não for localizado ou tiver erro de digitação.
    """

    gerenciar_conn = False

    if conn is None:
        conn= conectar_bd_original()
        gerenciar_conn = True

    cursor = conn.cursor() # Mensageiro, passa o comando e retorna resltados

    try:
        cursor.execute('SELECT id FROM usuario WHERE nome_usuario=%s AND senha=%s', (usuario, senha))
        login_sucesso = cursor.fetchone()

        if login_sucesso:
            print('Usuário e senha encontrado! ')
            return login_sucesso
        else:
            print("Usuário ou Senha não encontrado!")
            return None
        
    except MySQLdb.Error as e: # Captura erro específico do MySQL
        print(f'Erro no MySQL ao verificar usuário e senha: {e}')
        raise # Re-levanta a exceção para que o chamador saiba que algo deu errado

    except Exception as e:
        print(f'Erro inesperado ao verificar usuário e senha: {e}')

    finally:
        if gerenciar_conn:
            desconectar(conn)


def pega_despesas_cartao(id_user, id_card, conn=None):
    """
    Busca todas as despesas de um cartão específico, trazendo junto 
    os dados do cartão em um único dicionário usando INNER JOIN.
    """
    gerenciar_conn = False
    if conn is None:
        conn = conectar_bd_original()
        gerenciar_conn = True

    cursor = conn.cursor()

    try:
        # A mágica acontece aqui: Juntamos as duas tabelas onde as chaves se encontram
        query = """
            SELECT 
                d.id, 
                d.local, 
                d.valor_total, 
                d.parcelas, 
                d.data_compra,
                c.nome,
                c.limite, 
                c.dia_fechamento, 
                c.dia_vencimento
            FROM despesas d
            INNER JOIN cartoes_credito c ON d.fk_cc = c.id
            WHERE d.fk_usuario = %s AND d.fk_cc = %s
        """
        
        cursor.execute(query, (id_user, id_card))
        resultados = cursor.fetchall()
        
        # Mapeando as colunas. 
        # Cuidado para não confundir o vencimento da despesa com o da fatura!
        colunas = [
            'despesa_id', 'local', 'valor_total', 'parcelas', 'data_compra', 
            'nome_cartao', 'limite_cartao', 'fechamento_fatura', 'vencimento_fatura'
        ]
        
        # O Padrão Ouro que você já domina!
        return [dict(zip(colunas, linha)) for linha in resultados]

    except Exception as e:
        print(f"Erro ao buscar despesas e cartão (JOIN): {e}")
        return []
    finally:
        if gerenciar_conn:
            desconectar(conn)





def pega_cartao(id_user, id_card, conn=None):
    """
    Busca os cartões cadastrados pelo usuário

    Args:
        id_user: id do usuário que fez login
    Returns:
        List: Retorna uma lista com (nome, data_fechamento, data_vencimento)
    """
    gerenciar_conn = False

    if conn is None:
        conn= conectar_bd_original()
        gerenciar_conn= True

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT nome, limite, dia_fechamento, dia_vencimento FROM cartoes_credito WHERE fk_usuario = %s and id = %s", (id_user, id_card, ))
        cartoes = cursor.fetchall() 

        colunas = ['nome', 'limite', 'dia_fechamento', 'dia_vencimento']
        return [dict(zip(colunas, c)) for c in cartoes]
    
    except MySQLdb.Error as e:
        print(f"Erro MySQL ao listar cartoes: {e}")
        return [] # Retorna lista vazia em caso de erro no DB
    except Exception as e: # Capture exceções para depuração
        print(f"Erro ao listar cartoes: {e}")
        return [] # Retorne uma lista vazia em caso de erro geral
    
    finally:
        if gerenciar_conn:
            desconectar(conn)




def pega_despesas_geral(id_user, conn=None):
    """
    Busca as despesas do usuário
    Args:
        id_user: identificação do usuário
    Returns:
        List(Dict): Retorna uma lista de dicionarios com as despesas do usuáro passado

    """
    gerenciar_conn = False

    if conn is None:
        conn= conectar_bd_original()
        gerenciar_conn= True

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, local, valor_total, parcelas, data_compra, data_vencimento, fk_cc FROM despesas WHERE fk_usuario = %s", (id_user,))
        despesas = cursor.fetchall() # fetchall() para obter todas as linhas, retorna tupla de tuplas 

        colunas = ['id', 'local', 'valor_total', 'parcelas', 'data_compra', 'data_vencimento', 'cartao_id']
        return [dict(zip(colunas, d)) for d in despesas]
    
    except MySQLdb.Error as e:
        print(f"Erro MySQL ao listar despesas: {e}")
        return [] # Retorna lista vazia em caso de erro no DB
    except Exception as e: # Capture exceções para depuração
        print(f"Erro ao listar despesas: {e}")
        return [] # Retorne uma lista vazia em caso de erro geral
    
    finally:
        if gerenciar_conn:
            desconectar(conn)
