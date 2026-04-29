from datetime import datetime
from sqlalchemy.orm import Session
from app.models.Antifraude import Antifraude, SessionLocal, init_db
from app.repository.AntifraudeRepository import AntifraudeRepository
from app.config.Kafka_Config import (
    criar_producer,
    criar_consumer,
    TOPICO_FRAUDE_DETECTADA,
    TOPICO_TRANSACAO_APROVADA
)
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

repository = AntifraudeRepository()


class AntifraudeService:

    def __init__(self):
        self.modelo = self.treinar_modelo()

    def treinar_modelo(self):
        dados = pd.DataFrame({
            "valor": [500, 8000, 200, 15000, 300, 9000, 100, 12000],
            "hora": [14, 2, 10, 3, 16, 1, 9, 4],
            "frequencia": [1, 5, 1, 8, 1, 6, 1, 7],
            "conta_destino_nova": [0, 1, 0, 1, 0, 1, 0, 1],
            "fraude": [0, 1, 0, 1, 0, 1, 0, 1]
        })

        X = dados[["valor", "hora", "frequencia", "conta_destino_nova"]]
        y = dados["fraude"]

        modelo = RandomForestClassifier()
        modelo.fit(X, y)

        return modelo

    def verificar_valor(self, valor):
        if valor > 5000:
            return 30
        return 0

    def verificar_horario(self):
        hora_atual = datetime.utcnow().hour
        if 0 <= hora_atual < 6:
            return 30
        return 0

    def verificar_conta_destino(self, conta_destino, db: Session):
        existe = repository.verificar_conta_destino(db, conta_destino)
        if not existe:
            return 20, 1
        return 0, 0

    def verificar_frequencia(self, conta_origem, db: Session):
        total = repository.verificar_frequencia(db, conta_origem)
        if total > 1:
            return 30, total
        return 0, total

    def calcular_score_ml(self, valor, hora, frequencia, conta_destino_nova):
        features = pd.DataFrame([{
            "valor": valor,
            "hora": hora,
            "frequencia": frequencia,
            "conta_destino_nova": conta_destino_nova
        }])

        probabilidade = self.modelo.predict_proba(features)[0][1]
        return probabilidade * 100

    def calcular_score(self, valor, conta_origem, conta_destino, db: Session):
        score_regras = 0

        score_regras += self.verificar_valor(valor)
        score_regras += self.verificar_horario()

        score_freq, total_freq = self.verificar_frequencia(conta_origem, db)
        score_regras += score_freq

        score_destino, conta_nova = self.verificar_conta_destino(conta_destino, db)
        score_regras += score_destino

        score_ml = self.calcular_score_ml(
            valor,
            datetime.utcnow().hour,
            total_freq,
            conta_nova
        )

        return (score_regras + score_ml) / 2

    def validar_score(self, score):
        if score >= 71:
            return "BLOQUEADA"
        elif score >= 41:
            return "ANALISE_MANUAL"
        return "APROVADA"

    def processar(self):
        init_db()

        consumer = criar_consumer()
        producer = criar_producer()

        print("AntifraudeService iniciado...", flush=True)
        print("Aguardando mensagens Kafka...", flush=True)

        for mensagem in consumer:
            dados = mensagem.value
            db = SessionLocal()

            try:
                score = self.calcular_score(
                    dados["valor"],
                    dados["contaOrigem"],
                    dados["contaDestino"],
                    db
                )

                status = self.validar_score(score)

                antifraude = Antifraude(
                    transacao_id=dados["id"],
                    conta_origem=dados["contaOrigem"],
                    conta_destino=dados["contaDestino"],
                    valor=dados["valor"],
                    score=score,
                    status=status,
                    data_analise=datetime.utcnow()
                )

                repository.salvar(db, antifraude)

                topico = (
                    TOPICO_FRAUDE_DETECTADA
                    if status == "BLOQUEADA"
                    else TOPICO_TRANSACAO_APROVADA
                )

                producer.send(topico, {
                    "transacao_id": dados["id"],
                    "status": status,
                    "score": score
                })

                producer.flush()

                print(f"Transacao {dados['id']} processada — Score: {score:.1f} — Status: {status}", flush=True)

            except Exception as e:
                print(f"Erro ao processar transacao: {str(e)}", flush=True)

            finally:
                db.close()