import os
from neteane_site import app
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, validators, SubmitField, PasswordField


class FormularioProduto(FlaskForm):
    nome = StringField('Nome do Produto', [validators.DataRequired(), validators.Length(min=1, max=30)])
    valor = FloatField('Valor', [validators.DataRequired()])
    quantidade = FloatField('Quantidade', [validators.DataRequired()])
    salvar = SubmitField('Salvar')

class FormularioUsuario(FlaskForm):
    nome = StringField('Nome de Usuário', [validators.DataRequired(), validators.Length(min=1, max=30)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')

def recupera_imagem(codigo):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa-{codigo}' in nome_arquivo:
            return nome_arquivo
    return "capa_padrao.png"

def deleta_arquivo(codigo):
    arquivo = recupera_imagem(codigo)
    if arquivo != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))