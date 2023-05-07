import requests
from models import Currency
from db import SessionLocal

def update_currency_rates():
    response = requests.get("https://api.exchangerate.host/latest?base=usd")
    rates = response.json()["rates"]


    db = SessionLocal()
    try:
        for code, rate in rates.items():
            currency = db.query(Currency).filter_by(code=code).first()
            if currency:
                currency.rate = rate
            else:
                currency = Currency(code=code, rate=rate)
                db.add(currency)
        db.commit()
    finally:
        db.close()
