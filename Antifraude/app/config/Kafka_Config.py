import json
import os
from kafka import KafkaProducer, KafkaConsumer

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

TOPICO_TRANSACAO_CRIADA = "transacao_criada"
TOPICO_FRAUDE_DETECTADA = "fraude_detectada"
TOPICO_TRANSACAO_APROVADA = "transacao_aprovada"


def criar_producer():
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        acks="all",
        retries=10,
        linger_ms=5,
        request_timeout_ms=30000
    )


def criar_consumer():
    return KafkaConsumer(
        TOPICO_TRANSACAO_CRIADA,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        group_id="antifraude-group",
        enable_auto_commit=True,
        session_timeout_ms=30000,
        heartbeat_interval_ms=10000
    )