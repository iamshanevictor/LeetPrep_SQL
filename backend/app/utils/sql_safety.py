import re


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

    keywords = _extract_keywords(normalized)
    if not keywords:
        return False, "Query must contain SQL keywords."

    first_keyword = keywords[0]
    if first_keyword not in ALLOWED_STARTING_KEYWORDS:
        return False, "Only SELECT or WITH queries are allowed."

    blocked_keywords = find_blocked_keywords(normalized)
    if blocked_keywords:
        blocked = ", ".join(sorted(set(blocked_keywords)))
        return False, f"Query contains blocked keyword(s): {blocked}."

    return True, "Query is safe to run."
