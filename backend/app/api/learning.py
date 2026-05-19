from flask import Blueprint, jsonify, request

from app.services.grader import grade_submission
from app.services.learning_loader import (
    get_boss_problem,
    get_lesson,
    get_module,
    list_modules,
    load_roadmap,
)
from app.services.sql_runner import SQLExecutionError, run_user_query


learning_bp = Blueprint("learning", __name__)


@learning_bp.get("/roadmap")
def roadmap():
    """Return the full learning roadmap overview."""
    return jsonify(load_roadmap())


@learning_bp.get("/modules")
def modules():
    """Return all learning modules in roadmap order."""
    return jsonify({"modules": list_modules()})


@learning_bp.get("/modules/<module_id>")
def module_detail(module_id):
    """Return module metadata plus authored lessons and boss summary."""
    module = get_module(module_id)
    if module is None:
        return jsonify({"error": "Module not found"}), 404

    return jsonify({"module": module})


@learning_bp.get("/modules/<module_id>/lessons/<lesson_id>")
def lesson_detail(module_id, lesson_id):
    """Return a full lesson."""
    lesson = get_lesson(module_id, lesson_id)
    if lesson is None:
        return jsonify({"error": "Lesson not found"}), 404

    return jsonify({"lesson": lesson})


@learning_bp.post("/modules/<module_id>/lessons/<lesson_id>/run")
def run_lesson_query(module_id, lesson_id):
    """Run a SQL query against a lesson's seed data."""
    lesson = get_lesson(module_id, lesson_id)
    if lesson is None:
        return jsonify({"error": "Lesson not found"}), 404

    query = (request.get_json(silent=True) or {}).get("query", "")
    try:
        result = run_user_query(lesson, query)
    except SQLExecutionError as error:
        return jsonify({"error": "SQL execution failed", "message": str(error)}), 400

    return jsonify({"result": result})


@learning_bp.post("/modules/<module_id>/lessons/<lesson_id>/submit")
def submit_lesson_query(module_id, lesson_id):
    """Grade a SQL query for a lesson practice task."""
    lesson = get_lesson(module_id, lesson_id)
    if lesson is None:
        return jsonify({"error": "Lesson not found"}), 404

    query = (request.get_json(silent=True) or {}).get("query", "")
    return jsonify(grade_submission(lesson, query))


@learning_bp.get("/modules/<module_id>/boss")
def boss_problem_detail(module_id):
    """Return a full boss problem."""
    boss_problem = get_boss_problem(module_id)
    if boss_problem is None:
        return jsonify({"error": "Boss problem not found"}), 404

    return jsonify({"boss_problem": boss_problem})


@learning_bp.post("/modules/<module_id>/boss/run")
def run_boss_query(module_id):
    """Run a SQL query against a boss problem's seed data."""
    boss_problem = get_boss_problem(module_id)
    if boss_problem is None:
        return jsonify({"error": "Boss problem not found"}), 404

    query = (request.get_json(silent=True) or {}).get("query", "")
    try:
        result = run_user_query(boss_problem, query)
    except SQLExecutionError as error:
        return jsonify({"error": "SQL execution failed", "message": str(error)}), 400

    return jsonify({"result": result})


@learning_bp.post("/modules/<module_id>/boss/submit")
def submit_boss_query(module_id):
    """Grade a SQL query for a boss problem."""
    boss_problem = get_boss_problem(module_id)
    if boss_problem is None:
        return jsonify({"error": "Boss problem not found"}), 404

    query = (request.get_json(silent=True) or {}).get("query", "")
    return jsonify(grade_submission(boss_problem, query))
