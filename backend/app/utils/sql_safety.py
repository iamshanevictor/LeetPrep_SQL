import re

import sqlglot
from sqlglot import exp


BLOCKED_KEYWORDS = {
    "DROP",
    "DELETE",
    "UPDATE",
    "INSERT",
    "ALTER",
    "CREATE",
    "ATTACH",
    "COPY",
    "PRAGMA",
    "EXPORT",
    "IMPORT",
}

ALLOWED_STARTING_KEYWORDS = {"SELECT", "WITH"}
BLOCKED_EXPRESSIONS = (
    exp.Alter,
    exp.Command,
    exp.Create,
    exp.Delete,
    exp.Drop,
    exp.Insert,
    exp.Update,
)
BLOCKED_FUNCTIONS = {
    "glob",
    "parquet_scan",
    "parquetscan",
    "read_blob",
    "readblob",
    "read_csv",
    "readcsv",
    "read_json",
    "readjson",
    "read_ndjson",
    "readndjson",
    "read_parquet",
    "readparquet",
    "read_text",
    "readtext",
    "sqlite_scan",
    "sqlitescan",
}


def normalize_sql(query):
    """Collapse whitespace and strip leading/trailing spaces from a SQL query."""
    return re.sub(r"\s+", " ", query or "").strip()


def _extract_keywords(query):
    return re.findall(r"\b[A-Za-z_]+\b", query.upper())


def find_blocked_keywords(query):
    """Return blocked SQL keywords found in the query."""
    keywords = _extract_keywords(query)
    return [keyword for keyword in keywords if keyword in BLOCKED_KEYWORDS]


def is_select_only_query(query):
    """Return True when a query starts with SELECT or WITH and has no blocked keywords."""
    normalized = normalize_sql(query)
    if not normalized:
        return False

    first_keyword = _extract_keywords(normalized)[0] if _extract_keywords(normalized) else ""
    return first_keyword in ALLOWED_STARTING_KEYWORDS and not find_blocked_keywords(normalized)


def validate_safe_sql(query):
    """Validate that a learner query is safe enough for future read-only execution.

    Returns:
        A tuple of (is_safe, message).
    """
    normalized = normalize_sql(query)
    if not normalized:
        return False, "Query cannot be empty."

    blocked_keywords = find_blocked_keywords(normalized)
    if blocked_keywords:
        blocked = ", ".join(sorted(set(blocked_keywords)))
        return False, f"Query contains blocked keyword(s): {blocked}."

    try:
        statements = sqlglot.parse(normalized, read="duckdb")
    except sqlglot.errors.ParseError:
        return False, "Query could not be parsed as SQL."

    statements = [statement for statement in statements if statement is not None]
    if len(statements) != 1:
        return False, "Only one SELECT or WITH query is allowed."

    statement = statements[0]
    if not isinstance(statement, (exp.Select, exp.Union)):
        return False, "Only SELECT or WITH queries are allowed."

    blocked_expression = _find_blocked_expression(statement)
    if blocked_expression is not None:
        return False, f"Query contains blocked SQL operation: {blocked_expression}."

    blocked_function = _find_blocked_function(statement)
    if blocked_function is not None:
        return False, f"Query contains blocked function: {blocked_function}."

    return True, "Query is safe to run."


def _find_blocked_expression(statement):
    for node in statement.walk():
        if isinstance(node, BLOCKED_EXPRESSIONS):
            return node.key.upper()

    return None


def _find_blocked_function(statement):
    for node in statement.walk():
        function_name = (getattr(node, "key", "") or getattr(node, "name", "")).lower()
        if function_name in BLOCKED_FUNCTIONS:
            return function_name

    return None
