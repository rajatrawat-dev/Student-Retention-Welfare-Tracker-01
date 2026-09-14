"""Safety validator enforcing strict read-only analytical SQL execution."""

import re
from typing import Tuple, List

FORBIDDEN_KEYWORDS = [
    r"DROP",
    r"DELETE",
    r"UPDATE",
    r"INSERT",
    r"ALTER",
    r"CREATE",
    r"TRUNCATE",
    r"GRANT",
    r"REVOKE",
    r"ATTACH",
    r"DETACH",
    r"COPY",
    r"PRAGMA",
    r"EXEC",
    r"EXECUTE",
    r"SHUTDOWN",
    r"REPLACE",
]

ALLOWED_ENTITIES = ["students", "department_summary", "risk_summary"]

def validate_query(sql: str) -> Tuple[bool, str]:
    """Validates SQL query for AI Safety compliance.
    Returns (is_valid, error_reason).
    """
    if not sql or not sql.strip():
        return False, "Query is empty."

    cleaned_sql = sql.strip().strip(";").strip()

    # Rule 1: Disallow multiple statements separated by semicolon
    if ";" in cleaned_sql:
        return False, "Multi-statement queries are strictly prohibited."

    # Rule 2: Must begin with SELECT or WITH
    first_word = cleaned_sql.split()[0].upper()
    if first_word not in ["SELECT", "WITH"]:
        return False, f"Forbidden query type '{first_word}'. Only SELECT queries are permitted."

    # Rule 3: Check for forbidden destructive / operational keywords
    for pattern in FORBIDDEN_KEYWORDS:
        if re.search(pattern, cleaned_sql, re.IGNORECASE):
            match = re.search(pattern, cleaned_sql, re.IGNORECASE).group(0)
            return False, f"Security Violation: Forbidden keyword '{match}' detected."

    # Rule 4: Verify query references allowed tables/views
    lower_sql = cleaned_sql.lower()
    has_allowed = any(entity in lower_sql for entity in ALLOWED_ENTITIES)
    if not has_allowed:
        return False, f"Query must reference approved entities: {', '.join(ALLOWED_ENTITIES)}"

    return True, "Query validated successfully."
