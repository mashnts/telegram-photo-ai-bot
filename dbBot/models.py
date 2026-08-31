from sqlalchemy import Column, Integer, String, BigInteger, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)
    
    expenses = relationship("Expense", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username}>"
    
class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(String(100))
    date = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="expenses")

    def __repr__(self):
        return f"<Expense {self.amount} - {self.category}>"