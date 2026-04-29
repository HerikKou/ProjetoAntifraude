from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.Service.TransacaoService import TransacaoService
from app.dto.TransacaoDto import TransacaoRequest, TransacaoResponse
from app.models.Transacao import get_db

router = APIRouter()
service = TransacaoService()

@router.post("/transacao", response_model=TransacaoResponse)
def criar_transacao(request: TransacaoRequest, db: Session = Depends(get_db)):
    transacao = service.criar_transacao(db, request)
    return transacao
