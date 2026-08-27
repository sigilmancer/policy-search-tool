import pytest
import os
from httpx import AsyncClient, ASGITransport 
from backend.main import app

@pytest.fixture(autouse=True)
def setup_test_data():
    os.makedirs("data", exist_ok=True)
    test_content = (
        "[SECTION: HOUSING]\n"
        "Hammersmith requires 35% affordable housing for buildings over four stories.\n\n"
        "[SECTION: TRANSPORT]\n"
        "Clean air zones restrict diesel vehicles over 3.5 tonnes at night."
    )
    with open("data/policy_docs.txt", "w") as f:
        f.write(test_content)
    yield
    if os.path.exists("data/policy_docs.txt"):
        os.remove("data/policy_docs.txt")

@pytest.mark.asyncio
async def test_query_endpoint_returns_successful_payload():
    #pass app through the new ASGITransport object
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/query", json={"text": "Hammersmith housing"})
        
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "Hammersmith housing"
    assert "SECTION: HOUSING" in data["answer"]
    assert data["sources_found"] == 1

@pytest.mark.asyncio
async def test_query_endpoint_returns_no_matches_gracefully():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/query", json={"text": "spaceships"})
        
    assert response.status_code == 200
    data = response.json()
    assert "No specific local policy clauses found" in data["answer"]
    assert data["sources_found"] == 0

@pytest.mark.asyncio
async def test_query_endpoint_rejects_empty_strings():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/query", json={"text": "   "})
        
    assert response.status_code == 400
    assert response.json()["detail"] == "Query text cannot be empty."
