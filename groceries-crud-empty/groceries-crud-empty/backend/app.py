import os
import pymysql
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="static", static_url_path="")

# ----------------------------
# DATABASE CONNECTION
# ----------------------------
def get_conn():
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST", "db"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "1234"),
        database=os.getenv("MYSQL_DATABASE", "groceries"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

# ----------------------------
# HELPERS
# ----------------------------
def get_or_create_dept_id(name):
    conn = get_conn()
    with conn.cursor() as c:
        c.execute("SELECT id FROM dept WHERE name=%s", (name,))
        row = c.fetchone()
        if row:
            return row["id"]
        c.execute("INSERT INTO dept(name) VALUES (%s)", (name,))
        return c.lastrowid


def get_or_create_origin_id(code):
    conn = get_conn()
    with conn.cursor() as c:
        c.execute("SELECT id FROM origin WHERE code=%s", (code,))
        row = c.fetchone()
        if row:
            return row["id"]
        c.execute("INSERT INTO origin(code) VALUES (%s)", (code,))
        return c.lastrowid

# ----------------------------
# FETCH FUNCTIONS
# ----------------------------
def fetch_departments():
    conn = get_conn()
    with conn.cursor() as c:
        c.execute("SELECT id, name FROM dept ORDER BY name")
        return c.fetchall()

def fetch_origins():
    conn = get_conn()
    with conn.cursor() as c:
        c.execute("SELECT id, code FROM origin ORDER BY code")
        return c.fetchall()

def fetch_all_products():
    conn = get_conn()
    with conn.cursor() as c:
        query = """
        SELECT p.id, p.name,
               d.name AS department,
               o.code AS origin,
               p.price,
               p.stock
        FROM products p
        JOIN dept d ON p.dept_id = d.id
        JOIN origin o ON p.origin_id = o.id
        ORDER BY p.id
        """
        c.execute(query)
        return c.fetchall()

def fetch_product(product_id):
    conn = get_conn()
    with conn.cursor() as c:
        query = """
        SELECT p.id, p.name,
               d.name AS department,
               o.code AS origin,
               p.price,
               p.stock
        FROM products p
        JOIN dept d ON p.dept_id = d.id
        JOIN origin o ON p.origin_id = o.id
        WHERE p.id = %s
        """
        c.execute(query, (product_id,))
        return c.fetchone()

# ----------------------------
# INSERT / UPDATE / DELETE
# ----------------------------
def insert_product(product):
    dept_id = get_or_create_dept_id(product["department"])
    origin_id = get_or_create_origin_id(product["origin"])

    conn = get_conn()
    with conn.cursor() as c:
        c.execute("""
            INSERT INTO products(name, dept_id, origin_id, price, stock)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            product["name"],
            dept_id,
            origin_id,
            product["price"],
            product["stock"]
        ))

def update_product(product_id, product):
    dept_id = get_or_create_dept_id(product["department"])
    origin_id = get_or_create_origin_id(product["origin"])

    conn = get_conn()
    with conn.cursor() as c:
        c.execute("""
            UPDATE products
            SET name=%s, dept_id=%s, origin_id=%s, price=%s, stock=%s
            WHERE id=%s
        """, (
            product["name"],
            dept_id,
            origin_id,
            product["price"],
            product["stock"],
            product_id
        ))

def delete_product(product_id):
    conn = get_conn()
    with conn.cursor() as c:
        c.execute("DELETE FROM products WHERE id=%s", (product_id,))

# ----------------------------
# ROUTES
# ----------------------------

@app.route("/")
def root():
    return send_from_directory("static", "index.html")

@app.route("/api/departments")
def api_departments():
    return jsonify(fetch_departments())

@app.route("/api/origins")
def api_origins():
    return jsonify(fetch_origins())

@app.route("/api/items")
def api_items():
    return jsonify(fetch_all_products())

@app.route("/api/items", methods=["POST"])
def api_create_item():
    insert_product(request.json)
    return jsonify({"status": "created"})

@app.route("/api/items/<int:item_id>", methods=["GET"])
def api_get_item(item_id):
    item = fetch_product(item_id)
    if not item:
        return jsonify({"error": "Not found"}), 404
    return jsonify(item)

@app.route("/api/items/<int:item_id>", methods=["PUT"])
def api_update_item(item_id):
    update_product(item_id, request.json)
    return jsonify({"status": "updated"})

@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def api_delete_item(item_id):
    delete_product(item_id)
    return jsonify({"status": "deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
