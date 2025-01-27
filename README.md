# Visualisation des résidus de traitement des mesures DORIS

## Description du projet

Ce projet consiste à développer un logiciel de visualisation des résidus de traitement des mesures DORIS et des produits associés (résidus d’observation, paramètres orbitaux) fournis par l'International Doris Service (IDS). L'objectif de cet outil est qu'il soit utilisé et que son développement soit poursuivi par le centre d'analyse **IGN/IPGP/JPL**.

Le logiciel utilise une architecture **MVC** (Modèle, Vue, Contrôleur) et implémente divers design patterns tels que **Strategy**, **Factory**, et **Observer**. Cette architecture a pour but de rendre le projet accessible et facile à prendre en main, afin de permettre à un futur étudiant de continuer le développement de l'outil sans difficulté.

## Description des fichiers présents dans le dépot Git

- **"Controlleur.py", "Modele.py", "View.py"** : Ce sont les trois fichiers de l'architecture MVC qui constitue le corps de l'architecture du code.
- **"Runclasse.py"** : Fichier qu'il faut exécuter pour le lancement du logiciel.
- **"index.html"** : Documentation complète de tous les fichiers python réalisée avec la librairie **pdoc**.
- **"Documentation_développeur.ipynb"** et **"Documentation_utilisateur.ipynb"** : JupyterNotebook créant une documentation pour le développeur en décrivant certaines fonctions pour observer précisément leur sortie, et une documentation utilisateur pour lui indiquer comment installer et mettre en marche le projet. Ces deux fichiers se répètent avec le fichier **index.html** et **readme** mais sont une demande spécifique des commanditaires.

## Installation

### Prérequis

Pour faire fonctionner ce projet en local, vous aurez besoin des librairies suivantes :

- **PyQt5** : Pour l'interface graphique.
- **PyQtWebEngine** : Pour intégrer des fonctionnalités Web dans l'interface graphique.
- **Folium** : Pour la visualisation des cartes interactives.

### Cloner le projet

Vous pouvez cloner ce projet en utilisant `git` :

```bash
git clone https://github.com/ton-utilisateur/nom-du-projet.git](https://github.com/VanessaMnn/ProjetInfoIPGP.git
cd nom-du-projet
```

### Installation des dépendances

```bash
pip install PyQt5
pip install PyQtWebEngine
pip install folium
```

## Usage

Une fois les dépendances installées, vous pouvez démarrer l'application avec la commande suivante :

```bash
python Runclasse.py
```

## Auteur

Développé par Vanessa Monnier  
Date de début du projet : novembre 2024
