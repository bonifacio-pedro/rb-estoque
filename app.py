from flask import Flask, url_for, redirect, request, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
#from werkzeug.utils import secure_filename
from db import Product

app = Flask(__name__)
engine = create_engine('mysql+mysqldb://root:45093988rgftqj@localhost/sys_estoque_rb', pool_recycle=3600)
Session = sessionmaker(bind=engine)
session = Session()
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/img/upload')

# Produtos
@app.route('/produtos')
def produtos():
    products = session.query(Product).all()
    return render_template('produtos.html', products=products)

@app.route('/produtos/deletar/<id>')
def deletar(id):
    product = session.query(Product).filter_by(product_id=id).one()
    session.delete(product)
    session.commit()
    return redirect(url_for('produtos'))

@app.route('/produtos/ame/<id>')
def aumentar_estoque(id):
    product = session.query(Product).filter_by(product_id=id).one()
    product.product_qntd += 1
    session.commit()
    return redirect(url_for('produtos'))

@app.route('/produtos/dme/<id>')
def diminuir_estoque(id):
    product = session.query(Product).filter_by(product_id=id).one()
    product.product_qntd -= 1
    session.commit()
    return redirect(url_for('produtos'))

@app.route('/produtos/cadastrar')
def add_produtos():
    return render_template('add_produtos.html')

@app.route('/produtos/cadastrar', methods=['POST'])
def add_produtos_post():
    if request.method == 'POST':
        val_new = request.form['val']
        if ',' in val_new:
            val_new = val_new.replace(',','.')
        product = Product(int(request.form['cod']),request.form['name'],request.form['desc'],int(request.form['qntd']),float(val_new))
        img = request.files['arq']
        img_path = os.path.join(UPLOAD_FOLDER, img.filename)
        img.save(img_path)
        session.add(product)
        session.commit()
        return redirect(url_for('produtos'))

if __name__ == '__main__':
    app.run(debug=True)

