import requests
from bs4 import BeautifulSoup
import anthropic

# ================================
# VERNISSAGE — Scraper Artiste V2
# Semaine 2 — enrichissement auto
# ================================

def scraper_wikipedia(nom_artiste):
    """
    Utilise l'API officielle Wikipedia pour récupérer
    les infos sur un artiste, sans risque de blocage.
    """
    
    print(f"Recherche de {nom_artiste} sur Wikipedia...")
    
    # On essaie d'abord en français
    for langue_wiki in ["fr", "en"]:
        url = f"https://{langue_wiki}.wikipedia.org/api/rest_v1/page/summary/{nom_artiste.replace(' ', '_')}"
        
        headers = {"User-Agent": "Vernissage/1.0 (projet etudiant)"}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            texte = data.get("extract", "")
            if texte:
                print(f"Trouvé en {'français' if langue_wiki == 'fr' else 'anglais'} ({len(texte)} caractères)")
                return texte
    
    print(f"Aucune page Wikipedia trouvée pour {nom_artiste}")
    return None


def generer_fiche_bilingue(nom, data_wikipedia):
    """
    Génère une fiche complète en français ET en anglais
    à partir des données récupérées automatiquement.
    """
    
    client = anthropic.Anthropic()
    
    fiches = {}
    
    for langue in ["français", "anglais"]:
        print(f"Génération de la fiche en {langue}...")
        
        prompt = f"""Tu es un expert en marché de l'art contemporain.

À partir de ces informations sur l'artiste, génère une fiche de présentation 
professionnelle en {langue}.

DONNÉES SOURCES :
Nom : {nom}
Informations collectées : {data_wikipedia}

Génère une fiche avec exactement ces 4 sections :

BIOGRAPHIE (3-4 phrases, ton sobre et précis, pas marketing)
POSITIONNEMENT MARCHÉ (2 phrases sur la place de cet artiste dans le marché actuel)
HASHTAGS INSTAGRAM (exactement 3 hashtags pour toucher collectionneurs et amateurs d'art)
PRIX SUGGÉRÉ (fourchette de prix pour une première oeuvre avec justification courte)

Réponds uniquement avec ces 4 sections, sans introduction ni conclusion."""

        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        fiches[langue] = message.content[0].text
    
    return fiches


def sauvegarder_fiche_bilingue(nom, fiches):
    """
    Sauvegarde les deux versions dans un seul fichier bien structuré.
    """
    nom_fichier = f"fiche_v2_{nom.replace(' ', '_').lower()}.txt"
    
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write(f"FICHE ARTISTE — {nom.upper()}\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("VERSION FRANÇAISE\n")
        f.write("-" * 30 + "\n")
        f.write(fiches["français"])
        f.write("\n\n")
        
        f.write("ENGLISH VERSION\n")
        f.write("-" * 30 + "\n")
        f.write(fiches["anglais"])
    
    print(f"Fiche bilingue sauvegardée : {nom_fichier}")


# ================================
# LANCE LE SCRIPT ICI
# ================================

nom_artiste = "Zaria Forman"  # Change le nom pour tester avec d'autres artistes

# Étape 1 : on va chercher les données automatiquement
data = scraper_wikipedia(nom_artiste)

if data:
    # Étape 2 : on génère la fiche bilingue avec ces vraies données
    fiches = generer_fiche_bilingue(nom_artiste, data)
    
    # Étape 3 : on affiche et on sauvegarde
    print("\n" + "=" * 50)
    print("VERSION FRANÇAISE")
    print("=" * 50)
    print(fiches["français"])
    
    print("\n" + "=" * 50)
    print("ENGLISH VERSION")
    print("=" * 50)
    print(fiches["anglais"])
    
    sauvegarder_fiche_bilingue(nom_artiste, fiches)
else:
    print("Impossible de récupérer les données. Vérifie le nom de l'artiste.")