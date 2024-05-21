import os
import time
import pandas as pd
import sys
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
input_file = r'C:\Users\X248317\Desktop\Code\trusted_url\domains_5.txt'  # Chemin du fichier de noms de domaine sur Windows
output_file = r'C:\Users\X248317\Desktop\Code\trusted_url\output_domains_categories.xlsx'  # Chemin du fichier Excel de sortie sur Windows
edge_driver_path = r'C:\Users\X248317\bin\edgedriver-123.0.0.0\msedgedriver.exe'  # Chemin vers msedgedriver sur Windows
edge_binary_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'  # Chemin vers le binaire de Microsoft Edge

# Vérifiez que msedgedriver est exécutable
if not os.access(edge_driver_path, os.X_OK):
    os.chmod(edge_driver_path, 0o755)

# Configuration des options pour Edge
options = EdgeOptions()
options.use_chromium = True
options.binary_location = edge_binary_path

# Rediriger stderr vers un fichier temporaire pour ignorer les erreurs répétitives
original_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')

# Initialisation du WebDriver
service = EdgeService(executable_path=edge_driver_path)
driver = webdriver.Edge(service=service, options=options)

# Restaurer stderr à la fin de l'exécution
def restore_stderr():
    global original_stderr
    sys.stderr.close()
    sys.stderr = original_stderr

def select_product_and_check_url(domain):
    max_attempts = 3
    attempt = 0
    while attempt < max_attempts:
        try:
            print(f"Checking domain: {domain}, attempt {attempt + 1}/{max_attempts}")
            driver.get('https://trustedsource.org/en/feedback/url?action=checksingle&sid=91C3B70BFCACD9BFDB84568175B5A3E2')

            # Attendre que la page se charge
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'product'))
            )
            print("Page loaded.")

            # Sélectionner la troisième option dans le menu déroulant
            product_dropdown = driver.find_element(By.NAME, 'product')
            product_dropdown.find_elements(By.TAG_NAME, 'option')[2].click()
            print("Product selected.")

            # Entrer le nom de domaine
            domain_input = driver.find_element(By.NAME, 'url')
            domain_input.send_keys(domain)
            print("Domain entered.")

            # Attendre que le bouton "Check URL" soit présent
            check_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="submit"][value="Check URL"]'))
            )
            print("Check URL button found.")

            # Cliquer sur le bouton "Check URL"
            check_button.click()
            print("Check URL button clicked.")

            # Attendre que le résultat s'affiche
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'table.result-table'))
            )
            print("Results table found.")

            # Extraire les données du tableau HTML
            table = driver.find_element(By.CSS_SELECTOR, 'table.result-table')
            rows = table.find_elements(By.TAG_NAME, 'tr')
            data = []
            for row in rows[1:]:  # Ignorer la première ligne (en-tête)
                cols = row.find_elements(By.TAG_NAME, 'td')
                cols = [col.text for col in cols]
                # Vérifier que la ligne contient des colonnes pertinentes
                if len(cols) == 5:
                    data.append(cols[1:])  # Exclure la première colonne qui semble être vide
            print(f"Extracted data: {data}")

            return data

        except Exception as e:
            print(f"An error occurred: {e}. Refreshing the page.")
            driver.refresh()
            time.sleep(5)  # Attendre un moment avant de réessayer
            attempt += 1

    print(f"Failed to retrieve data for domain: {domain} after {max_attempts} attempts.")
    return []

def main():
    # Lire les noms de domaine depuis le fichier texte
    with open(input_file, 'r') as file:
        domains = [line.strip() for line in file.readlines()]

    # Limiter à 80 noms de domaine
    domains = domains[:80]
    print(f"Domains to check: {domains}")

    # Initialiser une liste pour stocker les données
    all_data = []

    for domain in domains:
        data = select_product_and_check_url(domain)
        if not data:  # Si aucune donnée n'est trouvée, ajouter des cases vides
            data = [[domain, '', '', '']]
        all_data.extend(data)
        # Attendre 15 secondes entre chaque requête pour éviter le bannissement de l'IP
        time.sleep(15)
        # Pause de 4 secondes entre chaque domaine
        time.sleep(4)

    # Débogage : Afficher les données extraites
    for row in all_data:
        print(row)

    # Créer un DataFrame pandas à partir des données
    df = pd.DataFrame(all_data, columns=['Domain', 'Status', 'Categorization', 'Reputation'])
    print("DataFrame created.")

    # Vérifier et créer le répertoire de sortie si nécessaire
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Exporter le DataFrame en fichier Excel
    df.to_excel(output_file, index=False)
    print(f"Le fichier Excel '{output_file}' a été généré avec succès.")

    # Fermer le navigateur
    driver.quit()
    print("Browser closed.")
    restore_stderr()

if __name__ == "__main__":
    main()
