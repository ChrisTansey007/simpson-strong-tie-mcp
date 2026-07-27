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


@pytest.mark.asyncio
async def test_connection_service_unity_ratio_compliant():
    service = ConnectionService()
    req = ConnectionCheckRequest(
        model_number="H1A",
        required_uplift_lbf=Decimal("372.5"),  # 0.5 ratio (372.5/745)
        required_download_lbf=Decimal("312.5"),  # 0.25 ratio (312.5/1250)
        required_lateral_lbf=Decimal("87"),  # 0.2 ratio (87/435)
    )
    result = await service.check_connection(req)
    assert result.is_compliant is True
    assert result.unity_ratio == Decimal("0.95")
    assert len(result.warnings) == 0
    assert "UNITY_RATIO_EXCEEDED" not in result.elimination_reasons


@pytest.mark.asyncio
async def test_connection_service_unity_ratio_exceeded():
    service = ConnectionService()
    req = ConnectionCheckRequest(
        model_number="H1A",
        required_uplift_lbf=Decimal("745"),  # 1.0 ratio
        required_download_lbf=Decimal("125"),  # 0.1 ratio
        required_lateral_lbf=Decimal("43.5"),  # 0.1 ratio
    )
    result = await service.check_connection(req)
    assert result.is_compliant is False
    assert result.unity_ratio == Decimal("1.2")
    assert "Multi-vector load combination unity ratio" in result.warnings[0]
    assert "UNITY_RATIO_EXCEEDED" in result.elimination_reasons
