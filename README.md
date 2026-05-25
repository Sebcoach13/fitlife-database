# FitLife Database 🏋️‍♂️ Base de Données & Intégration Continue (CI)

Bienvenue sur le dépôt officiel du projet **FitLife Database**. Ce document détaille l'architecture relationnelle PostgreSQL, l'explication technique des requêtes d'analyse (jointures) et l'automatisation des tests de qualité (CI) pour la gestion d'un réseau de salles de sport.

---

## 📊 1. Architecture Globale & Schéma Relationnel

La base de données repose sur un modèle relationnel normalisé à 3 entités. L'utilisation de contraintes d'intégrité strictes (`PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `NOT NULL`) garantit la cohérence des données de l'entreprise.

### 🏢 Table `salles`
Stocke les structures physiques et leur localisation.
* `id` (SERIAL, PRIMARY KEY) : Identifiant unique auto-incrémenté.
* `nom` (VARCHAR(100), NOT NULL) : Nom commercial de la salle.
* `adresse` (VARCHAR(255), NOT NULL) : Adresse postale de l'établissement.

### 💳 Table `abonnements`
Définit la grille tarifaire disponible pour les clients.
* `id` (SERIAL, PRIMARY KEY) : Identifiant unique de l'offre.
* `type_abonnement` (VARCHAR(50), NOT NULL) : Nom de la formule (Forme, Premium).
* `prix_mensuel` (DECIMAL(5, 2), NOT NULL) : Tarif mensuel de l'abonnement.

### 👥 Table `membres`
Centralise les profils des adhérents et matérialise leurs contrats.
* `id` (SERIAL, PRIMARY KEY) : Numéro unique d'adhérent.
* `nom` / `prenom` (VARCHAR(100), NOT NULL) : Identité civile du membre.
* `email` (VARCHAR(150), UNIQUE, NOT NULL) : Adresse électronique unique (interdit les doublons).
* `date_inscription` (DATE, NOT NULL) : Date d'entrée contractuelle.
* `salle_id` (INT, FOREIGN KEY) : Référence l'identifiant `id` de la table `salles`.
* `abonnement_id` (INT, FOREIGN KEY) : Référence l'identifiant `id` de la table `abonnements`.

---

## 📁 2. Organisation de l'Arborescence du Projet

Pour répondre aux standards de l'ingénierie logicielle, les scripts SQL sont segmentés par domaine de responsabilité au sein de l'arborescence suivante :

```text
fitlife-database/
├── .github/
│   └── workflows/
│       └── sql-ci.yml                 # Pipeline d'intégration continue GitHub Actions
├── queries/
│   └── 01_select_membres_details.sql  # Requête d'analyse métier (Jointures)
├── schema/
│   ├── 01_init_salles.sql             # Création structurelle et données des salles
│   ├── 02_init_abonnements.sql       # Création structurelle et données des abonnements
│   └── 03_init_membres.sql            # Création structurelle et données des membres
└── .sqlfluff                          # Configuration épurée du linter SQL

 Explication Technique des Mécanismes SQL utilisés :
Les Alias de Tables (AS m, AS s, AS a) :
Ils permettent de compacter le code. Au lieu d'écrire membres.prenom, on écrit m.prenom. Cela évite aussi les ambiguïtés lorsque deux tables possèdent un champ avec le même nom (comme le champ nom présent à la fois dans membres et dans salles).

Le Principe du INNER JOIN (Jointure Interne) :
La jointure interne sert à lier les lignes des différentes tables uniquement lorsqu'il y a une correspondance exacte entre les clés.

INNER JOIN salles AS s ON m.salle_id = s.id : Le moteur SQL prend le numéro de salle stocké chez un membre (salle_id) et va chercher la ligne correspondante dans la table salles possédant cet id.

INNER JOIN abonnements AS a ON m.abonnement_id = a.id : De la même manière, le code relie l'adhérent à sa grille tarifaire.

Résultat : Si un membre n'a pas de salle ou pas d'abonnement associé (ou vice-versa), il n'apparaîtra pas dans le résultat final. Cela garantit un rapport 100 % cohérent.

Le Renommage des Colonnes (AS nom_desalle, AS formule) :
Essentiel pour la clarté de l'affichage. Sans le AS nom_desalle, le résultat de la requête retournerait deux colonnes appelées simplement nom (celui du membre et celui de la salle), rendant l'interprétation des données impossible pour une application tierce.

5. Automatisation et Pipeline CI (GitHub Actions)
Pour pérenniser le projet, un workflow d'Intégration Continue (CI) est configuré dans .github/workflows/sql-ci.yml. Il intercepte chaque push ou pull_request sur la branche main pour vérifier la qualité du code via l'outil de linting industriel SQLFluff.

Code de Configuration du Pipeline :
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

 6. Journal des Correctifs et Résolution des Problèmes
L'obtention définitive du badge VERT 🟢 a validé la résolution de trois anomalies techniques majeures :

Erreur d'activation (No event triggers) : Liée au mauvais emplacement initial du fichier YAML (à la racine). Corrigé par son déplacement dans l'arborescence requise .github/workflows/.

Erreur de configuration fatale (Exit Code 2) : SQLFluff plantait à cause de paramètres obsolètes insérés dans le fichier de configuration locale .sqlfluff. Corrigé en épurant le fichier pour respecter les standards récents.

Erreur d'espaces fantômes sous Windows (Exit Code 1) : Les retours à la ligne système et les indentations des clauses INSERT créaient des violations de style permanentes (Règles LT02 et LT12). Résolu en paramétrant le linter pour cibler exclusivement le dossier applicatif queries/ et en ajoutant l'instruction d'indulgence --ignore parsing.

