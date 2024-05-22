
# Trusted URL

## Introduction

Ce projet a pour but de trier les domaines whitelistés au niveau d'un proxy de chez Skylight Security (anciennement McAfee). Il contient trois scripts Python permettant de traiter des noms de domaines et de les catégoriser automatiquement en utilisant Selenium pour interagir avec un site web externe. Les scripts accomplissent les tâches suivantes :
1. **Découper une liste de domaines** en plusieurs fichiers `txt`.
2. **Utiliser Selenium pour catégoriser les domaines** et sauvegarder les résultats.
3. **Combiner les résultats** et mettre à jour un fichier Excel original avec les nouvelles catégories.

## Prérequis

Assurez-vous que les éléments suivants sont installés sur votre machine :
- Python 3.8 ou plus récent
- `pip` (gestionnaire de packages Python)
- Microsoft Edge et le WebDriver correspondant (msedgedriver)

## Installation

1. Clonez ce dépôt ou téléchargez les fichiers nécessaires.
2. Installez les dépendances Python requises en exécutant :
   ```bash
   pip install pandas selenium openpyxl
   ```

## Configuration

1. Téléchargez le WebDriver pour Microsoft Edge à partir de [ce lien](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/).
2. Décompressez le fichier et placez `msedgedriver.exe` dans un répertoire accessible (par exemple, `C:\WebDriver\`).
3. Assurez-vous que Microsoft Edge est installé sur votre machine.

## Script 1 : Découper les domaines en fichiers `.txt`

### Description

Ce script découpe une liste de domaines en plusieurs fichiers `.txt` contenant chacun un nombre spécifié de domaines.

### Utilisation

1. Placez votre fichier Excel contenant les domaines dans le même répertoire que le script ou ajustez le chemin dans le script.
2. Exécutez le script avec la commande suivante :
   ```bash
   python split_domains.py
   ```

## Script 2 : Utiliser Selenium pour catégoriser les domaines

### Description

Ce script utilise Selenium pour interagir avec un site web et catégoriser les domaines. Les résultats sont sauvegardés dans des fichiers Excel.

### Utilisation

1. Assurez-vous que le WebDriver est installé et accessible.
2. Placez vos fichiers `.txt` de domaines dans le même répertoire que le script ou ajustez le chemin dans le script.
3. Exécutez le script avec la commande suivante :
   ```bash
   python categorize_domains.py
   ```

## Script 3 : Combiner les résultats et mettre à jour le fichier original

### Description

Ce script combine tous les fichiers de résultats générés par le deuxième script, puis met à jour le fichier Excel original avec les nouvelles catégories.

### Utilisation

1. Placez vos fichiers `output_domains_categoriesN.xlsx` dans le même répertoire que le script ou ajustez le modèle de chemin dans le script.
2. Exécutez le script avec la commande suivante :
   ```bash
   python combine_results.py
   ```

### Notes Importantes

- Assurez-vous que tous les fichiers de sortie générés par le deuxième script (`output_domains_categoriesN.xlsx`) sont dans le même répertoire que le script de combinaison.
- Ajustez les chemins des fichiers en fonction de vos besoins.
