import time
from datetime import datetime

from app.models.Pagamento import Pagamento, SessionLocal, init_db
from app.repository.PagamentoRepository import PagamentoRepository
from app.config.Kafka_Config import criar_consumer_aprovada

repository = PagamentoRepository()


class PagamentoService:

    def inicializar_banco(self):
        for i in range(10):
            try:
                init_db()
                print("[Pagamento] Banco inicializado")
                return
            except Exception as e:
                print(f"[Pagamento] erro init DB: {e}")
                time.sleep(3)

        raise Exception("Falha ao inicializar banco")

    def run_consumer(self):
        consumer = criar_consumer_aprovada()
        print("[Pagamento] Consumer iniciado, aguardando mensagens...")

        for mensagem in consumer:
            self.processar_mensagem(mensagem)

    def processar_mensagem(self, mensagem):
        dados = mensagem.value
        print(f"[Pagamento] Recebido: {dados}")

        db = SessionLocal()

        try:
            pagamento = Pagamento(
                transacao_id=dados["transacao_id"],
                status="PAGO",
                score_fraude=dados.get("score"),
                tipo_pagamento="PIX",
                data_pagamento=datetime.utcnow()
            )

            repository.salvar(db, pagamento)

            print(f"[Pagamento] Transacao {dados['transacao_id']} paga com sucesso")

        except Exception as e:
            print(f"[Pagamento] erro ao processar: {e}")

        finally:
            db.close()

    def start(self):
        self.inicializar_banco()
        self.run_consumer()