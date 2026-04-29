import sys
import os
from unittest.mock import Mock, patch

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

from app.service.AntifraudeService import AntifraudeService


def test_validar_score():
    service = AntifraudeService()

    assert service.validar_score(80) == "BLOQUEADA"
    assert service.validar_score(50) == "ANALISE_MANUAL"
    assert service.validar_score(20) == "APROVADA"


def test_calcular_score():
    service = AntifraudeService()

    db = Mock()

    with patch.object(service, "verificar_valor", return_value=30):
        with patch.object(service, "verificar_horario", return_value=30):
            with patch.object(
                service,
                "verificar_frequencia",
                return_value=(30, 2)
            ):
                with patch.object(
                    service,
                    "verificar_conta_destino",
                    return_value=(20, 1)
                ):
                    with patch.object(
                        service,
                        "calcular_score_ml",
                        return_value=80
                    ):
                        score = service.calcular_score(
                            10000,
                            "123",
                            "456",
                            db
                        )

    assert score == 95