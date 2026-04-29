import sys
import os
from unittest.mock import Mock, patch

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

from app.service.TransacaoService import TransacaoService


def test_criar_transacao():
    service = TransacaoService()

    db = Mock()

    request = Mock()
    request.conta_origem = "123"
    request.conta_destino = "456"
    request.valor = 1000.0
    request.tipo_transacao = "PIX"

    transacao_mock = Mock()
    transacao_mock.id = 1
    transacao_mock.contaOrigem = "123"
    transacao_mock.contaDestino = "456"
    transacao_mock.valor = 1000.0
    transacao_mock.tipo_transacao = "PIX"

    producer_mock = Mock()

    with patch(
        "app.service.TransacaoService.repository.salvar",
        return_value=transacao_mock
    ):
        with patch(
            "app.service.TransacaoService.criar_producer",
            return_value=producer_mock
        ):
            result = service.criar_transacao(db, request)

    assert result.id == 1
    producer_mock.send.assert_called_once()
    producer_mock.flush.assert_called_once()