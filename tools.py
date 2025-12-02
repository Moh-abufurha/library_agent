import sqlite3
import json
from datetime import datetime

DB_NAME = "library.db"
def get_connection():
    return sqlite3.connect(DB_NAME)
#
# def find_books(q):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT isbn, title, author, price, stock
#         FROM books
#         WHERE LOWER(title) LIKE '%' || LOWER(?) || '%'
#     """, (q,))
#
#     results = cur.fetchall()
#     conn.close()
#     books = [
#         {"isbn": r[0], "title": r[1], "author": r[2], "price": r[3], "stock": r[4]}
#         for r in results
#     ]
#     return books

def find_books(q):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT isbn, title, author, price, stock 
        FROM books 
        WHERE LOWER(title) LIKE '%' || LOWER(?) || '%'
           OR LOWER(author) LIKE '%' || LOWER(?) || '%'
    """, (q, q))
    results = cur.fetchall()
    conn.close()

    books = [
        {"isbn": r[0], "title": r[1], "author": r[2], "price": r[3], "stock": r[4]}
        for r in results
    ]
    return books


def create_order(customer_id,items):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (customer_id, created_at) VALUES (?, ?)",
                (customer_id, datetime.now().isoformat()))
    order_id = cur.lastrowid
    for item in items:
        isbn = item["isbn"]
        qty=item["qty"]
        cur.execute("INSERT INTO order_items (order_id, isbn, qty) VALUES (?, ?, ?)",
                    (order_id, isbn, qty))
        cur.execute("UPDATE books SET stock = stock - ? WHERE isbn = ?", (qty, isbn))
    conn.commit()
    conn.close()
    return {"order_id": order_id, "message": f"Order {order_id} created successfully!"}


def restock_book(title, qty):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE books
        SET stock = stock + ?
        WHERE LOWER(title) LIKE '%' || LOWER(?) || '%'
    """, (qty, title))
    conn.commit()

    cur.execute("""
        SELECT title, stock
        FROM books
        WHERE LOWER(title) LIKE '%' || LOWER(?) || '%'
    """, (title,))
    book = cur.fetchone()
    conn.close()

    if not book:
        return {"error": f"No book found with title '{title}'"}

    return {"title": book[0], "new_stock": book[1]}


def update_price(isbn, price):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE books SET price = ? WHERE isbn = ?", (price, isbn))
    conn.commit()
    conn.close()
    return {"isbn": isbn, "new_price": price}


def order_status(order_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT o.id, o.created_at, c.name, c.email
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        WHERE o.id = ?
    """, (order_id,))
    order = cur.fetchone()

    if not order:
        conn.close()
        return {"error": " Order not found"}


    cur.execute("""
        SELECT b.title, b.author, i.qty
        FROM order_items i
        JOIN books b ON i.isbn = b.isbn
        WHERE i.order_id = ?
    """, (order_id,))
    items = cur.fetchall()
    conn.close()

    item_list = [{"title": t, "author": a, "qty": q} for (t, a, q) in items]
    return {
        "order_id": order[0],
        "created_at": order[1],
        "customer": {"name": order[2], "email": order[3]},
        "items": item_list
    }


def inventory_summary(threshold=10):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT title, author, stock FROM books WHERE stock < ?", (threshold,))
    results = cur.fetchall()
    conn.close()

    return [{"title": t, "author": a, "stock": s} for (t, a, s) in results]



def log_message(session_id, role, content):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO messages (session_id, role, content, created_at)
        VALUES (?, ?, ?, ?)
    """, (session_id, role, content, datetime.now().isoformat()))

    conn.commit()
    conn.close()
if __name__ == "__main__":
    print(find_books("Clean"))
    print(restock_book("9780201616224", 3))
    print(update_price("9780201616224", 31.5))
    print(create_order(2, [{"isbn": "9780132350884", "qty": 3}]))
    print(order_status(1))
    print(inventory_summary())

    # def restock_book(isbn, qty):
    #     conn = get_connection()
    #     cur = conn.cursor()
    #
    #     # update stock
    #     cur.execute("UPDATE books SET stock = stock + ? WHERE isbn = ?", (qty, isbn))
    #     conn.commit()
    #
    #     cur.execute("SELECT title, stock FROM books WHERE isbn = ?", (isbn,))
    #     book = cur.fetchone()
    #     conn.close()
    #
    #     if not book:
    #         return {"error": f"Book with ISBN {isbn} not found."}
    #
    #     return {"title": book[0], "new_stock": book[1]}

    # def restock_book(isbn=None, title=None, qty=0):
    #     conn = get_connection()
    #     cur = conn.cursor()
    #
    #     if isbn:
    #         cur.execute("UPDATE books SET stock = stock + ? WHERE isbn = ?", (qty, isbn))
    #         cur.execute("SELECT title, stock FROM books WHERE isbn = ?", (isbn,))
    #     elif title:
    #         cur.execute("UPDATE books SET stock = stock + ? WHERE LOWER(title) LIKE '%' || LOWER(?) || '%'", (qty, title))
    #         cur.execute("SELECT title, stock FROM books WHERE LOWER(title) LIKE '%' || LOWER(?) || '%'", (title,))
    #     else:
    #         conn.close()
    #         return {"error": "You must provide either ISBN or title."}
    #
    #     conn.commit()
    #     book = cur.fetchone()
    #     conn.close()
    #
    #     if not book:
    #         return {"error": "Book not found."}
    #
    #     return {"title": book[0], "new_stock": book[1]}
    #
