import pandas as pd
import os
import re

# Définir le chemin du répertoire contenant les fichiers texte
input_directory = 'path_to_your_txt_files'  # Remplacez par le chemin de votre répertoire
output_file = 'output_domains_categories.xlsx'

# Initialiser une liste pour stocker les données
data = []

# Expression régulière pour filtrer les fichiers de la forme "O1.txt", "O2.txt", etc.
file_pattern = re.compile(r'^O\d+\.txt$')

# Parcourir tous les fichiers dans le répertoire
for filename in os.listdir(input_directory):
    if file_pattern.match(filename):
        with open(os.path.join(input_directory, filename), 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                # Nettoyer la ligne et ignorer les lignes de titre et vides
                line = line.strip()
                if line and not line.startswith('URL') and 'http://' in line:
                    # Diviser la ligne sur les tabulations
                    parts = line.split('\t')
                    if len(parts) >= 3:
                        url = parts[0]
                        category = parts[2]
                        # Nettoyer les colonnes URL et Categorization
                        url = url.replace('http://', '').replace('https://', '').strip()
                        category = category.split('- ')[1].strip() if '- ' in category else category.strip()
                        data.append([url, category])

# Créer un DataFrame pandas à partir des données
df = pd.DataFrame(data, columns=['Domain', 'Category'])

# Trier le DataFrame par ordre alphabétique des domaines
df = df.sort_values(by='Domain').reset_index(drop=True)

# Exporter le DataFrame en fichier Excel
df.to_excel(output_file, index=False)

print(f"Le fichier Excel '{output_file}' a été généré avec succès.")
