CREATE TABLE salles (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    adresse VARCHAR(255) NOT NULL
);

INSERT INTO salles (nom, adresse) VALUES
    ('FitLife Paris 11', '12 Rue de la Roquette, Paris'),
    ('FitLife Lyon Centre', '45 Rue de la République, Lyon'),
    ('FitLife Marseille Vieux-Port', '8 Quai du Port, Marseille');