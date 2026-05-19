from app.utils.sql_safety import (
    find_blocked_keywords,
    is_select_only_query,
    normalize_sql,
    validate_safe_sql,
)


def test_normalize_sql_collapses_whitespace():
    assert normalize_sql(" SELECT   *\nFROM users ") == "SELECT * FROM users"


def test_select_query_is_safe():
    assert is_select_only_query("SELECT * FROM users") is True
    assert validate_safe_sql("SELECT * FROM users") == (True, "Query is safe to run.")


def test_with_query_is_safe():
    query = "WITH cte AS (SELECT * FROM users) SELECT * FROM cte"
    assert is_select_only_query(query) is True
    assert validate_safe_sql(query) == (True, "Query is safe to run.")


def test_drop_query_is_unsafe():
    is_safe, message = validate_safe_sql("DROP TABLE users")

    assert is_safe is False
    assert message == "Only SELECT or WITH queries are allowed."
    assert find_blocked_keywords("DROP TABLE users") == ["DROP"]


def test_blocked_keyword_inside_select_is_unsafe():
    is_safe, message = validate_safe_sql("SELECT * FROM users; DELETE FROM users")

    assert is_safe is False
    assert message == "Query contains blocked keyword(s): DELETE."
