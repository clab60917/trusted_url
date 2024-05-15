import pandas as pd

# Définir les chemins des fichiers
original_file = 'path_to_original_file.xlsx'  # fichier Excel original
output_file = 'output_domains_categories.xlsx'  # Le fichier généré par le deuxième script
final_file = 'final_updated_file.xlsx'  # Le fichier Excel final avec les mises à jour

# Lire le fichier Excel original
df_original = pd.read_excel(original_file, sheet_name='SGT')

# Lire le fichier contenant les domaines et catégories
df_output = pd.read_excel(output_file)

# Créer un dictionnaire pour une recherche rapide des catégories par domaine
domain_to_category = dict(zip(df_output['Domain'], df_output['Category']))

# Mettre à jour la colonne "categorie" dans le fichier original
def update_category(row):
    domain = row['domain']
    return domain_to_category.get(domain, row['categorie'])  # Conserver la valeur existante si non trouvée

# Ajouter une nouvelle colonne 'categorie' mise à jour
df_original['categorie'] = df_original.apply(update_category, axis=1)

# Enregistrer le fichier mis à jour dans un nouveau fichier Excel
df_original.to_excel(final_file, index=False)

print(f"Le fichier Excel final '{final_file}' a été généré avec succès.")
