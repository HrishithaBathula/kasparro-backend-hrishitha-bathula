from fastapi.testclient import TestClient
from api.main import app
from core.database import get_db

client = TestClient(app)


# ---- BROKEN DB MOCK ----
class BrokenDB:
    def execute(self, *args, **kwargs):
        raise Exception("Database unavailable")

    def close(self):
        pass


def broken_db():
    yield BrokenDB()


def test_health_db_failure():
    # Override DB dependency
    app.dependency_overrides[get_db] = broken_db

    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["db"] == "disconnected"

    # Cleanup to avoid test leakage
    app.dependency_overrides.clear()
