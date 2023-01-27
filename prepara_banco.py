import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='8y17tzps#EU'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `neteane_site`;")

cursor.execute("CREATE DATABASE `neteane_site`;")

cursor.execute("USE `neteane_site`;")

# criando tabelas
TABLES = {}
TABLES['Produtos'] = ('''
      CREATE TABLE `produtos` (
      `codigo` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `valor` varchar(40) NOT NULL,
      `quantidade` varchar(20) NOT NULL,
      PRIMARY KEY (`codigo`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(20) NOT NULL,
      `email` varchar(100) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("jackson", "jacksonjunior2109@gmail.com", generate_password_hash("123").decode('utf-8')),
      ("neteane", "silvaneteane@gmail.com", generate_password_hash("1502").decode('utf-8')),
      ("Guilherme Louro", "Cake", generate_password_hash("python_eh_vida").decode('utf-8'))
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from neteane_site.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
produtos_sql = 'INSERT INTO produtos (nome, valor, quantidade) VALUES (%s, %s, %s)'
produtos = [
      ('Cola Branca', 2, 5),
      ('Papel Fotográfico', 2, 5),
      ('Massa Biscuit', 15, 5)


]
cursor.executemany(produtos_sql, produtos)

cursor.execute('select * from neteane_site.produtos')
print(' -------------  Produtos:  -------------')
for produto in cursor.fetchall():
    print(produto[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()