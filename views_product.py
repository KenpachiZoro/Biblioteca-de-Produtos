from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from neteane_site import app, db
from models import Produtos
from helpers import recupera_imagem, deleta_arquivo, FormularioProduto
import time

@app.route('/')
def index():
    lista_produtos = Produtos.query.order_by(Produtos.codigo)
    return render_template('lista.html', titulo='Estoque', produtos=lista_produtos)

@app.route('/novo')
def novo_produto():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo_produto')))
    form = FormularioProduto()
    return render_template('novo.html', titulo='Novo Produto', form=form)

@app.route('/criar_produto', methods=['POST',])
def criar_produto():

    form = FormularioProduto(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo_produto'))

    nome = form.nome.data
    valor = form.valor.data
    quantidade = form.quantidade.data

    produto = Produtos.query.filter_by(nome=nome).first()

    if produto:
        flash('Produto já existente')
        return redirect(url_for('index'))

    novo_produto = Produtos(nome=nome, valor=valor, quantidade=quantidade)
    db.session.add(novo_produto)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa-{novo_produto.codigo}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:codigo>')
def editar(codigo):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', codigo=codigo)))
    produto = Produtos.query.filter_by(codigo=codigo).first()
    form = FormularioProduto()
    form.nome.data = produto.nome
    form.valor.data = produto.valor
    form.quantidade.data = produto.quantidade

    capa_produto = recupera_imagem(codigo)
    return render_template('editar.html', titulo='Editando Produto', codigo=codigo, capa_produto=capa_produto, form=form)


@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioProduto(request.form)

    if form.validate_on_submit():
        produto = Produtos.query.filter_by(codigo=request.form['codigo']).first()
        produto.nome = form.nome.data
        produto.valor = form.valor.data
        produto.quantidade = form.quantidade.data

        db.session.add(produto)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(produto.codigo)
        arquivo.save(f'{upload_path}/capa-{produto.codigo}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar_produto/<int:codigo>')
def deletar_produto(codigo):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',))
    Produtos.query.filter_by(codigo=codigo).delete()

    db.session.commit()
    flash('Produto deletado com sucesso!')
    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

