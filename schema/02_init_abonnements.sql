CREATE TABLE abonnements (
    id SERIAL PRIMARY KEY,
    type_abonnement VARCHAR(50) NOT NULL,
    prix_mensuel DECIMAL(5, 2) NOT NULL
);

INSERT INTO abonnements (type_abonnement, prix_mensuel)
VALUES
    ('Forme', 30.00),
    ('Premium', 50.00);
    