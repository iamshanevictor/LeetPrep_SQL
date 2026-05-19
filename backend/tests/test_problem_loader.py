from app.services.problem_loader import get_problem, list_problems


def test_list_problems_returns_empty_list_initially():
    assert list_problems() == []


def test_get_problem_returns_none_initially():
    assert get_problem("missing-problem") is None
