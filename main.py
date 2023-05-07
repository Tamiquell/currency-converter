from fastapi import FastAPI, Depends
from currency import update_currency_rates
from sqlalchemy.orm import Session
from db import Base, SessionLocal, engine
from crud import get_currency_rate


Base.metadata.create_all(bind=engine)


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    update_currency_rates()


@app.get("/update_currencies")
def update_currencies():
    update_currency_rates()
    return {"message": "Currencies updated"}


@app.get("/convert")
def convert_currency(source: str, target: str, amount: float, db: Session = Depends(get_db)):
    source = get_currency_rate(db, source)
    target = get_currency_rate(db, target)
    return {
        "code": target.code,
        "rate": amount * target.rate / source.rate
        }





if __name__ == '__main__':
    import uvicorn
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=8080, reload=True))
    server.run()