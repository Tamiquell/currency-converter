from sqlalchemy.orm import Session

from models import Currency


def get_currency_rate(db: Session, code: str):
    return db.query(Currency).filter(Currency.code == code).first()
