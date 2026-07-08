"""Carrega os dois arquivos xlsx de KA Allocation para o SQLite allocation.db.

Uso: python load_ka_allocation.py

Idempotente — recria as tabelas do zero a cada execução (DROP + CREATE + INSERT),
então pode ser rodado quantas vezes for necessário após uma nova exportação dos xlsx.
"""
import sqlite3
from contextlib import contextmanager
from pathlib import Path

import pandas as pd

ALLOCATION_DB = Path(__file__).parent / "allocation.db"


@contextmanager
def get_allocation_db():
    conn = sqlite3.connect(ALLOCATION_DB)
    try:
        yield conn
    finally:
        conn.close()


INPUT_XLSX = "ka-allocation-automation_output_data.xlsx"
OUTPUT_XLSX = "ka-allocation-automation_output_deal_allocation (9).xlsx"

GROUP_KEYS = ["quarter", "material_id", "key_account_id"]
EXPECTED_MONTH_STATUS_PATTERNS = (("done", "done", "ongoing"), ("next", "next", "next"))
INDEXED_COLS = ["key_account_code", "deal_group", "origin", "month_status"]

_SQL_TYPE = {
    "int64": "INTEGER",
    "float64": "REAL",
    "bool": "INTEGER",
    "object": "TEXT",
}


def _sql_type_for(dtype) -> str:
    if str(dtype).startswith("datetime64"):
        return "TEXT"
    return _SQL_TYPE.get(str(dtype), "TEXT")


def _prepare(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["month_seq"] = df.groupby(GROUP_KEYS).cumcount() + 1

    bad_groups = 0
    for _, sub in df.groupby(GROUP_KEYS):
        if tuple(sub["month_status"]) not in EXPECTED_MONTH_STATUS_PATTERNS:
            bad_groups += 1
    if bad_groups:
        print(f"  [AVISO] {bad_groups} grupo(s) de {GROUP_KEYS} fora do padrão esperado de month_status.")

    for col in df.columns:
        if str(df[col].dtype).startswith("datetime64"):
            df[col] = df[col].astype(str)
        elif df[col].dtype == bool:
            df[col] = df[col].astype(int)
    return df


def _year_month_is_corrupted(series: pd.Series) -> bool:
    """Detecta o bug de exportação conhecido: year_month colapsando para ~1969-12-31.
    Heurística: qualquer ano < 2000 é sinal do bug (dado de negócio é sempre recente)."""
    years = pd.to_datetime(series, errors="coerce").dt.year
    return bool((years < 2000).any())


def _fix_output_year_month(df_input: pd.DataFrame, df_output: pd.DataFrame) -> pd.DataFrame:
    """Corrige ka_deal_allocation.year_month usando o valor confiável de ka_input_data via
    join em (quarter, material_id, key_account_id, month_seq) — só quando necessário
    (o arquivo de origem já veio com um bug de exportação em versões anteriores, mas isso
    pode ser corrigido na fonte; aplicar o join incondicionalmente arriscaria sobrescrever
    um valor já correto com um valor levemente diferente do outro arquivo)."""
    if not _year_month_is_corrupted(df_output["year_month"]):
        print("  year_month de ka_deal_allocation já está correto na origem — nenhuma correção aplicada.")
        return df_output

    print("  [AVISO] year_month de ka_deal_allocation veio corrompido na origem — corrigindo via join com ka_input_data.")
    key_cols = GROUP_KEYS + ["month_seq"]
    lookup = df_input.drop_duplicates(key_cols).set_index(key_cols)["year_month"]
    corrected = df_output.set_index(key_cols).index.map(lookup)

    missing = pd.isna(corrected).sum()
    if missing:
        print(f"  [AVISO] {missing} linha(s) de ka_deal_allocation sem correspondência em "
              f"ka_input_data — year_month mantido bruto (corrompido) nessas linhas.")

    df_output = df_output.copy()
    df_output["year_month"] = [
        raw if pd.isna(fixed) else fixed
        for fixed, raw in zip(corrected, df_output["year_month"])
    ]
    return df_output


def _load_table(conn, table: str, df: pd.DataFrame) -> None:
    conn.execute(f"DROP TABLE IF EXISTS {table}")
    cols_sql = ",\n    ".join(f'"{c}" {_sql_type_for(df[c].dtype)}' for c in df.columns)
    conn.execute(f"CREATE TABLE {table} (\n    {cols_sql}\n)")

    cols_list = ",".join(f'"{c}"' for c in df.columns)
    placeholders = ",".join(["?"] * len(df.columns))
    rows = [tuple(r) for r in df.itertuples(index=False, name=None)]
    conn.executemany(f"INSERT INTO {table} ({cols_list}) VALUES ({placeholders})", rows)

    conn.execute(f'CREATE INDEX idx_{table}_composite ON {table} ("material_id", "key_account_id", "quarter")')
    for col in INDEXED_COLS:
        if col in df.columns:
            conn.execute(f'CREATE INDEX idx_{table}_{col} ON {table} ("{col}")')
    conn.commit()


def main() -> None:
    print(f"Lendo {INPUT_XLSX} ...")
    df_input = _prepare(pd.read_excel(INPUT_XLSX))
    print(f"Lendo {OUTPUT_XLSX} ...")
    df_output = _prepare(pd.read_excel(OUTPUT_XLSX))

    print("Verificando year_month de ka_deal_allocation ...")
    df_output = _fix_output_year_month(df_input, df_output)

    with get_allocation_db() as conn:
        _load_table(conn, "ka_input_data", df_input)
        _load_table(conn, "ka_deal_allocation", df_output)

    print("\nResumo:")
    for name, df in (("ka_input_data", df_input), ("ka_deal_allocation", df_output)):
        seq_counts = df["month_seq"].value_counts().sort_index().to_dict()
        quarters = sorted(df["quarter"].unique().tolist())
        print(f"  {name}: {len(df)} linhas | month_seq={seq_counts} | quarters={quarters}")


if __name__ == "__main__":
    main()
