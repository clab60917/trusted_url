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
from selenium.common.exceptions import TimeoutException
from tqdm import tqdm

# Configuration
input_file = 'path_to_input_file.txt'  # Chemin vers le fichier .txt de domaines
output_file = 'output_domains_categories.xlsx'  # Fichier de sortie
edge_driver_path = 'path_to_your_msedgedriver'  # Chemin vers msedgedriver
edge_binary_path = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'  # Chemin vers le binaire de Microsoft Edge

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
            WebDriverWait(driver, 30).until(
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
            WebDriverWait(driver, 30).until(
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
                    # Utiliser le domaine complet fourni en entrée
                    data.append([domain, cols[2], cols[3], cols[4]])
            print(f"Extracted data: {data}")

            return data

        except TimeoutException as e:
            print(f"Timeout occurred: {e}. Refreshing the page.")
            driver.refresh()
            time.sleep(5)  # Attendre un moment avant de réessayer
            attempt += 1
        except Exception as e:
            print(f"An error occurred: {e}. Retrying.")
            attempt += 1

    print(f"Failed to retrieve data for domain: {domain} after {max_attempts} attempts.")
    return [[domain, '', '', '']]  # Retourner des valeurs vides si échec

def main():
    print(f"Processing file: {input_file}")

    all_data = []

    # Lire les domaines à partir du fichier texte
    with open(input_file, 'r') as file:
        domains = [line.strip() for line in file.readlines()]

    # Progress bar
    pbar = tqdm(total=len(domains), desc="Processing domains")

    for domain in domains:
        # Extraire les données pour le domaine actuel
        data = select_product_and_check_url(domain)
        all_data.extend(data)

        # Mettre à jour la barre de progression
        pbar.update(1)
        # Pause entre chaque domaine pour éviter d'être bloqué
        time.sleep(15)

    pbar.close()

    # Sauvegarder les résultats dans un fichier Excel
    df = pd.DataFrame(all_data, columns=['Domain', 'Status', 'Categorization', 'Reputation'])
    df.to_excel(output_file, index=False)
    print(f"Results saved to {output_file}")

    print("Processing completed.")
    driver.quit()

if __name__ == "__main__":
    try:
        main()
    finally:
        restore_stderr()
