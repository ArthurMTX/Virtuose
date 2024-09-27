CREATE TABLE templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    hash VARCHAR(255)
);

CREATE TABLE domains (
    id SERIAL PRIMARY KEY,
    id_template INT,
    id_user INT,
    name VARCHAR(255),
    uuid VARCHAR(255),
    ram VARCHAR(3),
    cpu VARCHAR(2),
    FOREIGN KEY (id_template) REFERENCES templates(id)
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    FOREIGN KEY (id_user) REFERENCES auth_user(id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
);
