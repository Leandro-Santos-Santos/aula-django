import mysql.connector
def conecta_no_banco_de_dados():
    orc = mysql.connector.connect(host='127.0.0.1',user='root',password='')
    
    # Executar a instrução SQL para verificar se o banco de dados existe
    cursor = orc.cursor()
    cursor.execute('SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = "aula08";')

    # Obter o número de resultados
    num_results = cursor.fetchone()[0]

    # Fechar a conexão com o banco de dados
    orc.close()

    # Se o número de resultados for maior que zero, o banco de dados existe
    if num_results > 0:
        print('O banco de dados aula08 existe e esta pronto para uso.')
    else:
        # Conectar-se ao servidor MySQL para criar o banco de dados
        orc = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password=''
        )

        # Criar o banco de dados aula06
        cursor = orc.cursor()
        cursor.execute('CREATE DATABASE aula08;')
        orc.commit()

    # Conectar-se ao banco de dados aula06 recém-criado
        orc = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='aula08'  # Especificar o banco de dados
        )

    
        cursor = orc.cursor()
        cursor.execute('CREATE TABLE contatos (id_contato INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, mensagem TEXT NOT NULL,situacao varchar (50) NOT NULL);')

        cursor.execute('CREATE TABLE usuarios (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), email VARCHAR(255), senha VARCHAR(255));')

        cursor.execute('CREATE TABLE usuario_contato (usuario_id INT NOT NULL, contato_id INT NOT NULL, situacao VARCHAR(255) NOT NULL, PRIMARY KEY (usuario_id, contato_id), FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE, FOREIGN KEY (contato_id) REFERENCES contatos(id_contato) ON DELETE CASCADE);')
        orc.commit()
        nome="ORACLE"
        email="redbullracing@oracle.com"
        senha="12345"
        sql = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
        valores = (nome, email, senha)
        cursor.execute(sql, valores)
        orc.commit()
        
        orc.close()
    try:
        bmq = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='aula08'
        )
    except mysql.connector.Error as err:
        print("Erro de conexão com o banco de dados:", err)
        raise

    return bmq