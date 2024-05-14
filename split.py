import pandas as pd
import re

# Fonction pour vérifier si une chaîne est une adresse IP
def is_ip(address):
    ip_pattern = re.compile(r'^\d{1,3}(\.\d{1,3}){3}$')
    return bool(ip_pattern.match(address))

# Lire le fichier Excel
file_path = 'votre_fichier.xlsx'  
df = pd.read_excel(file_path)

# Extraire les domaines et filtrer les IPs
domains = df['domain']
filtered_domains = [domain for domain in domains if not is_ip(domain)]

# Trier les domaines par ordre alphabétique
filtered_domains.sort()

# Écrire les domaines dans des fichiers texte, 80 domaines par fichier
file_count = 1
for i in range(0, len(filtered_domains), 80):
    with open(f'domains_{file_count}.txt', 'w') as f:
        for domain in filtered_domains[i:i + 80]:
            f.write(f"{domain}\n")
    file_count += 1

print(f"{file_count - 1} fichiers générés.")
