import os
import time
import pandas as pd
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
domains = ["google.com"]  # Liste des domaines à tester
output_file = r'/Users/clementarthaud/Documents/VSCODE/HeadmindPartners/SG/trusted_url'  # Utilisez une chaîne brute pour éviter les problèmes d'échappement
edge_driver_path = r'/Users/clementarthaud/Downloads/edgedriver_mac64_m1/msedgedriver'  # Remplacez par le chemin correct

# Configuration des options pour Edge
options = EdgeOptions()
options.use_chromium = True

# Initialisation du WebDriver
driver = Edge(executable_path=edge_driver_path, options=options)

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

    # Cliquer sur le bouton "Check URL"
    driver.find_element(By.NAME, 'submit').click()

    # Attendre que le résultat s'affiche
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, 'table'))
    )

    # Télécharger le fichier CSV
    download_link = driver.find_element(By.LINK_TEXT, 'Download CSV')
    download_link.click()

    # Attendre le téléchargement
    time.sleep(5)  # Ajustez ce délai si nécessaire

def main():
    # Initialiser une liste pour stocker les données
    data = []

    for domain in domains:
        select_product_and_check_url(domain)
        # Traitement du fichier CSV (supposons qu'il soit téléchargé dans le répertoire de téléchargement par défaut)
        csv_file = r'/path/to/your/downloads/directory/results.csv'  # Chemin du fichier téléchargé
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            for index, row in df.iterrows():
                data.append([row['URL'], row['Categorization']])
            os.remove(csv_file)  # Supprimer le fichier après traitement

    # Créer un DataFrame pandas à partir des données
    df = pd.DataFrame(data, columns=['Domain', 'Category'])

    # Trier le DataFrame par ordre alphabétique des domaines
    df = df.sort_values(by='Domain').reset_index(drop=True)

    # Exporter le DataFrame en fichier Excel
    df.to_excel(output_file, index=False)

    print(f"Le fichier Excel '{output_file}' a été généré avec succès.")

    # Fermer le navigateur
    driver.quit()

if __name__ == "__main__":
    main()
