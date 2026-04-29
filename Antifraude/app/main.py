from app.service.AntifraudeService import AntifraudeService

if __name__ == "__main__":
    print("AntifraudeService iniciado...")
    service = AntifraudeService()
    service.processar()