import os

SECRET_KEY = 'netiane'

SQLALCHEMY_DATABASE_URI= \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = '8y17tzps#EU',
        servidor = 'localhost',
        database = 'neteane_site'
    )
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'