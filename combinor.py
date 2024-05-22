import pandas as pd
import glob

# Définir les chemins des fichiers
original_file = 'path_to_original_file.xlsx'  # Remplacez par le chemin de votre fichier Excel original
output_pattern = 'output_domains_categories*.xlsx'  # Modèle pour trouver tous les fichiers output
final_file = 'final_updated_file.xlsx'  # Le fichier Excel final avec les mises à jour

# Lire tous les fichiers output et les combiner en un seul DataFrame
all_files = glob.glob(output_pattern)
df_list = []

for file in all_files:
    df = pd.read_excel(file)
    df_list.append(df)

df_combined = pd.concat(df_list, ignore_index=True)

# Enregistrer le fichier combiné (optionnel)
df_combined.to_excel('combined_output_domains_categories.xlsx', index=False)
print("Tous les fichiers de sortie ont été combinés avec succès.")

# Lire le fichier Excel original
df_original = pd.read_excel(original_file, sheet_name='SGT')

# Créer un dictionnaire pour une recherche rapide des catégories par domaine
domain_to_category = dict(zip(df_combined['Domain'], df_combined['Category']))

# Mettre à jour la colonne "Categorie" dans le fichier original
def update_category(row):
    domain = row['domain']
    return domain_to_category.get(domain, row['Categorie'])  # Conserver la valeur existante si non trouvée

# Ajouter une nouvelle colonne 'Categorie' mise à jour
df_original['Categorie'] = df_original.apply(update_category, axis=1)

# Enregistrer le fichier mis à jour dans un nouveau fichier Excel
df_original.to_excel(final_file, index=False)

print(f"Le fichier Excel final '{final_file}' a été généré avec succès.")
