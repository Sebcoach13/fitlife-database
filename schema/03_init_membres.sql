CREATE TABLE membres (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    date_inscription DATE NOT NULL,
    salle_id INT REFERENCES salles (id),
    abonnement_id INT REFERENCES abonnements (id)
);

INSERT INTO membres (nom, prenom, email, date_inscription, salle_id, abonnement_id) VALUES
('Dupont', 'Jean', 'jean.dupont@email.com', '2026-01-15', 1, 1),
('Martin', 'Alice', 'alice.martin@email.com', '2026-02-20', 2, 2),
('Rousseau', 'Marc', 'marc.rousseau@email.com', '2026-03-05', 1, 2);
