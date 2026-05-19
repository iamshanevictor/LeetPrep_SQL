def run_user_query(problem, query):
    """Run a learner's SQL query against a future DuckDB problem database.

    Args:
        problem: The loaded problem definition.
        query: The SQL query submitted by the learner.

    Raises:
        NotImplementedError: Until DuckDB execution is added.
    """
    raise NotImplementedError(
        "SQL execution will be added after the problem format is finalized."
    )
