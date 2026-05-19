import json
from functools import lru_cache
from pathlib import Path


LEARNING_CONTENT_DIR = Path(__file__).resolve().parents[2] / "learning_content"
MODULES_DIR = LEARNING_CONTENT_DIR / "modules"


def _load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


@lru_cache(maxsize=1)
def load_roadmap():
    """Load the roadmap overview from JSON content."""
    return _load_json(LEARNING_CONTENT_DIR / "roadmap.json")


def list_modules():
    """Return module metadata in roadmap order."""
    modules = load_roadmap().get("modules", [])
    return sorted(modules, key=lambda module: module.get("order", 0))


def get_module(module_id):
    """Return one module with available lesson and boss summaries."""
    module = next(
        (module for module in list_modules() if module.get("id") == module_id),
        None,
    )
    if module is None:
        return None

    module_detail = dict(module)
    module_detail["lessons"] = [_lesson_summary(lesson) for lesson in list_lessons(module_id)]

    boss_problem = get_boss_problem(module_id)
    module_detail["boss_problem"] = _boss_summary(boss_problem) if boss_problem else None

    return module_detail


def list_lessons(module_id):
    """Return full lessons for a module when lesson JSON files exist."""
    module_dir = MODULES_DIR / module_id
    if not module_dir.exists():
        return []

    lessons = [
        _load_json(path)
        for path in module_dir.glob("lesson_*.json")
        if path.is_file()
    ]
    return sorted(lessons, key=lambda lesson: lesson.get("order", lesson.get("id", "")))


def get_lesson(module_id, lesson_id):
    """Return a single lesson by module id and lesson id."""
    lesson_path = MODULES_DIR / module_id / f"{lesson_id}.json"
    if not lesson_path.exists():
        return None

    return _load_json(lesson_path)


def get_boss_problem(module_id):
    """Return a module boss problem when it has been authored."""
    boss_path = MODULES_DIR / module_id / "boss_problem.json"
    if not boss_path.exists():
        return None

    return _load_json(boss_path)


def _lesson_summary(lesson):
    return {
        "id": lesson.get("id"),
        "module_id": lesson.get("module_id"),
        "type": lesson.get("type"),
        "title": lesson.get("title"),
        "difficulty": lesson.get("difficulty"),
        "concepts": lesson.get("concepts", []),
        "estimated_minutes": lesson.get("estimated_minutes"),
        "learning_objective": lesson.get("learning_objective"),
        "order": lesson.get("order"),
    }


def _boss_summary(boss_problem):
    return {
        "id": boss_problem.get("id", "boss_problem"),
        "module_id": boss_problem.get("module_id"),
        "type": boss_problem.get("type"),
        "title": boss_problem.get("title"),
        "difficulty": boss_problem.get("difficulty"),
        "concepts": boss_problem.get("concepts", []),
        "estimated_minutes": boss_problem.get("estimated_minutes"),
        "prerequisites": boss_problem.get("prerequisites", []),
    }
