import enum
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

# Define the Enum type
class PaymentType(enum.Enum):
    card = 1
    cash = 2

    # Create PaymentType objects from string
    # Expects "CARD" or "CASH" as defined in the sample data
    @staticmethod
    def from_str(label):
        if label in "CARD":
            return PaymentType.card
        elif label in "CASH":
            return PaymentType.cash
        else:
            raise NotImplementedError


class Product(Base):
    __tablename__ = "product"
    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    size = Column(String(255), nullable=False)
    flavour = Column(String(255), nullable=False)
    iced = Column(Boolean, nullable=False)
    price = Column(DECIMAL(4, 2), nullable=False)

    __table_args__ = (UniqueConstraint("name", "size", "flavour", "iced"),)


class Location(Base):
    __tablename__ = "location"

    id = Column(String(36), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    transactions = relationship("Transaction")


class BasketItem(Base):
    __tablename__ = "basket"

    id = Column(String(36), primary_key=True)
    transaction_id = Column(String(36), ForeignKey("transaction.id"), nullable=False)
    product_id = Column(String(36), ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    transaction = relationship(
        "Transaction",
        backref=backref("basket", uselist=True),
        foreign_keys="BasketItem.transaction_id",
    )
    products = relationship("Product", backref=backref("basket", uselist=True))


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(String(36), primary_key=True)
    datetime = Column(DateTime, nullable=False)
    payment_type = Column(Enum(PaymentType), nullable=False)
    location_id = Column(String(36), ForeignKey("location.id"), nullable=False)
