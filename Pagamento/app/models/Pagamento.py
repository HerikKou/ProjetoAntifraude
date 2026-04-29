from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost:3306/pagamentodb")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Pagamento(Base):
    __tablename__ = "pagamento"
    id = Column(Integer, primary_key=True, index=True)
    transacao_id = Column(Integer, nullable=False)
    status = Column(String(255), nullable=False)
    score_fraude = Column(Float, nullable=True)
    tipo_pagamento = Column(String(255), nullable=True)
    data_pagamento = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
