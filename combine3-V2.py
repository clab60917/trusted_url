import pandas as pd
import glob

# Définir les chemins des fichiers
original_file = 'path_to_original_file.xlsx'  # Remplacez par le chemin de votre fichier Excel original
output_pattern = 'output_domains_categories*.xlsx'  # Modèle pour trouver tous les fichiers output
final_file = 'final_updated_file.xlsx'  # Le fichier Excel final avec les mises à jour
correspondence_file = 'domain_correspondence.txt'  # Fichier pour enregistrer les correspondances de domaines

# Lire tous les fichiers output et les combiner en un seul DataFrame
all_files = glob.glob(output_pattern)
df_list = []

for file in all_files:
    df = pd.read_excel(file)
    df_list.append(df)

df_combined = pd.concat(df_list, ignore_index=True)

# Supprimer le préfixe 'http://' des domaines et nettoyer les catégories
df_combined['Domain'] = df_combined['Domain'].str.replace(r'^http://', '', regex=True)
df_combined['Categorization'] = df_combined['Categorization'].str.replace(r'^-\s*', '', regex=True)

# Enregistrer le fichier combiné (optionnel)
df_combined.to_excel('combined_output_domains_categories.xlsx', index=False)
print("Tous les fichiers de sortie ont été combinés avec succès.")

# Lire le fichier Excel original
excel_original = pd.ExcelFile(original_file)
df_original = pd.read_excel(original_file, sheet_name='SGT')

# Fonction pour trouver la meilleure correspondance
def match_domain(truncated_domain, domain_list):
    if truncated_domain.endswith('...'):
        truncated_domain_base = truncated_domain[:-3]
        matches = [d for d in domain_list if d.startswith(truncated_domain_base)]
        if matches:
            print(f"Match found: {truncated_domain} => {matches[0]}")
            return matches[0]
    return truncated_domain

# Créer un dictionnaire pour une recherche rapide des catégories par domaine
domain_to_category = dict(zip(df_combined['Domain'], df_combined['Categorization']))

# Enregistrer les correspondances de domaines
correspondences = []

# Mettre à jour la colonne "Categorie" dans le fichier original
def update_category(row):
    domain = row['domain']
    matched_domain = match_domain(domain, domain_to_category.keys())
    if matched_domain != domain:
        correspondences.append(f"{domain} => {matched_domain}")
    category = domain_to_category.get(matched_domain)
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

# Enregistrer les correspondances dans un fichier texte
with open(correspondence_file, 'w') as f:
    f.write("\n".join(correspondences))

print(f"Le fichier de correspondances '{correspondence_file}' a été généré avec succès.")
