import pytest

from app.services.learning_loader import get_boss_problem, get_lesson
from app.services import sql_runner
from app.services.sql_runner import SQLExecutionError, run_user_query


def test_duckdb_query_execution_for_lesson():
    lesson = get_lesson("module_01_salary_comparison", "lesson_01_group_by_avg")

    result = run_user_query(
        lesson,
        "SELECT department_id, AVG(salary) AS avg_salary FROM employees GROUP BY department_id",
    )

    assert result["columns"] == ["department_id", "avg_salary"]
    assert [1, 65000.0] in result["rows"]
    assert [2, 85000.0] in result["rows"]


def test_duckdb_query_execution_for_boss_problem():
    boss_problem = get_boss_problem("module_01_salary_comparison")

    result = run_user_query(
        boss_problem,
        "SELECT d.department_name, AVG(e.salary) AS department_avg_salary "
        "FROM employees e INNER JOIN departments d "
        "ON e.department_id = d.department_id "
        "GROUP BY d.department_name",
    )

    assert result["columns"] == ["department_name", "department_avg_salary"]
    assert ["Engineering", 90000.0] in result["rows"]


def test_duckdb_rejects_unsafe_query():
    lesson = get_lesson("module_01_salary_comparison", "lesson_01_group_by_avg")

    with pytest.raises(SQLExecutionError, match="blocked keyword"):
        run_user_query(lesson, "DROP TABLE employees")


def test_duckdb_rejects_query_that_is_too_long(monkeypatch):
    lesson = get_lesson("module_01_salary_comparison", "lesson_01_group_by_avg")
    monkeypatch.setattr(sql_runner, "MAX_QUERY_LENGTH", 10)

    with pytest.raises(SQLExecutionError, match="Query is too long"):
        run_user_query(lesson, "SELECT department_id FROM employees")


def test_duckdb_rejects_too_many_result_rows(monkeypatch):
    lesson = get_lesson("module_01_salary_comparison", "lesson_01_group_by_avg")
    monkeypatch.setattr(sql_runner, "MAX_RESULT_ROWS", 1)

    with pytest.raises(SQLExecutionError, match="too many rows"):
        run_user_query(lesson, "SELECT employee_id FROM employees")
