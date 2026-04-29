import sys
import os
from unittest.mock import Mock

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

from app.service.PagamentoService import PagamentoService


def test_processar_mensagem():
    service = PagamentoService()

    mensagem = Mock()
    mensagem.value = {
        "transacao_id": 1,
        "status": "APROVADA",
        "score": 15.0
    }

    db_mock = Mock()

    from unittest.mock import patch

    with patch(
        "app.service.PagamentoService.SessionLocal",
        return_value=db_mock
    ):
        with patch(
            "app.service.PagamentoService.repository.salvar"
        ) as salvar_mock:
            service.processar_mensagem(mensagem)

    salvar_mock.assert_called_once()
    db_mock.close.assert_called_once()