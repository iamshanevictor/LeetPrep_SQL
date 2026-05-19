from app.services.learning_loader import get_boss_problem, get_lesson


def list_problems():
    """Return all available SQL practice problem summaries.

    Practice problem JSON files have not been added yet, so the initial
    scaffold returns an empty list.
    """
    return []


def get_problem(problem_id):
    """Return one standalone or learning-content problem by id.

    Args:
        problem_id: A future standalone id, or a learning content id formatted
            as learning:<module_id>:lesson:<lesson_id> or learning:<module_id>:boss.

    Returns:
        A loaded learning content item when supported, otherwise None.
    """
    parts = problem_id.split(":")
    if len(parts) == 4 and parts[0] == "learning" and parts[2] == "lesson":
        return get_lesson(parts[1], parts[3])

    if len(parts) == 3 and parts[0] == "learning" and parts[2] == "boss":
        return get_boss_problem(parts[1])

    return None
