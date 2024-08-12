-- SQL script that creates a table users with the following requirements:
    --id: integer, never null, auto increment and primary key
    --email: string (255 characters), never null and unique
    --name: string (255 characters)
-- If the table already exists, the script will not fail

CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    PRIMARY KEY (id)
);
