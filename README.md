
# Groceries CRUD (Python + Flask + MySQL + Docker)

Stack: Python (Flask), MySQL 8, Docker Compose. Sin clases, sin validaciones complicadas.

## Cómo correr
1) Requisitos: Docker y Docker Compose.
2) En una terminal, entra a esta carpeta.
3) Ejecuta:
   ```bash
   docker compose build && docker compose up
   ```
4) Abre: http://localhost:50000

## API
- GET /api/items
- GET /api/items/<id>
- POST /api/items  (JSON: name, department, price, stock)
- PUT /api/items/<id>  (JSON: name, department, price, stock)
- DELETE /api/items/<id>

## Estructura
- backend/app.py -> Flask API + sirve / (index.html)
- backend/static/index.html -> Frontend con JS listo
- mysql/init.sql -> Crea DB y tabla `products` + datos de ejemplo
- docker-compose.yml -> Orquesta `db` y `api`

