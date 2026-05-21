from app import create_app


def test_roadmap_endpoint():
    app = create_app()

    with app.test_client() as client:
        response = client.get("/api/roadmap")

    assert response.status_code == 200
    assert response.get_json()["title"] == "Roadmap to Advanced SQL Interview Problems"


def test_module_endpoint_for_module_1():
    app = create_app()

    with app.test_client() as client:
        response = client.get("/api/modules/module_01_salary_comparison")

    data = response.get_json()
    assert response.status_code == 200
    assert len(data["module"]["lessons"]) == 4


def test_lesson_run_endpoint():
    app = create_app()

    with app.test_client() as client:
        response = client.post(
            "/api/modules/module_01_salary_comparison/lessons/lesson_01_group_by_avg/run",
            json={
                "query": (
                    "SELECT department_id, SUM(salary) AS total_salary "
                    "FROM employees GROUP BY department_id"
                )
            },
        )

    assert response.status_code == 200
    assert response.get_json()["result"]["columns"] == ["department_id", "total_salary"]


def test_lesson_detail_includes_expected_output():
    app = create_app()

    with app.test_client() as client:
        response = client.get(
            "/api/modules/module_01_salary_comparison/lessons/lesson_01_group_by_avg"
        )

    data = response.get_json()
    assert response.status_code == 200
    assert data["lesson"]["expected_result"]["columns"] == [
        "department_id",
        "total_salary",
    ]


def test_lesson_schema_column_order_matches_seed_rows():
    app = create_app()

    with app.test_client() as client:
        response = client.get(
            "/api/modules/module_01_salary_comparison/lessons/lesson_01_group_by_avg"
        )

    lesson = response.get_json()["lesson"]
    employees_schema = lesson["schema"][0]

    assert list(employees_schema["columns"].keys()) == [
        "employee_id",
        "employee_name",
        "department_id",
        "salary",
    ]
    assert lesson["seed_data"]["employees"][0] == [1, "Alice", 1, 60000]


def test_boss_submit_endpoint_correct_answer():
    app = create_app()
    query = (
        "WITH department_averages AS ("
        "SELECT d.department_name, AVG(e.salary) AS department_avg_salary "
        "FROM employees e INNER JOIN departments d "
        "ON e.department_id = d.department_id "
        "GROUP BY d.department_name"
        "), company_average AS ("
        "SELECT AVG(salary) AS company_avg_salary FROM employees"
        ") "
        "SELECT da.department_name, da.department_avg_salary, ca.company_avg_salary, "
        "CASE WHEN da.department_avg_salary > ca.company_avg_salary THEN 'higher' "
        "WHEN da.department_avg_salary < ca.company_avg_salary THEN 'lower' "
        "ELSE 'same' END AS comparison_result "
        "FROM department_averages da CROSS JOIN company_average ca"
    )

    with app.test_client() as client:
        response = client.post(
            "/api/modules/module_01_salary_comparison/boss/submit",
            json={"query": query},
        )

    assert response.status_code == 200
    assert response.get_json()["is_correct"] is True
