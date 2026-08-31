from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models import Base, User, Expense

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_or_create_user(session, telegram_id, username):

    user = session.query(User).filter(User.telegram_id == telegram_id).first()

    if user:
        return user
    
    new_user = User(telegram_id=telegram_id, username=username)
    session.add(new_user)
    session.commit()
    
    return new_user


def get_user_by_telegram_id(session, telegram_id):

    return session.query(User).filter(User.telegram_id == telegram_id).first()


def add_expense(session, user_id, amount, category, description=""):

    new_expense = Expense(
        user_id = user_id,
        amount = amount,
        category = category, 
        description = description
    )

    session.add(new_expense)
    session.commit()

    return new_expense


def get_user_expenses(session, user_id, limit=10):

    return session.query(Expense).\
    filter(Expense.user_id == user_id).\
    order_by(Expense.date.asc()).\
    limit(limit).\
    all()


def get_expenses_by_category(session, user_id):
    return session.query(Expense.category, func.sum(Expense.amount)).filter(Expense.user_id == user_id)\
    .group_by(Expense.category)\
    .all()


def delete_expense(session, expense_id):
    expense = session.query(Expense).filter(Expense.id == expense_id).first()

    if expense:
        session.delete(expense)
        session.commit()
        return True
    
    return False
