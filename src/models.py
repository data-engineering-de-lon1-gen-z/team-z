from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    DECIMAL,
    Boolean,
    Enum,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = "product"

    id = Column(String(36), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    size = Column(String(255))
    flavour = Column(String(255))
    iced = Column(Boolean, nullable=False)
    price = Column(DECIMAL(4, 2), nullable=False)
    baskets = relationship("Basket")


# TODO Also store the address?
class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    transactions = relationship("Transaction")


class Basket(Base):
    __tablename__ = "basket"

    id = Column(String(36), primary_key=True)
    transaction = relationship("Transaction", uselist=False, back_populates="basket")
    product_id = Column(String(36), ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=False)


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(String(36), primary_key=True)
    datetime = Column(DateTime, nullable=False)
    location_id = Column(Integer, ForeignKey("location.id"), nullable=False)
    basket_id = Column(String(36), ForeignKey("basket.id"), nullable=False)
    basket = relationship("Basket", back_populates="transaction")
