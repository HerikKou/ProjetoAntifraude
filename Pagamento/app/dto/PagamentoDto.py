from pydantic import BaseModel

class PagamentoKafkaDto(BaseModel):
    transacao_id: int
    status: str
    score: float
