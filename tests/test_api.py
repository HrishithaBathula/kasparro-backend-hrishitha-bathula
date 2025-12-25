# from fastapi.testclient import TestClient
# from api.main import app

# client = TestClient(app)


# def test_health_endpoint():
#     response = client.get("/health")
#     assert response.status_code == 200

#     data = response.json()
#     assert data["status"] == "ok"
#     assert "api_latency_ms" in data

# def test_stats_endpoint():
#     response = client.get("/stats")
#     assert response.status_code == 200
#     assert "etl_sources" in response.json()
from fastapi.testclient import TestClient
from api.main import app
from core.database import get_db

client = TestClient(app)


# ---- MOCK DB FOR API TESTS ----
class FakeResult:
    def mappings(self):
        return self

    def all(self):
        return [
            {
                "source": "coinpaprika",
                "last_processed_at": "2025-01-01T00:00:00",
                "last_success": "2025-01-01T00:00:00",
                "last_failure": None,
                "is_running": False,
            }
        ]


class FakeDB:
    def execute(self, query):
        return FakeResult()

    def close(self):
        pass


def override_get_db():
    yield FakeDB()


app.dependency_overrides[get_db] = override_get_db
# --------------------------------


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_stats_endpoint():
    response = client.get("/stats")
    assert response.status_code == 200
    assert "etl_sources" in response.json()
    assert len(response.json()["etl_sources"]) > 0
