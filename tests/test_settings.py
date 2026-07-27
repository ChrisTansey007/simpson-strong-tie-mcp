from simpson_common import get_settings


def test_settings_defaults():
    settings = get_settings()
    assert settings.environment == "local"
    assert settings.postgres_user == "simpson"
    assert "simpson_mcp" in settings.database_url
