from sqlalchemy import Column, Integer, String, ForeignKey, REAL, DateTime, Enum
from database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    password = Column(String(50))
    email = Column(String(120), unique=True)


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    owner = Column(Integer)


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    description = Column(String(100))
    category = ForeignKey('category.id', ondelete='CASCADE')
    owner = ForeignKey('user.id', ondelete='CASCADE')
    type = Column(Enum('income', 'spend'))
    date = Column(DateTime)
    amount = Column(REAL)

    def __repr__(self):
        return f'<User {self.name!r}>'
