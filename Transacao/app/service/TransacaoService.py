from sqlalchemy.orm import Session
from app.models.Transacao import Transacao
from app.repository.TransacaoRepository import TransacaoRepository
from app.dto.TransacaoDto import TransacaoRequest
from app.config.Kafka_Config import criar_producer, TOPICO_TRANSACAO_CRIADA
from datetime import datetime

repository = TransacaoRepository()

class TransacaoService:

    def criar_transacao(self, db: Session, request: TransacaoRequest):
        transacao = Transacao(
            contaOrigem=request.conta_origem,
            contaDestino=request.conta_destino,
            valor=request.valor,
            tipo_transacao=request.tipo_transacao,
            status="PENDENTE",
            data_transacao=datetime.utcnow()
        )

        transacao_salva = repository.salvar(db, transacao)

        producer = criar_producer()

        producer.send(TOPICO_TRANSACAO_CRIADA, {
            "id": transacao_salva.id,
            "contaOrigem": transacao_salva.contaOrigem,
            "contaDestino": transacao_salva.contaDestino,
            "valor": transacao_salva.valor,
            "tipo_transacao": transacao_salva.tipo_transacao
        })

        producer.flush(10)

        return transacao_salva