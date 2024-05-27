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
excel_original = pd.ExcelFile(original_file)
df_original = pd.read_excel(original_file, sheet_name='SGT')

# Créer un dictionnaire pour une recherche rapide des catégories par domaine
domain_to_category = dict(zip(df_combined['Domain'], df_combined['Categorization']))

# Diagnostique : vérifier quelques valeurs du dictionnaire
print("Exemple du dictionnaire des domaines à catégories :")
for domain in list(domain_to_category.keys())[:5]:
    print(f"{domain}: {domain_to_category[domain]}")

# Mettre à jour la colonne "Categorie" dans le fichier original
def update_category(row):
    domain = row['domain']
    category = domain_to_category.get(domain)
    if category:
        print(f"Mise à jour de la catégorie pour le domaine {domain}: {category}")
    return category if category else row['Categorie']  # Conserver la valeur existante si non trouvée

# Ajouter une nouvelle colonne 'Categorie' mise à jour
df_original['Categorie'] = df_original.apply(update_category, axis=1)

# Diagnostique : vérifier quelques valeurs mises à jour
print("Exemple des catégories mises à jour :")
print(df_original[['domain', 'Categorie']].head())

# Charger toutes les feuilles du fichier original
sheets = {sheet_name: pd.read_excel(original_file, sheet_name=sheet_name) for sheet_name in excel_original.sheet_names}

# Remplacer la feuille 'SGT' par la version mise à jour
sheets['SGT'] = df_original

# Enregistrer le fichier mis à jour dans un nouveau fichier Excel
with pd.ExcelWriter(final_file) as writer:
    for sheet_name, df in sheets.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Le fichier Excel final '{final_file}' a été généré avec succès.")
