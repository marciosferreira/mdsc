import psycopg2
from psycopg2.extras import DictCursor

conn = psycopg2.connect(
    host="127.0.0.1",
    port=5432,
    user="postgres",
    password="Moto#1234",
    dbname="postgres",
)
cur = conn.cursor(cursor_factory=DictCursor)

output = []

# Schemas
cur.execute("""
    SELECT schema_name
    FROM information_schema.schemata
    WHERE schema_name = 'brazil'
    ORDER BY schema_name
""")
schemas = [r["schema_name"] for r in cur.fetchall()]

for schema in schemas:
    output.append(f"\n{'='*60}")
    output.append(f"SCHEMA: {schema}")
    output.append(f"{'='*60}")

    # Tables
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %s AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """, (schema,))
    tables = [r["table_name"] for r in cur.fetchall()]

    for table in tables:
        output.append(f"\n  TABLE: {schema}.{table}")
        output.append(f"  {'-'*50}")

        # Columns
        cur.execute("""
            SELECT column_name, data_type, character_maximum_length,
                   numeric_precision, numeric_scale, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
            ORDER BY ordinal_position
        """, (schema, table))
        for col in cur.fetchall():
            dtype = col["data_type"]
            if col["character_maximum_length"]:
                dtype += f"({col['character_maximum_length']})"
            elif col["numeric_precision"] and col["numeric_scale"] is not None:
                dtype += f"({col['numeric_precision']},{col['numeric_scale']})"
            nullable = "NULL" if col["is_nullable"] == "YES" else "NOT NULL"
            default = f" DEFAULT {col['column_default']}" if col["column_default"] else ""
            output.append(f"    {col['column_name']:<35} {dtype:<25} {nullable}{default}")

        # Primary key
        cur.execute("""
            SELECT kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            WHERE tc.constraint_type = 'PRIMARY KEY'
                AND tc.table_schema = %s AND tc.table_name = %s
            ORDER BY kcu.ordinal_position
        """, (schema, table))
        pk_cols = [r["column_name"] for r in cur.fetchall()]
        if pk_cols:
            output.append(f"\n    PK: ({', '.join(pk_cols)})")

        # Foreign keys
        cur.execute("""
            SELECT kcu.column_name, ccu.table_schema AS ref_schema,
                   ccu.table_name AS ref_table, ccu.column_name AS ref_column
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
                AND tc.table_schema = %s AND tc.table_name = %s
        """, (schema, table))
        for fk in cur.fetchall():
            output.append(f"    FK: {fk['column_name']} → {fk['ref_schema']}.{fk['ref_table']}.{fk['ref_column']}")

        # Indexes
        cur.execute("""
            SELECT indexname, indexdef
            FROM pg_indexes
            WHERE schemaname = %s AND tablename = %s
            AND indexname NOT LIKE '%%_pkey'
            ORDER BY indexname
        """, (schema, table))
        for idx in cur.fetchall():
            output.append(f"    IDX: {idx['indexname']}: {idx['indexdef']}")

cur.close()
conn.close()

schema_text = "\n".join(output)
with open("schema.txt", "w", encoding="utf-8") as f:
    f.write(schema_text)

print("Schema salvo em schema.txt")
print(f"Schemas encontrados: {', '.join(schemas)}")
