from app import create_app


class CorsTestConfig:
    APP_NAME = "LeetPrep-SQL"
    SECRET_KEY = "test"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    PROBLEMS_DIR = "problems"
    CORS_ORIGINS = ["https://frontend.example.com"]


def test_health_check():
    app = create_app()

    with app.test_client() as client:
        response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "app": "LeetPrep-SQL"}


def test_cors_allows_configured_origin():
    app = create_app(CorsTestConfig)

    with app.test_client() as client:
        response = client.get(
            "/api/health",
            headers={"Origin": "https://frontend.example.com"},
        )

    assert response.headers["Access-Control-Allow-Origin"] == "https://frontend.example.com"


def test_cors_rejects_unconfigured_origin():
    app = create_app(CorsTestConfig)

    with app.test_client() as client:
        response = client.get(
            "/api/health",
            headers={"Origin": "https://not-allowed.example.com"},
        )

    assert "Access-Control-Allow-Origin" not in response.headers
