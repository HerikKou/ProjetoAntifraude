from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransacaoRequest(BaseModel):
    conta_origem: str
    conta_destino: str
    valor: float
    tipo_transacao: str

class TransacaoResponse(BaseModel):
    id: int
    contaOrigem: str
    contaDestino: str
    valor: float
    tipo_transacao: str
    status: str
    Score_fraude: Optional[float]
    data_transacao: datetime

    class Config:
        from_attributes = True
