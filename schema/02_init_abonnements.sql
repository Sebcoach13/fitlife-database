CREATE TABLE abonnements (
    id SERIAL PRIMARY KEY,
    type_abonnement VARCHAR(50) NOT NULL,
    prix_mensuel DECIMAL(5,2) NOT NULL
);
