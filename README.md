# Visualisation des résidus de traitement des mesures DORIS

## Description du projet

Ce projet consiste à développer un logiciel de visualisation des résidus de traitement des mesures DORIS et des produits associés (résidus d’observation, paramètres orbitaux) fournis par l'International Doris Service (IDS). L'objectif de cet outil est qu'il soit utilisé et que son développement soit poursuivi par le centre d'analyse **IGN/IPGP/JPL**.

Le logiciel utilise une architecture **MVC** (Modèle, Vue, Contrôleur) et implémente divers design patterns tels que **Strategy**, **Factory**, et **Observer**. Cette architecture a pour but de rendre le projet accessible et facile à prendre en main, afin de permettre à un futur étudiant de continuer le développement de l'outil sans difficulté.

## Installation

### Prérequis

Pour faire fonctionner ce projet en local, tu auras besoin des librairies suivantes :

- **PyQt5** : Pour l'interface graphique.
- **PyQtWebEngine** : Pour intégrer des fonctionnalités Web dans l'interface graphique.
- **Folium** : Pour la visualisation des cartes interactives.

### Cloner le projet

Tu peux cloner ce projet en utilisant `git` :

```bash
git clone https://github.com/ton-utilisateur/nom-du-projet.git
cd nom-du-projet
```

### Installation des dépendances

```bash
pip install PyQt5
pip install PyQtWebEngine
pip install folium
```

## Usage

Une fois les dépendances installées, tu peux démarrer l'application avec la commande suivante :

```bash
python Runclasse.py
```

## Auteur

Développé par Vanessa Monnier  
Date de début du projet : novembre 2024

```

### Vérification rapide :
1. **Vérifie les liens** comme ceux vers le fichier `LICENSE` (assure-toi que ce fichier existe dans ton projet si tu mentionnes cela).
2. **Mets à jour** ton propre nom et d'autres détails personnalisés.

Une fois que tu as copié ce texte dans ton fichier `README.md` sur GitHub, tu verras que la syntaxe est bien prise en charge et le fichier sera lisible et bien formaté.
