from flask import Flask, url_for, redirect, request, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import utils as u
#from werkzeug.utils import secure_filename
from db import Product

app = Flask(__name__)
engine = create_engine('mysql+mysqldb://root:45093988rgftqj@localhost/sys_estoque_rb', pool_recycle=3600)
Session = sessionmaker(bind=engine)
session = Session()
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/img/upload') # Onde salvar as imagens

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
        img = request.files['arq'] # Requisito a imagem do upload # Salvo um caminho com o nome da imagem
        img.save(u.caminho_imagem(UPLOAD_FOLDER,img.filename)) # Salvo imagem
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
    session.commit()
    return redirect(url_for('produtos'))

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

