import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pymysql

# -------- DB helpers (no classes, just functions) --------
def get_conn():
    """
    TODO (student):
      - Create and return a MySQL connection using environment variables:
        MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
      - Use pymysql.connect(...) with DictCursor and autocommit=True
    """
    # Example (do NOT implement here in the starter):
    # return pymysql.connect(host=..., user=..., password=..., database=...,
    #                        cursorclass=pymysql.cursors.DictCursor, autocommit=True)
    return None  # placeholder


def get_or_create_dept_id(dept_name):
    """
    TODO (student):
      - Try to SELECT id FROM dept WHERE name=%s LIMIT 1
      - If exists, return that id
      - Else INSERT INTO dept(name) VALUES(%s) and return lastrowid
    """
    # Pseudocode only:
    # conn = get_conn()
    # with conn.cursor() as cur:
    #   cur.execute("SELECT id FROM dept WHERE name=%s LIMIT 1", (dept_name,))
    #   row = cur.fetchone()
    #   if row: return row["id"]
    #   cur.execute("INSERT INTO dept (name) VALUES (%s)", (dept_name,))
    #   return cur.lastrowid
    return None  # placeholder


def get_or_create_origin_id(origin_code):
    """
    TODO (student):
      - Default origin_code to 'MX' if missing
      - SELECT id FROM origin WHERE code=%s LIMIT 1
      - If exists, return it; otherwise INSERT and return lastrowid
    """
    return None  # placeholder


def fetch_all_products():
    """
    TODO (student):
      - Return a list of products joining dept and origin so the frontend sees:
        id, name, department (dept.name), origin (origin.code), price, stock
      - SQL idea:
        SELECT p.id, p.name, d.name AS department, o.code AS origin, p.price, p.stock
        FROM products p
        JOIN dept d ON p.dept_id = d.id
        JOIN origin o ON p.origin_id = o.id
        ORDER BY p.id;
    """
    return []  # placeholder


def fetch_product(product_id):
    """
    TODO (student):
      - Return a single product by id with the same join as above
      - If not found, return None
    """
    return None  # placeholder


def insert_product(name, department, origin, price, stock):
    """
    TODO (student):
      - Use get_or_create_dept_id and get_or_create_origin_id to get foreign keys
      - INSERT INTO products (name, dept_id, origin_id, price, stock) VALUES (...)
      - Return new product id (lastrowid)
    """
    return None  # placeholder


def update_product(product_id, name, department, origin, price, stock):
    """
    TODO (student):
      - Resolve dept_id/origin_id
      - UPDATE products SET ... WHERE id=%s
      - Return affected rows count
    """
    return 0  # placeholder


def delete_product(product_id):
    """
    TODO (student):
      - DELETE FROM products WHERE id=%s
      - Return affected rows count
    """
    return 0  # placeholder


# --- Helpers to list departments and origins ---
def fetch_departments():
    """
    TODO (student):
      - SELECT id, name FROM dept ORDER BY name;
      - Return list of dicts
    """
    return []  # placeholder


def fetch_origins():
    """
    TODO (student):
      - SELECT id, code FROM origin ORDER BY code;
      - Return list of dicts
    """
    return []  # placeholder


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
