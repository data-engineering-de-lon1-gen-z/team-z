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
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = "product"
    id = Column(uuid(), primary_key=True)
    name = Column(String(255), nullable=False)
    size = Column(String(255), nullable=False)
    flavour = Column(String(255), nullable=False)
    iced = Column(Boolean, nullable=False)
    price = Column(DECIMAL(4, 2), nullable=False)

    __table_args__ = (UniqueConstraint("name", "size", "flavour", "iced"),)


class Location(Base):
    __tablename__ = "location"

    id = Column(uuid(), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    transactions = relationship("Transaction")


class BasketItem(Base):
    __tablename__ = "basket"

    id = Column(uuid(), primary_key=True)
    transaction_id = Column(uuid(), ForeignKey("transaction.id"), nullable=False)
    product_id = Column(uuid(), ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    transaction = relationship(
        "Transaction",
        backref=backref("basket", uselist=True),
        foreign_keys="BasketItem.transaction_id",
    )
    products = relationship("Product", backref=backref("basket", uselist=True))


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(uuid(), primary_key=True)
    datetime = Column(DateTime, nullable=False)
    location_id = Column(uuid(), ForeignKey("location.id"), nullable=False)
