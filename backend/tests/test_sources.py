from fastapi.testclient import TestClient


def test_get_sources_returns_belgian_news_sources(client: TestClient):
    """GET /sources returns the configured Belgian news sources."""
    response = client.get("/sources")
    assert response.status_code == 200

    sources = response.json()
    assert isinstance(sources, list)
    assert len(sources) == 9

    # Check structure of first source
    source = sources[0]
    assert "id" in source
    assert "name" in source
    assert "url" in source
    assert "source_language" in source

    # Check we have both Dutch and French sources
    names = {s["name"] for s in sources}
    assert "De Standaard" in names
    assert "Le Soir" in names
    assert "VRT NWS" in names

    # Check source languages are set
    for source in sources:
        assert source["source_language"] in ("nl", "fr")
