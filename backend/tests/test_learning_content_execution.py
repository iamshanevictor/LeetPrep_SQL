from app.services.learning_loader import get_boss_problem, list_lessons, list_modules
from app.services.sql_runner import run_user_query


def test_all_lesson_expected_queries_execute():
    for module in list_modules():
        for lesson in list_lessons(module["id"]):
            practice = lesson["practice"]
            result = run_user_query(lesson, practice["expected_query"])

            assert result["columns"] == practice["expected_columns"]


def test_all_boss_expected_queries_execute():
    for module in list_modules():
        boss_problem = get_boss_problem(module["id"])
        result = run_user_query(boss_problem, boss_problem["expected_query"])

        assert result["columns"] == boss_problem["expected_columns"]
