import os
import pandas as pd

# Configuration des chemins de fichiers
input_directory = "path_to_directory_with_output_files"  # Répertoire contenant les fichiers de résultats de catégorisation
original_file = "path_to_original_file.xlsx"  # Chemin vers le fichier Excel original
final_file = "final_updated_file.xlsx"  # Chemin vers le fichier Excel final mis à jour

# Charger le fichier Excel original
df_original = pd.read_excel(original_file, sheet_name='SGT')

# Combiner tous les fichiers de résultats de catégorisation
all_data = []
for filename in os.listdir(input_directory):
    if filename.startswith("output_domains_categories") and filename.endswith(".xlsx"):
        df = pd.read_excel(os.path.join(input_directory, filename))
        all_data.append(df)

df_combined = pd.concat(all_data, ignore_index=True)

# Créer un dictionnaire pour une recherche rapide des catégories et des statuts par domaine
domain_to_category = dict(zip(df_combined['Domain'], df_combined['Categorization']))
domain_to_status = dict(zip(df_combined['Domain'], df_combined['Status']))

# Mettre à jour la colonne "Categorie" et ajouter la colonne "Status-Bis" dans le fichier original
def update_category(row):
    domain = row['domain']
    category = domain_to_category.get(domain, row['Categorie'])
    if isinstance(category, str) and category.startswith('-'):
        category = category[1:].strip()
    return category

def update_status(row):
    domain = row['domain']
    return domain_to_status.get(domain, "")

# Ajouter une nouvelle colonne 'Categorie' mise à jour et une colonne 'Status-Bis'
df_original['Categorie'] = df_original.apply(update_category, axis=1)
df_original.insert(df_original.columns.get_loc('Categorie') + 1, 'Status-Bis', df_original.apply(update_status, axis=1))

# Enregistrer le fichier mis à jour dans un nouveau fichier Excel
df_original.to_excel(final_file, index=False)

print(f"Le fichier Excel final '{final_file}' a été généré avec succès.")
