from sqlalchemy.orm import Session
from app.models.Transacao import Transacao

class TransacaoRepository:

    def salvar(self, db: Session, transacao: Transacao):
        db.add(transacao)
        db.commit()
        db.refresh(transacao)
        return transacao

    def buscar_por_id(self, db: Session, id: int):
        return db.query(Transacao).filter(Transacao.id == id).first()

    def buscar_todas(self, db: Session):
        return db.query(Transacao).all()
