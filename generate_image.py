import csv
from PIL import Image, ImageDraw, ImageFont
import os

# Ouvrir le fichier CSV et le lire
with open('csv/citation.csv', 'r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file, delimiter=':')
    code = 0
    for row in reader:
        # Récupérer les valeurs de 'text' et 'auteur' pour chaque ligne
        auteur = row[0]
        text = row[1]
        # Générer un nom d'image unique
        code = code + 1
        if code < 15:
            nom_template = os.path.join("assets/images", f"{code}.png")
        else:
            code = 1

        # Charger l'image de template
        img = Image.open(nom_template)
        draw = ImageDraw.Draw(img)
        fnt_pensee = ImageFont.truetype("assets/fonts/josefin.ttf", 90)
        fnt_auteur = ImageFont.truetype("assets/fonts/moontime.ttf", 60)

        # Diviser le texte en lignes
        line_width = 750
        lines = []
        line = ''
        for word in text.split():
            bbox = draw.textbbox((0, 0), line + word, font=fnt_pensee)
            if bbox[2] - bbox[0] <= line_width:
                line += f' {word}'
            else:
                lines.append(line.lstrip())
                line = word
        if line:
            lines.append(line.lstrip())

        # Dessiner les lignes de texte centrées verticalement
        bbox = draw.textbbox((0, 0), 'Aj', font=fnt_pensee)  # Use 'Aj' to get a good approximation of line height
        line_height = bbox[3] - bbox[1]
        y = img.size[1] // 2 - line_height * len(lines) // 2

        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=fnt_pensee)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text(((img.size[0] - w) // 2, y), line, font=fnt_pensee, fill=(255, 255, 255))
            y += h

        # Dessiner le nom de l'auteur
        draw.text((420, 870), auteur, font=fnt_auteur, fill=(154, 149, 92))

        nom_image = os.path.join("assets/output/", f"{code}_{auteur}.png")

        # Enregistrer l'image
        img.save(nom_image, "PNG", quality=100, optimize=True)
        img.show()