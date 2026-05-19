from app.services.learning_loader import (
    get_boss_problem,
    get_lesson,
    get_module,
    list_lessons,
    list_modules,
    load_roadmap,
)


def test_load_roadmap():
    roadmap = load_roadmap()

    assert roadmap["title"] == "Roadmap to Advanced SQL Interview Problems"
    assert len(roadmap["modules"]) == 10


def test_list_modules_in_order():
    modules = list_modules()

    assert modules[0]["id"] == "module_01_salary_comparison"
    assert modules[-1]["id"] == "module_10_consecutive_numbers"


def test_load_module_1_lessons():
    lessons = list_lessons("module_01_salary_comparison")

    assert [lesson["id"] for lesson in lessons] == [
        "lesson_01_group_by_avg",
        "lesson_02_join_departments",
        "lesson_03_case_when",
        "lesson_04_cte",
    ]


def test_get_module_includes_lessons_and_boss_summary():
    module = get_module("module_01_salary_comparison")

    assert module["lessons_count"] == 4
    assert len(module["lessons"]) == 4
    assert module["boss_problem"]["id"] == "boss_problem"


def test_placeholder_module_has_no_lessons():
    module = get_module("module_02_quiet_students")

    assert module["lessons"] == []
    assert module["boss_problem"] is None


def test_get_lesson_and_boss_problem():
    lesson = get_lesson("module_01_salary_comparison", "lesson_01_group_by_avg")
    boss_problem = get_boss_problem("module_01_salary_comparison")

    assert lesson["title"] == "Calculate Average Salary by Department"
    assert boss_problem["type"] == "boss_problem"
