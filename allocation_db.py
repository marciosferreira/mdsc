import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

ALLOCATION_DB_PATH = Path(os.getenv("ALLOCATION_DB_PATH", str(Path(__file__).parent / "allocation.db")))


@contextmanager
def get_allocation_db():
    conn = sqlite3.connect(ALLOCATION_DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def ensure_allocation_tables_exist() -> None:
    """Checagem defensiva de startup — não semeia dados, só avisa se o loader nunca rodou."""
    try:
        with get_allocation_db() as conn:
            tables = {
                row["name"]
                for row in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name IN ('ka_input_data', 'ka_deal_allocation')"
                )
            }
    except Exception:
        tables = set()
    missing = {"ka_input_data", "ka_deal_allocation"} - tables
    if missing:
        import logging
        logging.getLogger(__name__).warning(
            "Tabelas de KA Allocation ausentes (%s). Rode load_ka_allocation.py para carregá-las.",
            ", ".join(sorted(missing)),
        )
