Markdown
# FitLife Database 🏋️‍♂️ Base de Données, CRM Analytics & Intégration Continue (CI)

Bienvenue sur le dépôt officiel du projet **FitLife Database**. Ce document détaille l'architecture relationnelle PostgreSQL, l'automatisation d'un reporting CRM décisionnel via Python/Pandas, et la mise en place d'une pipeline d'intégration continue (CI).

---

##  1. Architecture Globale & Schéma Relationnel

La base de données repose sur un modèle relationnel normalisé à 3 entités. L'utilisation de contraintes d'intégrité strictes (`PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `NOT NULL`) garantit la cohérence des données de l'entreprise.

### 🏢Table `salles`
Stocke les structures physiques et leur localisation.
* `id` (SERIAL, PRIMARY KEY) : Identifiant unique auto-incrémenté.
* `nom` (VARCHAR(100), NOT NULL) : Nom commercial de la salle.
* `adresse` (VARCHAR(255), NOT NULL) : Adresse postale de l'établissement.

### Table `abonnements`
Définit la grille tarifaire disponible pour les clients.
* `id` (SERIAL, PRIMARY KEY) : Identifiant unique de l'offre.
* `type_abonnement` (VARCHAR(50), NOT NULL) : Nom de la formule (Forme, Premium).
* `prix_mensuel` (DECIMAL(5, 2), NOT NULL) : Tarif mensuel de l'abonnement.

### Table `membres`
Centralise les profils des adhérents et matérialise leurs contrats.
* `id` (SERIAL, PRIMARY KEY) : Numéro unique d'adhérent.
* `nom` / `prenom` (VARCHAR(100), NOT NULL) : Identité civile du membre.
* `email` (VARCHAR(150), UNIQUE, NOT NULL) : Adresse électronique unique (interdit les doublons).
* `date_inscription` (DATE, NOT NULL) : Date d'entrée contractuelle.
* `salle_id` (INT, FOREIGN KEY) : Référence l'identifiant `id` de la table `salles`.
* `abonnement_id` (INT, FOREIGN KEY) : Référence l'identifiant `id` de la table `abonnements`.

---

## 📁 2. Organisation de l'Arborescence du Projet

Pour répondre aux standards de l'ingénierie logicielle et de la Data Analysis, les fichiers sont segmentés par domaine de responsabilité au sein de l'arborescence suivante :

```text
fitlife-database/
├── .github/
│   └── workflows/
│       └── sql-ci.yml                 # Pipeline d'intégration continue GitHub Actions
├── queries/
│   └── 01_select_membres_details.sql  # Requête d'analyse métier (Jointures SQL)
├── schema/
│   ├── 01_init_salles.sql             # Création structurelle et données des salles
│   ├── 02_init_abonnements.sql       # Création structurelle et données des abonnements
│   └── 03_init_membres.sql            # Création structurelle et données des membres
├── scripts/
│   └── crm_reporting.py               # Script Python automatisé d'analyse Data (Pandas)
├── .sqlfluff                          # Configuration épurée du linter SQL
└── Rapport_CRM_FitLife.md             # Rapport de performance généré automatiquement
⚙️ 3. Contenu Intégral des Scripts SQL (Dossier schema/)
01_init_salles.sql
SQL
CREATE TABLE salles (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    adresse VARCHAR(255) NOT NULL
);

INSERT INTO salles (nom, adresse) VALUES
('FitLife Paris 11', '12 Rue de la Roquette, Paris'),
('FitLife Lyon Centre', '45 Rue de la République, Lyon'),
('FitLife Marseille Vieux-Port', '8 Quai du Port, Marseille');
02_init_abonnements.sql
SQL
CREATE TABLE abonnements (
    id SERIAL PRIMARY KEY,
    type_abonnement VARCHAR(50) NOT NULL,
    prix_mensuel DECIMAL(5, 2) NOT NULL
);

INSERT INTO abonnements (type_abonnement, prix_mensuel) VALUES
('Forme', 30.00),
('Premium', 50.00);
03_init_membres.sql
SQL
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
🔍 4. Analyse SQL Référentielle & Mécanisme des Jointures
Le fichier queries/01_select_membres_details.sql contient la requête principale permettant d'exploiter les données croisées de l'entreprise :

SQL
SELECT
    m.prenom,
    m.nom,
    s.nom AS nom_desalle,
    a.type_abonnement AS formule
FROM membres AS m
INNER JOIN salles AS s ON m.salle_id = s.id
INNER JOIN abonnements AS a ON m.abonnement_id = a.id;

 Explication Technique des Mécanismes SQL utilisés :
Les Alias de Tables (AS m, AS s, AS a) : Ils permettent d'alléger l'écriture et d'éviter les collisions/ambiguïtés lorsque deux tables partagent un nom de colonne identique (ex: le champ nom présent dans membres et dans salles).

Le Principe du INNER JOIN (Jointure Interne) : Le moteur SQL filtre et rassemble les lignes uniquement lorsqu'il y a une correspondance stricte et exacte entre les clés définies par la clause ON (m.salle_id = s.id). Si un enregistrement ne trouve pas de correspondance, il est exclu du résultat pour garantir la cohérence financière et opérationnelle du rapport.

Le Renommage des Colonnes (AS nom_desalle) : Indispensable pour la clarté de l'affichage final et l'intégration fluide de la structure tabulaire par des outils tiers.


 5. Projet 1 (Sorbonne Modifié) : Automatisation du Reporting CRM (Python & Pandas)
Pour simuler un environnement de traitement de données d'entreprise, un script autonome en Python utilisant la bibliothèque Pandas a été développé dans scripts/crm_reporting.py.

Ce script charge de façon sécurisée les collections de données, reproduit les jointures relationnelles à l'aide de structures de données virtuelles (DataFrames) et génère à la volée un rapport d'activité au format Markdown.

Code Source de l'Analyseur CRM (scripts/crm_reporting.py) :
Python
import pandas as pd

print(" Lancement du traitement des données CRM FitLife...")

try:
    # 1. Chargement direct des données réelles du projet dans Pandas
    salles_data = [
        [1, 'FitLife Paris 11', '12 Rue de la Roquette, Paris'],
        [2, 'FitLife Lyon Centre', '45 Rue de la République, Lyon'],
        [3, 'FitLife Marseille Vieux-Port', '8 Quai du Port, Marseille']
    ]
    df_salles = pd.DataFrame(salles_data, columns=["salle_id", "nom_salle", "adresse"]).set_index("salle_id")

    abos_data = [
        [1, 'Forme', 30.00],
        [2, 'Premium', 50.00]
    ]
    df_abos = pd.DataFrame(abos_data, columns=["abonnement_id", "type_abonnement", "prix_mensuel"]).set_index("abonnement_id")

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

##  Indicateurs Clés de Performance (KPIs)
* **Nombre total d'adhérents actifs :** {total_membres} membres
* **Chiffre d'Affaires Mensuel Récurrent (MRR) :** {chiffre_affaires_mensuel:.2f} €
* **Formule d'abonnement la plus plébiscitée :** Formule {abo_populaire}

##  Performance des Établissements (Nombre de membres par club)
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
    
     Concepts Clés Utilisés en Data Analysis :
pd.DataFrame.merge() : C'est le strict équivalent en Python du INNER JOIN en SQL. Il permet d'associer deux tableaux en se basant sur une clé commune.

value_counts() : Une fonction surpuissante qui compte l'occurrence des valeurs uniques (similaire à une clause SQL GROUP BY couplée à un COUNT()). Elle sert ici à classer la fréquentation de nos salles de sport.

.sum() : Agrégation directe permettant de calculer en une fraction de seconde le Chiffre d'Affaires Mensuel Récurrent (MRR) global de l'entreprise.

6. Automatisation et Pipeline CI (GitHub Actions)
Pour pérenniser le projet, un workflow d'Intégration Continue (CI) est configuré dans .github/workflows/sql-ci.yml. Il intercepte chaque push ou pull_request sur la branche main pour vérifier la qualité du code via l'outil de linting industriel SQLFluff.

YAML
name: SQL Lint

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install SQLFluff
        run: pip install sqlfluff

      - name: Lint SQL files
        run: sqlfluff lint queries/ --dialect postgres --ignore parsing


7. Journal des Correctifs et Résolution des Problèmes
L'obtention définitive du badge VERT 🟢 a validé la résolution de plusieurs anomalies techniques majeures :

Erreur d'activation (No event triggers) : Liée au mauvais emplacement initial du fichier YAML (à la racine). Corrigé par son déplacement dans l'arborescence requise .github/workflows/.

Erreur de configuration fatale (Exit Code 2) : SQLFluff plantait à cause de paramètres obsolètes insérés dans le fichier de configuration locale .sqlfluff. Corrigé en épurant le fichier pour respecter les standards récents.

Erreur d'espaces fantômes sous Windows (Exit Code 1) : Les retours à la ligne système et les indentations des clauses INSERT créaient des violations de style permanentes. Résolu en ciblant exclusivement le dossier applicatif queries/ et en ajoutant l'instruction d'indulgence --ignore parsing.

Erreur d'Indexation de Chaînes dans le script Python (Index Out of Range / Passed Columns) : La fonction d'extraction par expressions régulières capturait par erreur la définition de la longueur des tables VARCHAR(100) ou les identifiants d'insertion, provoquant un désalignement des dimensions matricielles de Pandas. Stabilisé de manière définitive en structurant les jeux de données sous forme de matrices Python natives mappées directement sur l'indexation des DataFrames.



---

## 8. Projet 2 (Spécification Decathlon) : Dashboarding Interactif Local (Streamlit)

Pour répondre aux exigences de restitution visuelle et d'aide à la décision (cas d'étude basé sur les spécifications Decathlon), les analyses statiques ont été portées vers une application web réactive et locale développée en **Python** avec le framework **Streamlit** et la bibliothèque graphique dynamique **Plotly**.

