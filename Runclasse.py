from LectureFichier import LectureFichier
from Modele import Modele
from View import Vue
from View import CarteMondiale
from Controlleur import Controleur
from PyQt5.QtWidgets import QApplication
import sys
from View import fenetre_Skyplot

if __name__ == "__main__":

    ##---------Initialiser la classe-------------

    lecteur = LectureFichier("C:\\Users\\vmn\\Documents\\ENSG\\2024-2025-PPMD\\ProjetIPGP\\Archive_for_Vanessa")
    """
    ##--------Lecture smooth.pos----------------------

    nom_satellite = "JA3"
    jour_debut = "2024-04-07"
    jour_fin = "2024-04-09"
    resultats = lecteur.lire_smooth_pos(nom_satellite, jour_debut, jour_fin)


    # Sélectionner uniquement les colonnes 'jour', 'temps', 'x', 'y' et 'z'
    colonnes_positions = ['jour', 'temps', 'x', 'y', 'z']
    resultats_filtres = resultats[colonnes_positions]

    print(resultats_filtres)


    ## --------Lecture FinalResidual.out-------------
    """
    """
    final_residual_data = lecteur.lire_final_residual(nom_satellite='CS2', jour_debut='2024-04-07', jour_fin='2024-04-08', noms_stations=['SJVC'])

    print(final_residual_data)

    """
    """
    ##---------Lecture smooth.tdp--------------------

    smooth_tdp = lecteur.lire_fichiers_tdp("CS2", "2024-04-07", "2024-04-07")
    print(smooth_tdp)
    colonne_apriori = ['apriori']
    filtre = smooth_tdp[colonne_apriori]
    print(filtre)

    """
    ##-------Lecture station_data.txt------------
    """
    chemin_dossier = 'C:/Users/vmn/Documents/ENSG/2024-2025-PPMD/ProjetIPGP/station_doris/'

    lecture_fichier = LectureFichier(chemin_dossier)

    df_stations = lecture_fichier.lire_position_stations('stations_data.txt')

    print(df_stations)
    """
    ##---------Lien entre Model - Vue - Controlleur

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

    """
    stations = modele.obtenir_stations_final_residual("S3B", "2024-04-07", "2024-04-09")
    print(stations, len(stations))
    """

    ##----------Execution de la fenêtre PyQt5 : afficher CarteMondiale

    controleur.afficher_vue_principale()

    sys.exit(app.exec_())

