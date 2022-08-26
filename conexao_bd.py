import sqlite3


def conexao():
    try:
        # Conexão ao banco de dados
        connection = sqlite3.connect("aaaa.db")
        return connection
    except:
        print('Erro banco de dados')


def read_all():
    try:
        # Script para ler todos os dados
        sql = '''SELECT * FROM clientes'''

        connection = conexao()
        cursor = connection.cursor()
        cursor.execute(sql)

        # todos os registros
        rows = cursor.fetchall()

        return rows


    except:
        print('Falha ao conectar-se com o banco. Função read_all!')
    finally:
        cursor.close()
        connection.close()


def read_item(item_pesquisado):
    try:
        item_pesquisado = ('%' + item_pesquisado + '%')

        sql = '''SELECT * FROM clientes WHERE item like ? '''

        connection = conexao()
        cursor = connection.cursor()
        cursor.execute(sql, [item_pesquisado])

        rows = cursor.fetchall()
        return rows

    except:
        print('Falha ao conectar-se com o banco. Função read_item')
    finally:
        cursor.close()
        connection.close()


def read_nome(item_pesquisado):
    try:
        item_pesquisado = ('%' + item_pesquisado + '%')

        sql = '''SELECT * FROM clientes WHERE nome like ? '''

        connection = conexao()
        cursor = connection.cursor()
        cursor.execute(sql, [item_pesquisado])

        rows = cursor.fetchall()
        return rows

    except:
        print('Falha ao conectar-se com o banco. Função read_nome')
    finally:
        cursor.close()
        connection.close()


def read_numero(item_pesquisado):
    try:
        item_pesquisado = ('%' + item_pesquisado + '%')

        sql = '''SELECT * FROM clientes WHERE numero like ? '''

        connection = conexao()
        cursor = connection.cursor()
        cursor.execute(sql, [item_pesquisado])

        rows = cursor.fetchall()
        return rows

    except:
        print('Falha ao conectar-se com o banco. Função read_numero')
    finally:
        cursor.close()
        connection.close()
