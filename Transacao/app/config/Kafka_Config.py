from kafka import KafkaProducer
import json
import os

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPICO_TRANSACAO_CRIADA = "transacao_criada"

def criar_producer():
    return KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    request_timeout_ms=30000,
    retries=5,
    linger_ms=10
)
