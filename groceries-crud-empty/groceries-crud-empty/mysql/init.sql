CREATE DATABASE IF NOT EXISTS groceries;
USE groceries;

DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS dept;
DROP TABLE IF EXISTS origin;

CREATE TABLE dept (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL
);

CREATE TABLE origin (
  id INT AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(3) NOT NULL
);

CREATE TABLE products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  dept_id INT NOT NULL,
  origin_id INT NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  stock INT NOT NULL,
  FOREIGN KEY (dept_id) REFERENCES dept(id),
  FOREIGN KEY (origin_id) REFERENCES origin(id)
);

INSERT INTO dept (name) VALUES
  ('Produce'),
  ('Dairy'),
  ('Bakery'),
  ('Beverages');

INSERT INTO origin (code) VALUES
  ('MX'),
  ('USA'),
  ('CAN'),
  ('BR');

INSERT INTO products (name, dept_id, origin_id, price, stock) VALUES
  ('Apples', 1, 1, 25.50, 30),
  ('Milk 1L', 2, 1, 18.90, 40),
  ('Whole Wheat Bread', 3, 1, 32.00, 15),
  ('Orange Juice', 4, 2, 45.00, 20);
