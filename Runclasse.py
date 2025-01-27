## ------------------------------------------------------------------------------
# Auteur : Vanessa Monnier
# Date de création : 26 Janvier 2025
# Description : Ce fichier contient des fonctions pour lancer le logiciel
##------------------------------------------------------------------------------


from LectureFichier import LectureFichier
from Modele import Modele
from View import Vue
from View import CarteMondiale
from Controlleur import Controleur
from PyQt5.QtWidgets import QApplication
import sys
from View import fenetre_Skyplot

if __name__ == "__main__":


    # Initialisation des composants
    modele = Modele()
    app = QApplication(sys.argv)

    vue = CarteMondiale
    controleur = Controleur(modele, vue)
    vue.controleur = controleur

    controleur.charger_donnees(
    type_fichier="positions_stations",
    nom_satellite=None,
    jour_debut=None,
    jour_fin=None)

    controleur.afficher_vue_principale()
    sys.exit(app.exec_())

