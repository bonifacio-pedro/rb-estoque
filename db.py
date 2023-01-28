from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'product'
    product_id = Column(Integer, autoincrement=True, primary_key=True)
    product_cod = Column(Integer, nullable=False)
    product_name = Column(String(125), nullable=False)
    product_desc = Column(String(360), nullable=False)
    product_qntd = Column(Integer, nullable=False)
    product_valor = Column(Integer, nullable=False)

    def __init__(self,product_cod,product_name,product_desc,product_qntd,product_valor):
        self.product_cod = product_cod
        self.product_name = product_name
        self.product_desc = product_desc
        self.product_qntd = product_qntd
        self.product_valor = product_valor
