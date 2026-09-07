import sqlite3

DATABASE = "cyberlab.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price INTEGER NOT NULL
        )
    """)

    count = connection.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    if count == 0:
        connection.executemany(
            """
            INSERT INTO products (name, category, price)
            VALUES (?, ?, ?)
            """,
            [
                ("Laptop", "Electronics", 10000000),
                ("Keyboard", "Electronics", 500000),
                ("Backpack", "Accessories", 300000),
                ("Monitor", "Electronics", 2500000),
            ],
        )

    connection.commit()
    connection.close()
