from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Product(Base):
    __tablename__ = 'product'
    product_id = Column(Integer, autoincrement=True, primary_key=True)
    product_cod = Column(Integer, nullable=False)
    product_name = Column(String(125), nullable=False)
    product_desc = Column(String(360), nullable=False)
    product_qntd = Column(Integer, nullable=False)
    product_valor = Column(Float, nullable=False)

    def __init__(self,product_cod,product_name,product_desc,product_qntd,product_valor):
        self.product_cod = product_cod
        self.product_name = product_name
        self.product_desc = product_desc
        self.product_qntd = product_qntd
        self.product_valor = product_valor

class Client(Base):
    __tablename__ = 'clients'
    client_id = Column(Integer, autoincrement=True, primary_key=True)
    client_name = Column(String(125), nullable=False)
    client_uf = Column(String(15), nullable=False)
    client_city = Column(String(125), nullable=False)
    client_end = Column(String(200), nullable=False)
    client_cel = Column(String(125), nullable=False)
    client_mail = Column(String(125), nullable=False)

    def __init__(self,client_name,client_uf,client_city,client_end,client_cel,client_mail):
        self.client_name = client_name
        self.client_uf = client_uf
        self.client_city = client_city
        self.client_end = client_end
        self.client_cel = client_cel
        self.client_mail = client_mail
