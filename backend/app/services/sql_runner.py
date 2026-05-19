import duckdb

from app.utils.sql_safety import validate_safe_sql


class SQLExecutionError(Exception):
    """Raised when a learner query cannot be executed safely."""


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

    is_safe, message = validate_safe_sql(query)
    if not is_safe:
        raise SQLExecutionError(message)

    try:
        with duckdb.connect(database=":memory:") as connection:
            _create_tables(connection, problem.get("schema", []))
            _insert_seed_data(connection, problem.get("schema", []), problem.get("seed_data", {}))
            cursor = connection.execute(query)
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description or []]
    except duckdb.Error as error:
        raise SQLExecutionError(str(error)) from error

    return {
        "columns": columns,
        "rows": [[_serialize_value(value) for value in row] for row in rows],
    }


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
