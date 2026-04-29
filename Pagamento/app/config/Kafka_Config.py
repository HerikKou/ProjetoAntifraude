from kafka import KafkaConsumer
import json
import os

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPICO_TRANSACAO_APROVADA = "transacao_aprovada"

def criar_consumer_aprovada():
    print(f"[Pagamento] Conectando ao Kafka em {BOOTSTRAP_SERVERS}...")

    return KafkaConsumer(
        TOPICO_TRANSACAO_APROVADA,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        group_id="pagamento-group",
        enable_auto_commit=True
    )