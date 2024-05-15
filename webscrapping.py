# pip install msedge-selenium-tools selenium pandas openpyxl

import os
import time
import pandas as pd
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
input_directory = r'C:\path\to\your\txt\files'  # Utilisez une chaîne brute pour éviter les problèmes d'échappement
output_file = r'C:\path\to\your\output_domains_categories.xlsx'  # Utilisez une chaîne brute
username = 'your_username'  # Remplacez par votre nom d'utilisateur
password = 'your_password'  # Remplacez par votre mot de passe

# Chemin vers le Edge WebDriver
edge_driver_path = r'C:\path\to\edgedriver.exe'  # Remplacez par le chemin correct

# Configuration des options pour Edge
options = EdgeOptions()
options.use_chromium = True  # Utiliser Chromium

# Initialisation du WebDriver
driver = Edge(executable_path=edge_driver_path, options=options)

def login_to_trustedsource():
    driver.get('https://trustedsource.org/en/feedback/url?action=checklist&sid=91C3B70BFCACD9BFDB84568175B5A3E2')
    
    # Attendre que la page de connexion se charge
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'username'))
    )

    # Entrer les informations d'identification
    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)

    # Attendre que la connexion se termine
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'Customer URL Ticketing System'))
    )

def upload_and_check_file(file_path):
    driver.get('https://trustedsource.org/en/feedback/url?action=checklist&sid=91C3B70BFCACD9BFDB84568175B5A3E2')

    # Attendre que la page de téléchargement de fichier se charge
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'file'))
    )

    # Téléverser le fichier
    driver.find_element(By.NAME, 'file').send_keys(file_path)

    # Cliquer sur le bouton "Check URL List"
    driver.find_element(By.NAME, 'submit').click()

    # Attendre que le résultat s'affiche
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, 'table'))
    )

    # Copier les résultats du tableau
    table = driver.find_element(By.TAG_NAME, 'table')
    results = table.text

    return results

def main():
    # Connexion au site
    login_to_trustedsource()

    # Initialiser une liste pour stocker les données
    data = []

    # Parcourir tous les fichiers dans le répertoire
    for filename in os.listdir(input_directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_directory, filename)
            results = upload_and_check_file(file_path)
            
            # Traiter les résultats
            lines = results.split('\n')
            for line in lines[1:]:  # Sauter la ligne d'en-tête
                parts = line.split()
                if len(parts) >= 2:
                    domain = parts[0]
                    category = ' '.join(parts[1:])
                    data.append([domain, category])

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
