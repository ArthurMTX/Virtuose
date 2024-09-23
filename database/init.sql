CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    username VARCHAR(255),
    password VARCHAR(255),
    is_superuser BOOLEAN,
    is_staff BOOLEAN,
    date_joined TIMESTAMP,
    last_login DATE
);

CREATE TABLE templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    hash VARCHAR(255)
);

CREATE TABLE clones (
    id SERIAL PRIMARY KEY,
    id_template INT,
    id_user INT,
    name VARCHAR(255),
    FOREIGN KEY (id_template) REFERENCES templates(id)
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    FOREIGN KEY (id_user) REFERENCES "user"(id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
);
