from app import create_app


def test_problem_list_is_empty_initially():
    app = create_app()

    with app.test_client() as client:
        response = client.get("/api/problems")

    assert response.status_code == 200
    assert response.get_json() == {"problems": []}


def test_problem_detail_returns_placeholder_404():
    app = create_app()

    with app.test_client() as client:
        response = client.get("/api/problems/example")

    assert response.status_code == 404
    assert response.get_json() == {
        "error": "Problem not found",
        "message": "Practice problems have not been added yet.",
    }


def test_problem_run_returns_placeholder_501():
    app = create_app()

    with app.test_client() as client:
        response = client.post("/api/problems/example/run", json={"query": "SELECT 1"})

    assert response.status_code == 501
    assert response.get_json() == {
        "error": "Not implemented",
        "message": "SQL execution will be added after the problem format is finalized.",
    }


def test_problem_submit_returns_placeholder_501():
    app = create_app()

    with app.test_client() as client:
        response = client.post("/api/problems/example/submit", json={"query": "SELECT 1"})

    assert response.status_code == 501
    assert response.get_json() == {
        "error": "Not implemented",
        "message": "Grading will be added after the problem format is finalized.",
    }
