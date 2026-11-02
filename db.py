import os

import psycopg2


def get_conn():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "topic6_demo"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.environ["DB_PASSWORD"],
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
    )
