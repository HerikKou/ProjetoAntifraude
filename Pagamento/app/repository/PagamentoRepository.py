from sqlalchemy.orm import Session
from app.models.Pagamento import Pagamento

class PagamentoRepository:

    def salvar(self, db: Session, pagamento: Pagamento):
        db.add(pagamento)
        db.commit()
        db.refresh(pagamento)
        return pagamento
