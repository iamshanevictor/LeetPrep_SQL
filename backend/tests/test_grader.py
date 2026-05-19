from app.services.grader import grade_submission
from app.services.learning_loader import get_lesson


def test_grade_submission_correct_answer():
    lesson = get_lesson("module_01_salary_comparison", "lesson_01_group_by_avg")
    query = (
        "SELECT department_id, SUM(salary) AS total_salary "
        "FROM employees GROUP BY department_id"
    )

    result = grade_submission(lesson, query)

    assert result["is_correct"] is True
    assert result["expected_result"] is None
    assert result["error"] is None


def test_grade_submission_incorrect_answer():
    lesson = get_lesson("module_01_salary_comparison", "lesson_01_group_by_avg")

    result = grade_submission(lesson, "SELECT department_id, salary FROM employees")

    assert result["is_correct"] is False
    assert result["expected_result"] is not None
    assert result["error"] is None
