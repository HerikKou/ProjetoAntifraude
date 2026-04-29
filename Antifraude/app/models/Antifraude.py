from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

import os
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost:3306/antifraudedb")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Antifraude(Base):
    __tablename__ = "antifraude"
    id = Column(Integer, primary_key=True, index=True)
    transacao_id = Column(Integer, nullable=False)
    conta_origem = Column(String(255), nullable=False)
    conta_destino = Column(String(255), nullable=False)
    valor = Column(Float, nullable=False)
    score = Column(Float, nullable=True)
    status = Column(String(255), default="PENDENTE")
    data_analise = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
