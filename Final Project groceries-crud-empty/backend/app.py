import os
import pymysql
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="static", static_url_path="")

def get_conn():
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST", "db"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "1234"),
        database=os.getenv("MYSQL_DATABASE", "groceries"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


def get_or_create_dept_id(name):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM dept WHERE name=%s", (name,))
        row = cur.fetchone()
        if row:
            return row["id"]
        cur.execute("INSERT INTO dept(name) VALUES (%s)", (name,))
        return cur.lastrowid


def get_or_create_origin_id(code):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM origin WHERE code=%s", (code,))
        row = cur.fetchone()
        if row:
            return row["id"]
        cur.execute("INSERT INTO origin(code) VALUES (%s)", (code,))
        return cur.lastrowid


def fetch_all_products():
    conn = get_conn()
    with conn.cursor() as cur:
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
        cur.execute(query)
        return cur.fetchall()

def fetch_product(product_id):
    conn = get_conn()
    with conn.cursor() as cur:
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
        cur.execute(query, (product_id,))
        return cur.fetchone()

def insert_product(product):
    dept_id = get_or_create_dept_id(product["department"])
    origin_id = get_or_create_origin_id(product["origin"])

    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("""
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
    with conn.cursor() as cur:
        cur.execute("""
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
    with conn.cursor() as cur:
        cur.execute("DELETE FROM products WHERE id=%s", (product_id,))


# --- Helpers to list departments and origins ---
def fetch_departments():
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("SELECT id, name FROM dept ORDER BY name")
        return cur.fetchall()

def fetch_origins():
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("SELECT id, code FROM origin ORDER BY code")
        return cur.fetchall()


# -------- Flask app --------
app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)  # allow front-end JS to call API

# Serve the static index
@app.route("/")
def root():
    return send_from_directory("static", "index.html")


# -------- REST API (only instructional messages here) --------
@app.get("/api/items")
def api_list_items():
    return jsonify({
        "message": "GET /api/items should return a list of products joined with dept.name and origin.code."
    })

@app.get("/api/items/<int:product_id>")
def api_get_item(product_id):
    return jsonify({
        "message": "GET /api/items/<id> should return a single product (with department and origin) or 404 if not found.",
        "id_received": product_id
    })

@app.post("/api/items")
def api_create_item():
    data = request.get_json(force=True)
    return jsonify({
        "message": "POST /api/items should insert a product (resolving dept_id and origin_id) and return the new id.",
        "payload_received": data
    }), 201

@app.put("/api/items/<int:product_id>")
def api_update_item(product_id):
    data = request.get_json(force=True)
    return jsonify({
        "message": "PUT /api/items/<id> should update the product (name, department->dept_id, origin->origin_id, price, stock).",
        "id_received": product_id,
        "payload_received": data
    })

@app.delete("/api/items/<int:product_id>")
def api_delete_item(product_id):
    return jsonify({
        "message": "DELETE /api/items/<id> should delete the product and return a confirmation.",
        "id_received": product_id
    })

@app.get("/api/departments")
def api_departments():
    return jsonify({
        "message": "GET /api/departments should return a list like: [{id, name}, ...] ordered by name."
    })

@app.get("/api/origins")
def api_origins():
    return jsonify({
        "message": "GET /api/origins should return a list like: [{id, code}, ...] ordered by code."
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
