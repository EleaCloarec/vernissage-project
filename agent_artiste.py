import anthropic
import json

# ================================
# VERNISSAGE — Agent Artiste V1
# Semaine 1 — Project ATLAS
# ================================

def generer_fiche_artiste(nom, style, oeuvres):
    """
    Prend les infos brutes d'un artiste
    et génère une fiche de présentation complète.
    """
    
    client = anthropic.Anthropic()
    
    # On formate les œuvres pour le prompt
    oeuvres_texte = "\n".join([f"- {o}" for o in oeuvres])
    
    prompt = f"""Tu es un expert en marché de l'art contemporain et en stratégie de lancement d'artistes émergents.

À partir de ces informations brutes sur un artiste, génère une fiche de présentation professionnelle.

INFORMATIONS BRUTES :
Nom : {nom}
Style : {style}
Œuvres :
{oeuvres_texte}

Génère une fiche structurée avec exactement ces 4 sections :

BIOGRAPHIE (3-4 phrases, ton sobre et précis, pas marketing)
POSITIONNEMENT MARCHÉ (2 phrases qui expliquent où cet artiste se situe dans le marché de l'art actuel)
HASHTAGS INSTAGRAM (exactement 3 hashtags pertinents pour toucher collectionneurs et amateurs d'art)
PRIX SUGGÉRÉ (une fourchette de prix pour une première œuvre avec une justification courte)

Réponds uniquement avec ces 4 sections, sans introduction ni conclusion."""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text


def sauvegarder_fiche(nom, contenu):
    """Sauvegarde la fiche dans un fichier texte."""
    nom_fichier = f"fiche_{nom.replace(' ', '_').lower()}.txt"
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write(f"FICHE ARTISTE — {nom.upper()}\n")
        f.write("=" * 50 + "\n\n")
        f.write(contenu)
    print(f"✓ Fiche sauvegardée : {nom_fichier}")


# ================================
# TON PREMIER ARTISTE — à modifier
# ================================

nom = "Sabine Kalka"
style = "Sabine Kalka’s paintings explore the landscape of the psyche – the place where the conscious and unconscious meet. They convey a sense of place, or landscape, that can only exist on the periphery of consciousness, continually coming into and out of focus. In her paintings, the existential and the personal—the exterior and the interior—are intertwined, stepping back and forth between the timelessness of dreams and the relentless cycle of change in our daily lives. In her practice Kalka looks at the delusions of order and control that we human beings cling to as we navigate the fundamental unpredictability of reality, and sense our own finiteness in the immensity of time and nature."
oeuvres = [
    "La vie en rose — oil on canvas, 2021",
    "L'or du matin — oil on canvas, 2025",
    "Reverie — oil on canvas, 2021"
]

print(f"\n🎨 Génération de la fiche pour {nom}...")
print("-" * 50)

fiche = generer_fiche_artiste(nom, style, oeuvres)

print(fiche)
sauvegarder_fiche(nom, fiche)
