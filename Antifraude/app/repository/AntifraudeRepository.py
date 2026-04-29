from sqlalchemy.orm import Session
from app.models.Antifraude import Antifraude
from datetime import datetime, timedelta

class AntifraudeRepository:

    def salvar(self, db: Session, antifraude: Antifraude):
        db.add(antifraude)
        db.commit()
        db.refresh(antifraude)
        return antifraude

    def verificar_conta_destino(self, db: Session, conta_destino: str):
        return db.query(Antifraude).filter(Antifraude.conta_destino == conta_destino).first()

    def verificar_frequencia(self, db: Session, conta_origem: str):
        dez_minutos_atras = datetime.utcnow() - timedelta(minutes=10)
        return db.query(Antifraude).filter(
            Antifraude.conta_origem == conta_origem,
            Antifraude.data_analise >= dez_minutos_atras
        ).count()
