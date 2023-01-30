from flask import Flask, url_for, redirect, request, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import utils as u
#from werkzeug.utils import secure_filename
from db import Product, Client, Order
from config import settings as s

#
# Constantes
#
app = Flask(__name__)
engine = create_engine(s.DB_CONNECTION, pool_recycle=3600)
Session = sessionmaker(bind=engine)
session = Session()
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/img/upload/') # Onde salvar as imagens

#
# Pedidos
#
@app.route('/pedidos')
def pedidos():
    return render_template('pedidos.html')
@app.route('/pedidos/cadastrar')
def add_pedido():
    products = session.query(Product).all()
    clients = session.query(Client).all()
    data = {"products" : products, "clients": clients}
    return render_template('add_pedido.html', data=data)
@app.route('/pedidos/cadastrar_2', methods=['POST'])
def add_pedido_post():
    if request.method == 'POST':
        product = session.query(Product).get(request.form['product'])
        return render_template('add_pedidos_2.html',product=product)
    pass
#
# Clientes
#
@app.route('/clientes')
def clientes():
    clients = session.query(Client).all()
    return render_template('clientes.html', clients=clients)
#
# Clientes - Adicionar
#
@app.route('/clientes/cadastrar')
def add_clientes():
    return render_template('add_clientes.html')
@app.route('/clientes/cadastrar', methods=['POST'])
def add_clientes_post():
    if request.method == 'POST':
        # adicionar normal, nada a comentar
        client = Client(request.form['client_name'],request.form['client_uf'],request.form['client_city'],request.form['client_end'],request.form['client_cel'],request.form['client_mail'])
        session.add(client)
        session.commit()
        return redirect(url_for('clientes'))
#
# Clientes - Editar
#
@app.route('/clientes/editar/<id>')
def edit_cliente(id):
    client = session.query(Client).get(id)
                # Primeiro fazemos uma query para pegar o cliente, e setar os valores do input para uma edição mais simples
    return render_template('edit_cliente.html', client=client)
@app.route('/clientes/editar/<id>', methods=['GET','POST'])
def edit_clientes_post(id):
    client = session.query(Client).get(id)
    if request.method == 'POST':
        # Deve existir outra maneira de corrigir isso, ou melhor, fazer com menos linhas
        # * a corrigir
        client.client_name = request.form['client_name']
        client.client_uf = request.form['client_uf']
        client.client_city = request.form['client_city']
        client.client_end = request.form['client_end']
        client.client_cel = request.form['client_cel']
        client.client_mail= request.form['client_mail']
        session.commit()
        return redirect(url_for('clientes'))
#
# Clientes - deletar
#
@app.route('/clientes/deletar/<id>')
def delete_cliente(id):
    cliente = session.query(Client).get(id)
    session.delete(cliente)
    session.commit()
    return redirect(url_for('clientes'))

#
# Produtos
#
@app.route('/produtos')
def produtos():
    products = session.query(Product).all() # Query geral
    return render_template('produtos.html', products=products)
#
# Produtos - Cadastrar
#    
@app.route('/produtos/cadastrar')
def add_produtos():
    return render_template('add_produtos.html')
@app.route('/produtos/cadastrar', methods=['POST'])
def add_produtos_post():
    if request.method == 'POST':
        """
        Faço uma verificação se tem . ou , para voltar como float comum.
        """
        product = Product(int(request.form['cod']),request.form['name'],request.form['desc'],int(request.form['qntd']),float(u.retorna_float_valor(request.form['val'])))
        print(str(u.retorna_float_valor(request.form['val'])))
        img = request.files['arq'] # Requisito a imagem do upload # Salvo um caminho com o nome da imagem
        img.save(u.caminho_imagem(UPLOAD_FOLDER,request.form['name']+'.png')) # Salvo imagem
        session.add(product) # Adiciono o produto
        session.commit()
        return redirect(url_for('produtos'))
#
# Produtos - Deletar, diminuir e aumentar estoque
#
@app.route('/produtos/deletar/<id>')
def deletar(id):
    # Delete comum
    product = session.query(Product).get(id)
    session.delete(product)
    os.remove("{}{}".format(UPLOAD_FOLDER, product.product_name + '.png')) # Deletando arquivo junto
    session.commit()
    return redirect(url_for('produtos'))
        #
        # Atualizações de estoque
        #
@app.route('/produtos/ame/<id>')
def aumentar_estoque(id):
    # Aumento o estoque do produto em 1
    product = session.query(Product).get(id)
    product.product_qntd += 1
    session.commit()
    return redirect(url_for('produtos'))
@app.route('/produtos/dme/<id>')
def diminuir_estoque(id):
    # Diminuo o estoque do produto em 1
    product = session.query(Product).get(id)
    if product.product_qntd >= 1: # Verifica se não tem menos que um
        product.product_qntd -= 1
        session.commit()
        return redirect(url_for('produtos'))
    else:
        return redirect(url_for('produtos'))
#
# App
#
if __name__ == '__main__':
    app.run(debug=True)

