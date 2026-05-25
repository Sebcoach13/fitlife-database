import pandas as pd

print("🚀 Lancement du traitement des données CRM FitLife...")

try:
    # 1. Chargement direct des données réelles du projet dans Pandas
    # Données issues de 01_init_salles.sql (id, nom, adresse)
    salles_data = [
        [1, 'FitLife Paris 11', '12 Rue de la Roquette, Paris'],
        [2, 'FitLife Lyon Centre', '45 Rue de la République, Lyon'],
        [3, 'FitLife Marseille Vieux-Port', '8 Quai du Port, Marseille']
    ]
    df_salles = pd.DataFrame(salles_data, columns=["salle_id", "nom_salle", "adresse"]).set_index("salle_id")

    # Données issues de 02_init_abonnements.sql (id, type_abonnement, prix_mensuel)
    abos_data = [
        [1, 'Forme', 30.00],
        [2, 'Premium', 50.00]
    ]
    df_abos = pd.DataFrame(abos_data, columns=["abonnement_id", "type_abonnement", "prix_mensuel"]).set_index("abonnement_id")

    # Données issues de 03_init_membres.sql (nom, prenom, email, date_inscription, salle_id, abonnement_id)
    membres_data = [
        ['Dupont', 'Jean', 'jean.dupont@email.com', '2026-01-15', 1, 1],
        ['Martin', 'Alice', 'alice.martin@email.com', '2026-02-20', 2, 2],
        ['Rousseau', 'Marc', 'marc.rousseau@email.com', '2026-03-05', 1, 2]
    ]
    df_membres = pd.DataFrame(membres_data, columns=["nom", "prenom", "email", "date_inscription", "salle_id", "abonnement_id"])

except Exception as e:
    print(f"❌ Erreur lors de la création des structures de données : {e}")
    exit()

# 2. Moteur d'analyse (Jointures internes identiques aux INNER JOIN SQL)
try:
    # Jointure avec la grille tarifaire
    df_complet = df_membres.merge(df_abos, left_on="abonnement_id", right_index=True)
    # Jointure avec les clubs
    df_complet = df_complet.merge(df_salles, left_on="salle_id", right_index=True)

    # Calculs statistiques demandés par le cas CRM de la Sorbonne
    total_membres = len(df_membres)
    chiffre_affaires_mensuel = df_complet["prix_mensuel"].sum()
    repartition_salles = df_complet["nom_salle"].value_counts()
    abo_populaire = df_complet["type_abonnement"].value_counts().idxmax()

    # 3. Génération automatique du livrable de reporting
    rapport_content = f"""# 📈 RAPPORT D'ACTIVITÉ CRM AUTOMATISÉ - FITLIFE
généré automatiquement par le script Python (Moteur Pandas)

## 🎯 Indicateurs Clés de Performance (KPIs)
* **Nombre total d'adhérents actifs :** {total_membres} membres
* **Chiffre d'Affaires Mensuel Récurrent (MRR) :** {chiffre_affaires_mensuel:.2f} €
* **Formule d'abonnement la plus plébiscitée :** Formule {abo_populaire}

## 🏢 Performance des Établissements (Nombre de membres par club)
"""
    for salle, count in repartition_salles.items():
        rapport_content += f"* **{salle} :** {count} inscrit(s)\n"

    # Écriture du fichier Markdown final
    with open("Rapport_CRM_FitLife.md", "w", encoding="utf-8") as f:
        f.write(rapport_content)

    print("✅ Le traitement des données est un succès total !")
    print("➡️ Le fichier 'Rapport_CRM_FitLife.md' a été généré à la racine de ton projet !")

except Exception as e:
    print(f"❌ Erreur lors des calculs statistiques Pandas : {e}")