from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
import os
import textwrap

def generer_pdf_recette(data, image_path, output_name="recette_grand_mere.pdf"):
    c = canvas.Canvas(output_name, pagesize=A4)
    width, height = A4

    # 1. Police
    current_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(current_dir, "Au Bord de la Seine.ttf")
    pdfmetrics.registerFont(TTFont('GrandMere', font_path))

    # 2. Fond
    c.setFillColor(HexColor('#FDF5E6'))
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # 3. Titre
    c.setFont('GrandMere', 40)
    c.setFillColor(HexColor('#4B2E1E'))
    c.drawCentredString(width/2, height - 80, data.get('titre', 'Ma Recette'))

    # 4. Image
    if image_path and os.path.exists(image_path):
        c.setStrokeColor(HexColor('#8B4513'))
        c.rect(width - 230, height - 300, 180, 180, stroke=1, fill=0)
        c.drawImage(image_path, width - 225, height - 295, width=170, height=170)

    # 5. Ingrédients (Correction du format Dictionnaire)
    c.setFont('GrandMere', 22)
    c.drawString(60, height - 150, "Ce qu'il nous faut :")
    c.setFont('GrandMere', 18)
    y = height - 180
    for ing in data.get('ingredients', []):
        if isinstance(ing, dict):
            # On construit la phrase "Nom (Quantité)"
            texte = f"{ing.get('nom', '')} ({ing.get('quantite', '')})"
        else:
            texte = str(ing)
        c.drawString(80, y, f"- {texte}")
        y -= 25

    # 6. Étapes (Correction du format Dictionnaire)
    y -= 30
    c.setFont('GrandMere', 22)
    c.drawString(60, y, "En cuisine :")
    y -= 30
    c.setFont('GrandMere', 16)

    wrapper_etapes = textwrap.TextWrapper(width=60)
    for i, etape in enumerate(data.get('etapes', []), 1):
        # On extrait seulement le texte de l'étape
        texte_etape = etape.get('etape', str(etape)) if isinstance(etape, dict) else str(etape)
        
        lignes = wrapper_etapes.wrap(text=f"{i}. {texte_etape}")
        for line in lignes:
            if y < 160: break
            c.drawString(80, y, line)
            y -= 20
        y -= 5

    # 7. Astuce
    c.setDash(2, 2)
    c.roundRect(50, 40, 500, 100, 10, stroke=1, fill=0)
    c.setDash(1, 0)
    c.setFont('GrandMere', 18)
    c.drawString(70, 115, "Le secret de Grand-Mère :")
    c.setFont('GrandMere', 15)
    
    astuce_texte = data.get('astuce', '')
    wrapper_astuce = textwrap.TextWrapper(width=75)
    lignes_astuce = wrapper_astuce.wrap(text=astuce_texte)
    y_astuce = 95
    for line in lignes_astuce[:3]:
        c.drawString(70, y_astuce, line)
        y_astuce -= 18

    c.save()
    return output_name
