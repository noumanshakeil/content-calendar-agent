import pytest
@pytest.mark.asyncio
async def test_plan_week(client):
    r = await client.post("/api/posts/plan-week", json={"theme": "local LLM tips", "channel": "linkedin"})
    assert r.status_code == 200
    assert r.json()["created"] >= 1
