from flask import Flask, url_for, redirect, request, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import Product

app = Flask(__name__)
engine = create_engine('mysql+mysqldb://root:45093988rgftqj@localhost/sys_estoque_rb', pool_recycle=3600)
Session = sessionmaker(bind=engine)
session = Session()

# Produtos
@app.route('/produtos')
def produtos():
    products = session.query(Product).all()
    return render_template('produtos.html', products=products)


if __name__ == '__main__':
    app.run(debug=True)
