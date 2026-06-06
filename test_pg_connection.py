import psycopg2

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": ""
}

try:
    conn = psycopg2.connect(**DB_CONFIG)

    cur = conn.cursor()

    cur.execute("SELECT version();")
    version = cur.fetchone()

    print("✅ Connected Successfully")
    print("PostgreSQL Version:")
    print(version[0])

    cur.close()
    conn.close()

except Exception as e:
    print("❌ Connection Failed")
    print(e)