from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)
    nit = Column(String)
    nombre = Column(String)
    correo = Column(String)

class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True)
    numero = Column(String)
    subtotal = Column(Numeric)
    iva = Column(Numeric)
    total = Column(Numeric)
    estado = Column(String)