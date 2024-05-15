from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
import os
# Chemin vers msedgedriver
edge_driver_path = r'/Users/clementarthaud/Downloads/edgedriver_mac64_m1/msedgedriver'  # Remplacez par le chemin correct

# Vérifiez que msedgedriver est exécutable
if not os.access(edge_driver_path, os.X_OK):
    os.chmod(edge_driver_path, 0o755)

# Configuration des options pour Edge
options = EdgeOptions()
options.use_chromium = True

# Initialisation du WebDriver
service = EdgeService(executable_path=edge_driver_path)
driver = webdriver.Edge(service=service, options=options)

try:
    # Ouvrir une page web simple
    driver.get('https://www.google.com')

    # Vérifier que la page est chargée
    if "Google" in driver.title:
        print("La page Google a été chargée avec succès.")
    else:
        print("Échec du chargement de la page Google.")
finally:
    # Fermer le navigateur
    driver.quit()
