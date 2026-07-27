from decimal import Decimal

import pytest
from simpson_domain.enums import (
    CoatingType,
    EnvironmentClassification,
    FastenerType,
)
from simpson_domain.models import ConnectionCheckRequest
from simpson_engineering import ConnectionService, CorrosionService, FastenerService


@pytest.mark.asyncio
async def test_connection_service_prohibited_generic_deck_screws():
    service = ConnectionService()
    req = ConnectionCheckRequest(
        model_number="H1A",
        required_uplift_lbf=Decimal("500"),
        fastener_override=FastenerType.GENERIC_DECK_SCREW,
    )
    result = await service.check_connection(req)
    assert result.is_compliant is False
    assert "PROHIBITED_FASTENER_GENERIC_DECK_SCREW" in result.elimination_reasons


@pytest.mark.asyncio
async def test_connection_service_coastal_corrosion_suitability():
    service = ConnectionService()
    req = ConnectionCheckRequest(
        model_number="H1A",
        required_uplift_lbf=Decimal("500"),
        environment=EnvironmentClassification.COASTAL_HIGH_CORROSION,
    )
    result = await service.check_connection(req)
    assert result.is_compliant is False
    assert "INSUFFICIENT_CORROSION_RESISTANCE" in result.elimination_reasons


def test_fastener_substitution_rules():
    service = FastenerService()
    ok, msg = service.check_substitution(FastenerType.NAIL_COMMON_10D, FastenerType.SCREW_SD9)
    assert ok is True
    assert "approved 1-to-1 replacement" in msg

    ok_prohibited, msg_prohibited = service.check_substitution(
        FastenerType.NAIL_COMMON_10D, FastenerType.GENERIC_DECK_SCREW
    )
    assert ok_prohibited is False
    assert "PROHIBITED" in msg_prohibited


def test_corrosion_suitability_rules():
    service = CorrosionService()
    ok_ss, msg_ss = service.check_coating_suitability(
        CoatingType.STAINLESS_316, EnvironmentClassification.COASTAL_HIGH_CORROSION
    )
    assert ok_ss is True

    ok_g90, msg_g90 = service.check_coating_suitability(
        CoatingType.STANDARD_GALVANIZED, EnvironmentClassification.COASTAL_HIGH_CORROSION
    )
    assert ok_g90 is False
