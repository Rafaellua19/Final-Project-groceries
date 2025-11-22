-- TODO (student):
-- This file should create a simple relational schema for a grocery inventory.
-- Suggested steps (write the real SQL yourself):

-- 1) Create database and (optionally) a user:
--    CREATE DATABASE groceries;
--    CREATE USER 'user'@'%' IDENTIFIED BY 'pass';
--    GRANT ALL PRIVILEGES ON groceries.* TO 'user'@'%';
--    USE groceries;

-- 2) Create reference tables:
--    Table dept:
--      id INT AUTO_INCREMENT PRIMARY KEY
--      name VARCHAR(50) NOT NULL

--    Table origin:
--      id INT AUTO_INCREMENT PRIMARY KEY
--      code VARCHAR(3) NOT NULL

-- 3) Create products table that references dept and origin:
--      id INT AUTO_INCREMENT PRIMARY KEY
--      name VARCHAR(100) NOT NULL
--      dept_id INT NOT NULL
--      origin_id INT NOT NULL
--      price DECIMAL(10,2) NOT NULL
--      stock INT NOT NULL
--      FOREIGN KEY (dept_id) REFERENCES dept(id)
--      FOREIGN KEY (origin_id) REFERENCES origin(id)

-- 4) (Optional) Insert some seed rows:
--    INSERT INTO dept (name) VALUES ('Dairy'), ('Produce'), ... ;
--    INSERT INTO origin (code) VALUES ('MX'), ('USA'), ... ;
--    INSERT INTO products (name, dept_id, origin_id, price, stock) VALUES (...);

-- Insert products, referencing dept and origin IDs.
-- Note: We use subqueries to find the IDs, which is more robust than assuming ID values.
-- Keep it simple. Avoid complex constraints or validations.
