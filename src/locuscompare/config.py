"""Database connection configuration.

Mirrors the R package's approach of shipping the (read-only) connection
parameters with the package so it works out of the box. Any field can be
overridden with a ``LOCUSCOMPARE_DB_*`` environment variable.
"""
import os

_DEFAULT = {
    "host": "54.254.162.217",
    "user": "locuscompare",
    "password": "voddit-7rubfo-faqxoB",
    "port": 31987,
    "database": "colotool",
}


def get_db_config():
    """Return the DB connection parameters, allowing ``LOCUSCOMPARE_DB_*`` overrides."""
    return {
        "host": os.environ.get("LOCUSCOMPARE_DB_HOST", _DEFAULT["host"]),
        "user": os.environ.get("LOCUSCOMPARE_DB_USER", _DEFAULT["user"]),
        "password": os.environ.get("LOCUSCOMPARE_DB_PASSWORD", _DEFAULT["password"]),
        "port": int(os.environ.get("LOCUSCOMPARE_DB_PORT", _DEFAULT["port"])),
        "database": os.environ.get("LOCUSCOMPARE_DB_NAME", _DEFAULT["database"]),
    }
