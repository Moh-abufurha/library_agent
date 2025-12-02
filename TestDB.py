import sqlite3

DB_NAME = "library.db"

def show_books():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    print("\n📚 Books Inventory:")
    cur.execute("SELECT isbn, title, author, price, stock FROM books ORDER BY title;")
    books = cur.fetchall()
    for b in books:
        print(f"  {b[1]} by {b[2]} | ISBN: {b[0]} | Price: {b[3]} | Stock: {b[4]}")
    conn.close()

def show_customers():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    print("\n👥 Customers:")
    cur.execute("SELECT id, name, email FROM customers ORDER BY id;")
    for c in cur.fetchall():
        print(f"  ID: {c[0]} | {c[1]} | {c[2]}")
    conn.close()

def show_orders():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    print("\n🧾 Orders:")
    cur.execute("SELECT id, customer_id, created_at FROM orders ORDER BY id DESC LIMIT 5;")
    orders = cur.fetchall()
    for o in orders:
        print(f"  Order #{o[0]} | Customer ID: {o[1]} | Date: {o[2]}")
    conn.close()

def show_order_items():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    print("\n📦 Order Items:")
    cur.execute("""
        SELECT i.order_id, b.title, i.qty
        FROM order_items i
        JOIN books b ON b.isbn = i.isbn
        ORDER BY i.order_id DESC LIMIT 10;
    """)
    items = cur.fetchall()
    for it in items:
        print(f"  Order {it[0]} → {it[1]} (x{it[2]})")
    conn.close()

# 🆕 NEW TABLES
def show_messages():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    print("\n💬 Messages:")
    cur.execute("SELECT id, session_id, role, content, created_at FROM messages ORDER BY id DESC LIMIT 10;")
    msgs = cur.fetchall()
    for m in msgs:
        print(f"  #{m[0]} | {m[2]} | Session: {m[1]} | {m[3][:60]}... | {m[4]}")
    conn.close()

def show_tool_calls():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    print("\n🛠️ Tool Calls:")
    cur.execute("SELECT id, session_id, name, args_json, result_json, created_at FROM tool_calls ORDER BY id DESC LIMIT 10;")
    calls = cur.fetchall()
    for c in calls:
        print(f"  #{c[0]} | {c[2]} | Args: {c[3][:50]}... | Created: {c[5]}")
    conn.close()

if __name__ == "__main__":
    print("=== DATABASE INSPECTOR ===")
    show_books()
    show_customers()
    show_orders()
    show_order_items()
    show_messages()
    show_tool_calls()
    print("\n✅ Done checking database!\n")
