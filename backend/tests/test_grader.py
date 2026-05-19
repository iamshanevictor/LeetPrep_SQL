import pytest

from app.services.grader import grade_submission


def test_grade_submission_is_placeholder():
    with pytest.raises(NotImplementedError, match="Grading will be added"):
        grade_submission(problem=None, query="SELECT 1")
