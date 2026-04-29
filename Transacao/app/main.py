from fastapi import FastAPI
from app.controller.TransacaoController import router as transacao_router
from app.models.Transacao import init_db

app = FastAPI()
init_db()
app.include_router(transacao_router)
