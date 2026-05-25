SELECT
    m.prenom,
    m.nom,
    s.nom AS nom_de_salle,
    a.type_abonnement AS formule
FROM membres AS m
INNER JOIN salles AS s
    ON m.salle_id = s.id
INNER JOIN abonnements AS a
    ON m.abonnement_id = a.id;