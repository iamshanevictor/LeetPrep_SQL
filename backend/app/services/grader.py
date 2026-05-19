from app.services.sql_runner import SQLExecutionError, run_user_query


def grade_submission(problem, query):
    """Grade a learner's SQL query for a lesson practice or boss problem.

    Args:
        problem: The loaded lesson or problem definition.
        query: The SQL query submitted by the learner.

    Returns:
        A dictionary with correctness, feedback, and result details.
    """
    expected_query = _get_expected_query(problem)
    if expected_query is None:
        return {
            "is_correct": False,
            "feedback": "This lesson does not have an expected query yet.",
            "user_result": None,
            "expected_result": None,
            "error": "Missing expected query.",
        }

    try:
        expected_result = run_user_query(problem, expected_query)
        user_result = run_user_query(problem, query)
    except SQLExecutionError as error:
        return {
            "is_correct": False,
            "feedback": "Your query could not be run safely or successfully.",
            "user_result": None,
            "expected_result": None,
            "error": str(error),
        }

    order_matters = _get_order_matters(problem)
    is_correct = _results_match(user_result, expected_result, order_matters)

    return {
        "is_correct": is_correct,
        "feedback": (
            "Correct. Your query returns the expected result."
            if is_correct
            else "Not quite yet. Compare your output with the expected result."
        ),
        "user_result": user_result,
        "expected_result": None if is_correct else expected_result,
        "error": None,
    }


def _get_expected_query(problem):
    if problem is None:
        return None

    if problem.get("type") == "tutorial_practice":
        return problem.get("practice", {}).get("expected_query")

    return problem.get("expected_query")


def _get_order_matters(problem):
    if problem.get("type") == "tutorial_practice":
        return problem.get("practice", {}).get("order_matters", False)

    return problem.get("order_matters", False)


def _results_match(user_result, expected_result, order_matters):
    if user_result.get("columns") != expected_result.get("columns"):
        return False

    user_rows = user_result.get("rows", [])
    expected_rows = expected_result.get("rows", [])
    if order_matters:
        return user_rows == expected_rows

    return sorted(_row_key(row) for row in user_rows) == sorted(
        _row_key(row) for row in expected_rows
    )


def _row_key(row):
    return tuple(str(value) for value in row)
