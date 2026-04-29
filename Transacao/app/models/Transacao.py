from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import os
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost:3306/transacaodb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Transacao(Base):
    __tablename__ = "transacao"
    id = Column(Integer, primary_key=True, index=True)
    contaOrigem = Column(String(255), nullable=False)
    contaDestino = Column(String(255), nullable=False)
    valor = Column(Float, nullable=False)
    status = Column(String(255), default="PENDENTE")
    tipo_transacao = Column(String(255), nullable=False)
    Score_fraude = Column(Float, nullable=True)
    data_transacao = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
