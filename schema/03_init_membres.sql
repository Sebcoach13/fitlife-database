CREATE TABLE membres (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    date_inscription DATE NOT NULL,
    salle_id INT REFERENCES salles(id),
    abonnement_id INT REFERENCES abonnements(id)
);