import os
import threading

import duckdb

from app.utils.sql_safety import validate_safe_sql


class SQLExecutionError(Exception):
    """Raised when a learner query cannot be executed safely."""


MAX_QUERY_LENGTH = int(os.getenv("SQL_MAX_QUERY_LENGTH", "5000"))
MAX_RESULT_ROWS = int(os.getenv("SQL_MAX_RESULT_ROWS", "200"))
QUERY_TIMEOUT_SECONDS = float(os.getenv("SQL_QUERY_TIMEOUT_SECONDS", "5"))
DUCKDB_MEMORY_LIMIT = os.getenv("DUCKDB_MEMORY_LIMIT", "128MB")


def run_user_query(problem, query):
    """Run a learner's SQL query against an in-memory DuckDB database.

    Args:
        problem: The loaded lesson or problem definition.
        query: The SQL query submitted by the learner.

    Returns:
        A dictionary with result columns and rows.
    """
    if problem is None:
        raise SQLExecutionError("Problem content could not be found.")

    if len(query or "") > MAX_QUERY_LENGTH:
        raise SQLExecutionError(
            f"Query is too long. Keep it under {MAX_QUERY_LENGTH} characters."
        )

    is_safe, message = validate_safe_sql(query)
    if not is_safe:
        raise SQLExecutionError(message)

    try:
        with duckdb.connect(database=":memory:") as connection:
            _configure_connection(connection)
            _create_tables(connection, problem.get("schema", []))
            _insert_seed_data(connection, problem.get("schema", []), problem.get("seed_data", {}))
            columns, rows = _execute_limited_query(connection, query)
    except duckdb.Error as error:
        raise SQLExecutionError(str(error)) from error

    return {
        "columns": columns,
        "rows": [[_serialize_value(value) for value in row] for row in rows],
    }


def _configure_connection(connection):
    connection.execute("PRAGMA enable_progress_bar=false")
    connection.execute("SET threads=1")
    connection.execute(f"SET memory_limit = '{DUCKDB_MEMORY_LIMIT}'")


def _execute_limited_query(connection, query):
    timed_out = threading.Event()

    def interrupt_query():
        timed_out.set()
        connection.interrupt()

    timer = threading.Timer(QUERY_TIMEOUT_SECONDS, interrupt_query)
    timer.daemon = True
    timer.start()

    try:
        cursor = connection.execute(query)
        rows = cursor.fetchmany(MAX_RESULT_ROWS + 1)
        columns = [description[0] for description in cursor.description or []]
    except duckdb.Error as error:
        if timed_out.is_set():
            raise SQLExecutionError(
                f"Query exceeded the {QUERY_TIMEOUT_SECONDS:g} second execution limit."
            ) from error
        raise
    finally:
        timer.cancel()

    if timed_out.is_set():
        raise SQLExecutionError(
            f"Query exceeded the {QUERY_TIMEOUT_SECONDS:g} second execution limit."
        )

    if len(rows) > MAX_RESULT_ROWS:
        raise SQLExecutionError(
            f"Query returned too many rows. Limit results to {MAX_RESULT_ROWS} rows or fewer."
        )

    return columns, rows


def _create_tables(connection, schema):
    for table in schema:
        table_name = _quote_identifier(table["table_name"])
        columns = [
            f"{_quote_identifier(column_name)} {column_type}"
            for column_name, column_type in table["columns"].items()
        ]
        connection.execute(f"CREATE TABLE {table_name} ({', '.join(columns)})")


def _insert_seed_data(connection, schema, seed_data):
    for table in schema:
        table_name = table["table_name"]
        rows = seed_data.get(table_name, [])
        if not rows:
            continue

        quoted_table = _quote_identifier(table_name)
        placeholders = ", ".join(["?"] * len(table["columns"]))
        connection.executemany(f"INSERT INTO {quoted_table} VALUES ({placeholders})", rows)


def _quote_identifier(identifier):
    return f'"{identifier.replace(chr(34), chr(34) + chr(34))}"'


def _serialize_value(value):
    if hasattr(value, "isoformat"):
        return value.isoformat()

    return value
