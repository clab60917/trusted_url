# ce script c'est la version améliorée de aaa.py pour tester avec des listes sans etre connecté
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
input_file = r'/Users/clementarthaud/Documents/VSCODE/HeadmindPartners/SG/trusted_url/domain_list.txt'  # Chemin du fichier de noms de domaine
output_file = r'/Users/clementarthaud/Documents/VSCODE/HeadmindPartners/SG/trusted_url/output_domains_categories.xlsx'  # Chemin du fichier Excel de sortie
edge_driver_path = r'/Users/clementarthaud/Downloads/edgedriver_mac64_m1/msedgedriver'  # Chemin vers msedgedriver
edge_binary_path = r'/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'  # Chemin vers le binaire de Microsoft Edge

# Vérifiez que msedgedriver est exécutable
if not os.access(edge_driver_path, os.X_OK):
    os.chmod(edge_driver_path, 0o755)

# Configuration des options pour Edge
options = EdgeOptions()
options.use_chromium = True
options.binary_location = edge_binary_path

# Initialisation du WebDriver
service = EdgeService(executable_path=edge_driver_path)
driver = webdriver.Edge(service=service, options=options)

def select_product_and_check_url(domain):
    driver.get('https://trustedsource.org/en/feedback/url?action=checksingle&sid=91C3B70BFCACD9BFDB84568175B5A3E2')

    # Attendre que la page se charge
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'product'))
    )

    # Sélectionner la troisième option dans le menu déroulant
    product_dropdown = driver.find_element(By.NAME, 'product')
    product_dropdown.find_elements(By.TAG_NAME, 'option')[2].click()

    # Entrer le nom de domaine
    domain_input = driver.find_element(By.NAME, 'url')
    domain_input.send_keys(domain)

    # Attendre que le bouton "Check URL" soit présent
    check_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="submit"][value="Check URL"]'))
    )

    # Cliquer sur le bouton "Check URL"
    check_button.click()

    # Attendre que le résultat s'affiche
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table.result-table'))
    )

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

    return data

def main():
    # Lire les noms de domaine depuis le fichier texte
    with open(input_file, 'r') as file:
        domains = [line.strip() for line in file.readlines()]

    # Limiter à 80 noms de domaine
    domains = domains[:80]

    # Initialiser une liste pour stocker les données
    all_data = []

    for domain in domains:
        data = select_product_and_check_url(domain)
        all_data.extend(data)
        # Attendre 15 secondes entre chaque requête pour éviter le bannissement de l'IP
        time.sleep(15)

    # Débogage : Afficher les données extraites
    for row in all_data:
        print(row)

    # Créer un DataFrame pandas à partir des données
    df = pd.DataFrame(all_data, columns=['Domain', 'Status', 'Categorization', 'Reputation'])

    # Trier le DataFrame par ordre alphabétique des domaines
    df = df.sort_values(by='Domain').reset_index(drop=True)

    # Exporter le DataFrame en fichier Excel
    df.to_excel(output_file, index=False)

    print(f"Le fichier Excel '{output_file}' a été généré avec succès.")

    # Fermer le navigateur
    driver.quit()

if __name__ == "__main__":
    main()
