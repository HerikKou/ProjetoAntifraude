from pydantic import BaseModel

class TransacaoKafkaDto(BaseModel):
    id: int
    conta_Origem: str
    conta_Destino: str
    valor: float
    tipo_transacao: str
