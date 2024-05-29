# Catégorisation de domaines pour proxy

## Introduction
Ce projet vise à catégoriser les domaines autorisés au niveau d'un proxy en utilisant Skyhigh Security (anciennement McAfee). Le processus implique de diviser une grande liste de domaines en fichiers texte plus petits, de catégoriser chaque domaine, puis de combiner les résultats dans un fichier Excel final.

## Installation

### Prérequis
- Python 3.6 ou supérieur
- Selenium
- pandas
- tqdm
- Navigateur Microsoft Edge
- Edge WebDriver (compatible avec la version installée du navigateur Edge)

### Étapes
1. Clonez le dépôt ou téléchargez les fichiers de script.
2. Installez les paquets Python requis :
    ```sh
    pip install selenium pandas tqdm openpyxl
    ```
3. Téléchargez la version appropriée de Edge WebDriver [ici](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) et placez-le dans un répertoire connu.

## Utilisation

### Script 1 : Diviser les Domaines en Fichiers txt
Ce script lit une grande liste de domaines à partir d'un fichier Excel et les divise en fichiers texte plus petits, chacun contenant un nombre spécifié maximal de domaines.

- **Fichier :** `split1.py`
- **Entrée :** Fichier Excel avec les domaines dans la colonne 'domain' de la feuille 'SGT'.
- **Sortie :** Plusieurs fichiers texte contenant chacun jusqu'à 1000 domaines (customisable).

**Comment l'exécuter :**
```sh
python split1.py
```

**Fichiers requis :**
- Un fichier Excel (`path_to_excel_file`) avec les domaines dans la colonne 'domain' de la feuille 'SGT'.

**Fichiers générés :**
- Plusieurs fichiers texte (`domains_x.txt`) contenant chacun jusqu'à 1000 domaines.

### Script 2 : Catégoriser les Domaines
Ce script utilise Selenium pour automatiser le processus de vérification de la catégorisation de chaque domaine sur le site TrustedSource. Il enregistre les résultats de la catégorisation dans un fichier Excel.

- **Fichier :** `categorize2.py`
- **Entrée :** Un fichier texte contenant des domaines + le reste de la config.
- **Sortie :** Un fichier Excel avec les résultats de la catégorisation.

**Comment l'exécuter :**
1. Mettez à jour les variables `input_file` et `output_file` dans le script avec les chemins corrects.
2. Exécutez le script :
    ```sh
    python categorize2.py
    ```

**Fichiers requis :**
- Un fichier texte (`domains_x.txt`) contenant des domaines.

**Fichiers générés :**
- Un fichier Excel (`output_domains_categories.xlsx`) avec les résultats de la catégorisation.

### Script 3 : Combiner les Résultats avec les Données Originales
Ce script combine les résultats de la catégorisation avec le fichier Excel original, en mettant à jour la colonne 'Categorie' dans la feuille 'SGT'.

- **Fichier :** `combine3.py`
- **Entrée :** Fichier Excel original et plusieurs fichiers de résultats de catégorisation.
- **Sortie :** Un fichier Excel final mis à jour.

**Comment l'exécuter :**
1. Assurez-vous que tous les fichiers de résultats de catégorisation sont dans le même répertoire.
2. Mettez à jour les chemins dans le script si nécessaire.
3. Exécutez le script :
    ```sh
    python combine3.py
    ```

**Fichiers requis :**
- Le fichier Excel original (`path_to_original_file.xlsx`).
- Plusieurs fichiers Excel de résultats de catégorisation (`output_domains_categories_x.xlsx`).

**Fichiers générés :**
- Un fichier Excel final mis à jour (`final_updated_file.xlsx`).

## Explications Détaillées des Scripts

### split1.py
1. Lit le fichier Excel original (`path_to_excel_file`) et extrait la colonne 'domain' de la feuille 'SGT'.
2. Trie les domaines par ordre alphabétique et les divise en fichiers texte plus petits, chacun contenant jusqu'à 1000 domaines.
3. Produit les fichiers texte dans le répertoire spécifié (`output_directory`).

### categorize2.py
1. Lit les domaines à partir du fichier texte spécifié (`input_file`).
2. Utilise Selenium pour naviguer sur le site TrustedSource et vérifier la catégorisation de chaque domaine.
3. Gère les éventuels timeouts et réessaie jusqu'à 3 fois par domaine.
4. Produit les résultats de la catégorisation dans un fichier Excel (`output_file`).

### combine3.py
1. Lit le fichier Excel original et les fichiers de résultats de catégorisation.
2. Combine les résultats en faisant correspondre les domaines et met à jour la colonne 'Categorie' dans la feuille 'SGT'.
3. Ajoute une colonne 'Status-Valid' dans la feuille GTS.
3. Produit un fichier Excel final mis à jour (`final_updated_file.xlsx`).

## Notes
- Assurez-vous que la version de Edge WebDriver correspond à la version installée du navigateur Edge.
- Ajustez les temps de pause dans `categorize2.py` si nécessaire pour éviter d'être bloqué par le site TrustedSource.
- Si probleme de ufc-8, le rajouter ou l'enlever.