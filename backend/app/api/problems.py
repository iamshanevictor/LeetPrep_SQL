from flask import Blueprint, jsonify, request

from app.services.grader import grade_submission
from app.services.problem_loader import get_problem, list_problems
from app.services.sql_runner import run_user_query


problems_bp = Blueprint("problems", __name__)


@problems_bp.get("/problems")
def get_problems():
    """Return the currently available practice problems."""
    return jsonify({"problems": list_problems()})


@problems_bp.get("/problems/<problem_id>")
def get_problem_detail(problem_id):
    """Return one practice problem when problem files exist."""
    problem = get_problem(problem_id)
    if problem is None:
        return (
            jsonify(
                {
                    "error": "Problem not found",
                    "message": "Practice problems have not been added yet.",
                }
            ),
            404,
        )

    return jsonify({"problem": problem})


@problems_bp.post("/problems/<problem_id>/run")
def run_problem_query(problem_id):
    """Placeholder endpoint for future DuckDB-backed query execution."""
    problem = get_problem(problem_id)
    query = (request.get_json(silent=True) or {}).get("query", "")

    if problem is None:
        return (
            jsonify(
                {
                    "error": "Not implemented",
                    "message": "SQL execution will be added after the problem format is finalized.",
                }
            ),
            501,
        )

    try:
        result = run_user_query(problem, query)
    except NotImplementedError:
        return (
            jsonify(
                {
                    "error": "Not implemented",
                    "message": "SQL execution will be added after the problem format is finalized.",
                }
            ),
            501,
        )

    return jsonify({"result": result})


@problems_bp.post("/problems/<problem_id>/submit")
def submit_problem_query(problem_id):
    """Placeholder endpoint for future automated grading."""
    problem = get_problem(problem_id)
    query = (request.get_json(silent=True) or {}).get("query", "")

    if problem is None:
        return (
            jsonify(
                {
                    "error": "Not implemented",
                    "message": "Grading will be added after the problem format is finalized.",
                }
            ),
            501,
        )

    try:
        result = grade_submission(problem, query)
    except NotImplementedError:
        return (
            jsonify(
                {
                    "error": "Not implemented",
                    "message": "Grading will be added after the problem format is finalized.",
                }
            ),
            501,
        )

    return jsonify({"result": result})
