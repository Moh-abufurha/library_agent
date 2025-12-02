import sqlite3
from datetime import datetime

DB_NAME = "library.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cur = conn.cursor()


    cur.executescript("""
    CREATE TABLE IF NOT EXISTS books (
        isbn TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE
    );

    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    );

    CREATE TABLE IF NOT EXISTS order_items (
        order_id INTEGER,
        isbn TEXT,
        qty INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (isbn) REFERENCES books(isbn)
    );
    
    CREATE TABLE IF NOT EXISTS conversation_summaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        summary TEXT NOT NULL,
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        role TEXT CHECK(role IN ('user','assistant','tool')),
        content TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS tool_calls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        name TEXT,
        args_json TEXT,
        result_json TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully!")


def seed_data():
    conn = get_connection()
    cur = conn.cursor()

    books = [
        ('9780132350884', 'clean code', 'robert c. martin', 30.5, 10),
        ('9780201616224', 'the pragmatic programmer', 'andrew hunt', 28.0, 5),
        ('9780131103627', 'the c programming language', 'brian kernighan', 25.0, 8),
        ('9780262033848', 'introduction to algorithms', 'thomas cormen', 60.0, 3),
        ('9780134685991', 'effective java', 'joshua bloch', 35.0, 4),
        ('9781491950296', 'designing data-intensive applications', 'martin kleppmann', 45.0, 6),
        ('9780596009205', 'head first design patterns', 'eric freeman', 32.0, 9),
        ('9781617294945', 'spring in action', 'craig walls', 40.0, 7),
        ('9780134494166', 'clean architecture', 'robert c. martin', 33.0, 10),
        ('9780596517748', 'javascript: the good parts', 'douglas crockford', 22.0, 5),
    ]

    customers = [
        ('John Doe', 'john@example.com'),
        ('Jane Smith', 'jane@example.com'),
        ('Ali Ahmad', 'ali@example.com'),
        ('Sara Khalid', 'sara@example.com'),
    ]


    cur.executemany(
        "INSERT OR IGNORE INTO books (isbn, title, author, price, stock) VALUES (?, ?, ?, ?, ?)",
        books
    )
    cur.executemany(
        "INSERT OR IGNORE INTO customers (name, email) VALUES (?, ?)",
        customers
    )


    orders = [
        (1, datetime.now().isoformat()),
        (2, datetime.now().isoformat()),
        (3, datetime.now().isoformat())
    ]
    cur.executemany("INSERT INTO orders (customer_id, created_at) VALUES (?, ?)", orders)

    order_items = [
        (1, '9780132350884', 2),(1, '9780201616224', 1),
        (2, '9780134494166', 1),
        (3, '9780262033848', 1),(3, '9780134685991', 1)
    ]
    cur.executemany("INSERT INTO order_items (order_id, isbn, qty) VALUES (?, ?, ?)", order_items)

    for item in order_items:
        cur.execute("UPDATE books SET stock = stock - ? WHERE isbn = ?", (item[2], item[1]))

    conn.commit()
    conn.close()
    print("Data seeded successfully!")


if __name__ == "__main__":
    init_db()
    seed_data()
