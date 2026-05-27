import pandas as pd
import plotly.express as px
import streamlit as st

# Configuration de la page web (titre dans l'onglet, icône et disposition large)
st.set_page_config(
    page_title="FitLife Core Dashboard", page_icon="🏋️‍♂️", layout="wide"
)

# 1. Base de données simulée (Moteur Pandas)
salles_data = [
    [1, "FitLife Paris 11", "12 Rue de la Roquette, Paris"],
    [2, "FitLife Lyon Centre", "45 Rue de la République, Lyon"],
    [3, "FitLife Marseille Vieux-Port", "8 Quai du Port, Marseille"],
]
df_salles = pd.DataFrame(
    salles_data, columns=["salle_id", "nom_salle", "adresse"]
).set_index("salle_id")

abos_data = [[1, "Forme", 30.00], [2, "Premium", 50.00]]
df_abos = pd.DataFrame(
    abos_data, columns=["abonnement_id", "type_abonnement", "prix_mensuel"]
).set_index("abonnement_id")

membres_data = [
    ["Dupont", "Jean", "jean.dupont@email.com", "2026-01-15", 1, 1],
    ["Martin", "Alice", "alice.martin@email.com", "2026-02-20", 2, 2],
    ["Rousseau", "Marc", "marc.rousseau@email.com", "2026-03-05", 1, 2],
]
df_membres = pd.DataFrame(
    membres_data,
    columns=[
        "nom",
        "prenom",
        "email",
        "date_inscription",
        "salle_id",
        "abonnement_id",
    ],
)

# Jointures des tables virtuelles
df_complet = df_membres.merge(df_abos, left_on="abonnement_id", right_index=True)
df_complet = df_complet.merge(df_salles, left_on="salle_id", right_index=True)

# 2. Interface Graphique Streamlit
st.title("🏋️‍♂️ FitLife Analytics — Dashboard Décisionnel")
st.markdown(
    "Bienvenue sur l'interface de pilotage interactive."
)
st.divider()

# Section KPIs (Cartes Flash)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Adhérents Actifs", value=f"{len(df_membres)} membres")
with col2:
    st.metric(
        label="Chiffre d'Affaires Mensuel (MRR)",
        value=f"{df_complet['prix_mensuel'].sum():.2f} €",
    )
with col3:
    abo_phare = df_complet["type_abonnement"].value_counts().idxmax()
    st.metric(label="Formule Plébiscitée", value=abo_phare)

st.divider()

# Section Graphique & Filtre
col_gauche, col_droite = st.columns([2, 1])

with col_gauche:
    st.subheader("🏢 Fréquentation par Établissement")
    # Comptage des membres par salle pour alimenter le graphique
    df_salles_count = (
        df_complet["nom_salle"].value_counts().reset_index(name="Inscrits")
    )
    # Création du graphique interactif avec Plotly
    fig = px.bar(
        df_salles_count,
        x="nom_salle",
        y="Inscrits",
        labels={"nom_salle": "Club", "Inscrits": "Nombre de membres"},
        color="nom_salle",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    st.plotly_chart(fig, use_container_width=True)

with col_droite:
    st.subheader("🔍 Filtre Dynamique CRM")
    # Menu déroulant interactif
    liste_salles = ["Toutes les salles"] + list(df_salles["nom_salle"].unique())
    salle_selectionnee = st.selectbox(
        "Sélectionnez un établissement :", liste_salles
    )

    # Filtrage du tableau en fonction du choix de l'utilisateur
    if salle_selectionnee == "Toutes les salles":
        df_filtre = df_complet
    else:
        df_filtre = df_complet[df_complet["nom_salle"] == salle_selectionnee]

    # Affichage du tableau de données dynamique
    st.dataframe(
        df_filtre[["prenom", "nom", "type_abonnement"]],
        use_container_width=True,
    )