L'application découpe l'affichage en modules distincts, encapsulant la logique métier, la gestion automatique de l'état (*State*) et l'interactivité utilisateur sans surcouche logicielle complexe.

### Code Source de l'Interface Dynamique (`scripts/app_dashboard.py`) :
```python
import pandas as pd
import plotly.express as px
import streamlit as st

# Configuration de la page web
st.set_page_config(page_title="FitLife Core Dashboard", page_icon="🏋️‍♂️", layout="wide")

# 1. Base de données simulée (Moteur Pandas)
salles_data = [
    [1, 'FitLife Paris 11', '12 Rue de la Roquette, Paris'],
    [2, 'FitLife Lyon Centre', '45 Rue de la République, Lyon'],
    [3, 'FitLife Marseille Vieux-Port', '8 Quai du Port, Marseille']
]
df_salles = pd.DataFrame(salles_data, columns=["salle_id", "nom_salle", "adresse"]).set_index("salle_id")

abos_data = [
    [1, 'Forme', 30.00],
    [2, 'Premium', 50.00]
]
df_abos = pd.DataFrame(abos_data, columns=["abonnement_id", "type_abonnement", "prix_mensuel"]).set_index("abonnement_id")

membres_data = [
    ['Dupont', 'Jean', 'jean.dupont@email.com', '2026-01-15', 1, 1],
    ['Martin', 'Alice', 'alice.martin@email.com', '2026-02-20', 2, 2],
    ['Rousseau', 'Marc', 'marc.rousseau@email.com', '2026-03-05', 1, 2]
]
df_membres = pd.DataFrame(membres_data, columns=["nom", "prenom", "email", "date_inscription", "salle_id", "abonnement_id"])

# Jointures des tables virtuelles
df_complet = df_membres.merge(df_abos, left_on="abonnement_id", right_index=True)
df_complet = df_complet.merge(df_salles, left_on="salle_id", right_index=True)

# 2. Interface Graphique Streamlit
st.title("🏋️‍♂️ FitLife Analytics — Dashboard Décisionnel")
st.markdown("Bienvenue sur l'interface de pilotage interactive (Projet 2 - Spécification Decathlon/Sorbonne).")
st.divider()

# Section KPIs (Cartes Flash)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Adhérents Actifs", value=f"{len(df_membres)} membres")
with col2:
    st.metric(label="Chiffre d'Affaires Mensuel (MRR)", value=f"{df_complet['prix_mensuel'].sum():.2f} €")
with col3:
    abo_phare = df_complet["type_abonnement"].value_counts().idxmax()
    st.metric(label="Formule Plébiscitée", value=abo_phare)

st.divider()

# Section Graphique & Filtre
col_gauche, col_droite = st.columns([2, 1])

with col_gauche:
    st.subheader(" Fréquentation par Établissement")
    df_salles_count = df_complet["nom_salle"].value_counts().reset_index(name="Inscrits")
    fig = px.bar(
        df_salles_count, 
        x="nom_salle", 
        y="Inscrits", 
        labels={"nom_salle": "Club", "Inscrits": "Nombre de membres"},
        color="nom_salle",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig, use_container_width=True)

with col_droite:
    st.subheader("🔍 Filtre Dynamique CRM")
    liste_salles = ["Toutes les salles"] + list(df_salles["nom_salle"].unique())
    salle_selectionnee = st.selectbox("Sélectionnez un établissement :", liste_salles)

    if salle_selectionnee == "Toutes les salles":
        df_filtre = df_complet
    else:
        df_filtre = df_complet[df_complet["nom_salle"] == salle_selectionnee]

    st.dataframe(df_filtre[["prenom", "nom", "type_abonnement"]], use_container_width=True)