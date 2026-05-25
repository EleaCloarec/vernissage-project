import streamlit as st
import plotly.express as px
import pandas as pd

# ================================
# VERNISSAGE — Dashboard V1
# Semaine 3 — Visualisation
# ================================

# Configuration de la page (titre, icône, layout large)
st.set_page_config(
    page_title="Vernissage — Art Émergent",
    page_icon="🎨",
    layout="wide"
)

# ================================
# LES DONNÉES
# Pour l'instant on les entre à la main.
# En semaine 4 elles viendront automatiquement du scraper.
# ================================

artistes = [
    {
        "nom": "Zaria Forman",
        "pays": "États-Unis",
        "style": "Dessin hyperréaliste",
        "medium": "Pastel",
        "theme": "Environnement",
        "prix_min": 8000,
        "prix_max": 25000,
        "wikipedia": True,
        "instagram_followers": 98000,
        "expositions": 45,
        "score_emergent": 72
    },
    {
        "nom": "Samantha Keely Smith",
        "pays": "États-Unis",
        "style": "Peinture abstraite",
        "medium": "Huile",
        "theme": "Nature",
        "prix_min": 3000,
        "prix_max": 18000,
        "wikipedia": False,
        "instagram_followers": 12000,
        "expositions": 28,
        "score_emergent": 85
    },
    {
        "nom": "Sabine Kalka",
        "pays": "Allemagne",
        "style": "Peinture contemporaine",
        "medium": "Huile",
        "theme": "Figuratif",
        "prix_min": 2000,
        "prix_max": 8000,
        "wikipedia": False,
        "instagram_followers": 4500,
        "expositions": 15,
        "score_emergent": 91
    },
    {
        "nom": "Yayoi Kusama",
        "pays": "Japon",
        "style": "Art contemporain",
        "medium": "Mixte",
        "theme": "Psychédélique",
        "prix_min": 150000,
        "prix_max": 1000000,
        "wikipedia": True,
        "instagram_followers": 1200000,
        "expositions": 500,
        "score_emergent": 10
    }
]

df = pd.DataFrame(artistes)

# ================================
# INTERFACE — HEADER
# ================================

st.title("🎨 Vernissage")
st.subheader("Plateforme de découverte d'art émergent")
st.markdown("---")

# ================================
# MÉTRIQUES EN HAUT
# ================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Artistes référencés", len(df))

with col2:
    st.metric("Prix moyen minimum", f"{int(df['prix_min'].mean()):,} €")

with col3:
    artistes_emergents = len(df[df['score_emergent'] > 70])
    st.metric("Artistes très émergents", artistes_emergents)

with col4:
    st.metric("Pays représentés", df['pays'].nunique())

st.markdown("---")

# ================================
# DEUX COLONNES PRINCIPALES
# ================================

col_gauche, col_droite = st.columns(2)

with col_gauche:
    st.subheader("Prix par artiste")
    
    # Graphique à barres avec fourchette de prix
    fig_prix = px.bar(
        df.sort_values("prix_min"),
        x="nom",
        y=["prix_min", "prix_max"],
        barmode="group",
        labels={"value": "Prix (€)", "nom": "Artiste", "variable": ""},
        color_discrete_map={"prix_min": "#8B5CF6", "prix_max": "#C4B5FD"},
        title="Fourchette de prix par artiste"
    )
    fig_prix.update_layout(
        legend=dict(orientation="h"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_prix, use_container_width=True)

with col_droite:
    st.subheader("Score émergent vs Followers Instagram")
    
    fig_scatter = px.scatter(
        df,
        x="instagram_followers",
        y="score_emergent",
        size="prix_max",
        color="pays",
        hover_name="nom",
        labels={
            "instagram_followers": "Followers Instagram",
            "score_emergent": "Score émergent (100 = très émergent)",
            "pays": "Pays"
        },
        title="Potentiel émergent vs visibilité sociale"
    )
    fig_scatter.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# ================================
# TABLEAU INTERACTIF
# ================================

st.subheader("Tous les artistes")

# Filtres
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    pays_filtre = st.multiselect(
        "Filtrer par pays",
        options=df['pays'].unique(),
        default=df['pays'].unique()
    )

with col_f2:
    budget_max = st.slider(
        "Budget maximum (€)",
        min_value=0,
        max_value=int(df['prix_max'].max()),
        value=int(df['prix_max'].max())
    )

with col_f3:
    score_min = st.slider(
        "Score émergent minimum",
        min_value=0,
        max_value=100,
        value=0
    )

# Application des filtres
df_filtre = df[
    (df['pays'].isin(pays_filtre)) &
    (df['prix_min'] <= budget_max) &
    (df['score_emergent'] >= score_min)
]

st.dataframe(
    df_filtre[["nom", "pays", "style", "medium", "prix_min", "prix_max", "score_emergent"]],
    use_container_width=True,
    hide_index=True
)

st.markdown("---")
st.caption("Vernissage — Project ATLAS 2026")