import psycopg2
from psycopg2.extras import DictCursor


conn = psycopg2.connect(
    host="127.0.0.1",
    port=5432,
    user="postgres",
    password="Moto#1234",
    dbname="postgres",
)

print("conectando com o banco")
cur = conn.cursor(cursor_factory = DictCursor)

print("banco conectado")

print("realizasndo consulta")

cur.execute("SELECT po.* FROM brazil.purchase_order AS po")


table_result = cur.fetchall()

print("resultado: ")
print(table_result)