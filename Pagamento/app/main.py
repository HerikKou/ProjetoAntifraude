from app.service.PagamentoService import PagamentoService

if __name__ == "__main__":
    print("[Pagamento] Iniciando PagamentoService...")
    service = PagamentoService()
    service.start()