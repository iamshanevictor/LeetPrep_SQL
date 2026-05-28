"""Validate roadmap lesson JSON before release.

Run from the backend directory:
    python scripts/validate_learning_content.py
"""

from pathlib import Path
import sys


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.services.learning_loader import (  # noqa: E402
    get_boss_problem,
    list_lessons,
    list_modules,
    load_roadmap,
)
from app.services.sql_runner import SQLExecutionError, run_user_query  # noqa: E402


LESSON_REQUIRED_FIELDS = {
    "id",
    "module_id",
    "order",
    "type",
    "title",
    "difficulty",
    "concepts",
    "estimated_minutes",
    "learning_objective",
    "tutorial",
    "schema",
    "seed_data",
    "guided_example",
    "practice",
    "hints",
}

BOSS_REQUIRED_FIELDS = {
    "id",
    "module_id",
    "type",
    "title",
    "difficulty",
    "concepts",
    "estimated_minutes",
    "prerequisites",
    "prompt",
    "schema",
    "seed_data",
    "expected_query",
    "expected_columns",
    "order_matters",
    "explanation",
    "hints",
    "common_mistakes",
}


def validate_learning_content():
    """Return a list of validation errors for roadmap, lessons, and boss problems."""
    errors = []
    roadmap = load_roadmap()
    modules = list_modules()

    if not roadmap.get("title"):
        errors.append("roadmap.json: missing title")

    module_ids = [module.get("id") for module in modules]
    if len(module_ids) != len(set(module_ids)):
        errors.append("roadmap.json: module ids must be unique")

    for expected_order, module in enumerate(modules, start=1):
        module_id = module.get("id")
        if module.get("order") != expected_order:
            errors.append(f"{module_id}: expected order {expected_order}")

        lessons = list_lessons(module_id)
        if len(lessons) != module.get("lessons_count"):
            errors.append(
                f"{module_id}: lessons_count is {module.get('lessons_count')} "
                f"but {len(lessons)} lesson files were found"
            )

        lesson_ids = [lesson.get("id") for lesson in lessons]
        if len(lesson_ids) != len(set(lesson_ids)):
            errors.append(f"{module_id}: lesson ids must be unique")

        for lesson in lessons:
            errors.extend(_validate_lesson(module_id, lesson))

        boss_problem = get_boss_problem(module_id)
        if boss_problem is None:
            errors.append(f"{module_id}: missing boss_problem.json")
        else:
            errors.extend(
                _validate_boss_problem(
                    module_id,
                    boss_problem,
                    set(lesson_ids),
                    set(module_ids),
                )
            )

    return errors


def _validate_lesson(module_id, lesson):
    errors = _missing_field_errors(f"{module_id}/{lesson.get('id')}", lesson, LESSON_REQUIRED_FIELDS)

    if lesson.get("module_id") != module_id:
        errors.append(f"{module_id}/{lesson.get('id')}: module_id does not match folder")

    if lesson.get("type") != "tutorial_practice":
        errors.append(f"{module_id}/{lesson.get('id')}: type must be tutorial_practice")

    errors.extend(_validate_schema_and_seed_data(module_id, lesson))

    practice = lesson.get("practice", {})
    for field in ["prompt", "expected_query", "expected_columns", "order_matters"]:
        if field not in practice:
            errors.append(f"{module_id}/{lesson.get('id')}: practice missing {field}")

    errors.extend(
        _validate_expected_query(
            f"{module_id}/{lesson.get('id')}",
            lesson,
            practice.get("expected_query"),
            practice.get("expected_columns"),
        )
    )
    return errors


def _validate_boss_problem(module_id, boss_problem, lesson_ids, module_ids):
    errors = _missing_field_errors(
        f"{module_id}/boss_problem",
        boss_problem,
        BOSS_REQUIRED_FIELDS,
    )

    if boss_problem.get("module_id") != module_id:
        errors.append(f"{module_id}/boss_problem: module_id does not match folder")

    if boss_problem.get("type") != "boss_problem":
        errors.append(f"{module_id}/boss_problem: type must be boss_problem")

    allowed_prerequisites = lesson_ids | module_ids
    missing_prerequisites = sorted(
        set(boss_problem.get("prerequisites", [])) - allowed_prerequisites
    )
    if missing_prerequisites:
        errors.append(
            f"{module_id}/boss_problem: prerequisites not found: "
            f"{', '.join(missing_prerequisites)}"
        )

    errors.extend(_validate_schema_and_seed_data(module_id, boss_problem))
    errors.extend(
        _validate_expected_query(
            f"{module_id}/boss_problem",
            boss_problem,
            boss_problem.get("expected_query"),
            boss_problem.get("expected_columns"),
        )
    )
    return errors


def _missing_field_errors(label, content, required_fields):
    return [
        f"{label}: missing {field}"
        for field in sorted(required_fields)
        if field not in content
    ]


def _validate_schema_and_seed_data(module_id, content):
    errors = []
    label = f"{module_id}/{content.get('id')}"
    schema = content.get("schema", [])
    seed_data = content.get("seed_data", {})

    if not isinstance(schema, list) or not schema:
        return [f"{label}: schema must be a non-empty list"]

    for table in schema:
        table_name = table.get("table_name")
        columns = table.get("columns")
        if not table_name:
            errors.append(f"{label}: schema table missing table_name")
            continue
        if not isinstance(columns, dict) or not columns:
            errors.append(f"{label}/{table_name}: columns must be a non-empty object")
            continue

        for row_index, row in enumerate(seed_data.get(table_name, []), start=1):
            if len(row) != len(columns):
                errors.append(
                    f"{label}/{table_name}: seed row {row_index} has {len(row)} values "
                    f"but schema has {len(columns)} columns"
                )

    return errors


def _validate_expected_query(label, content, expected_query, expected_columns):
    if not expected_query:
        return [f"{label}: missing expected query"]

    if not expected_columns:
        return [f"{label}: missing expected columns"]

    try:
        result = run_user_query(content, expected_query)
    except SQLExecutionError as error:
        return [f"{label}: expected query failed: {error}"]

    if result["columns"] != expected_columns:
        return [
            f"{label}: expected columns {expected_columns} do not match query columns "
            f"{result['columns']}"
        ]

    return []


def main():
    errors = validate_learning_content()
    if errors:
        print("Learning content validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("Learning content validation passed.")


if __name__ == "__main__":
    main()
