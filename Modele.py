## ------------------------------------------------------------------------------
# Auteur : Vanessa Monnier
# Date de création : 26 Janvier 2025
# Description : Ce fichier contient des fonctions pour récupérer et traiter les données de plusieurs fichiers DORIS.
##------------------------------------------------------------------------------


from LectureFichier import LectureFichier
from pathlib import Path

class Modele:

    """
    Classe représentant le modèle de données dans l'application. Elle gère le chargement des données depuis différents types de fichiers, ainsi que la réinitialisation et la récupération d'informations spécifiques.
    """

    def __init__(self):

        """
        Initialise l'objet `Modele`. Définit le répertoire courant et initialise l'objet de lecture des fichiers.
        """

        self.current_dir = Path(__file__).parent
        self.donnees = []
        chemin_donnees = self.current_dir / "BDD"
        self.lecture_fichier = LectureFichier(chemin_donnees)


    def reset(self):

        """Réinitialiser les données du modèle. Vide la liste des données chargées."""

        self.donnees = []



    def charge_donnees(self, type_fichier, nom_satellite, jour_debut, jour_fin, noms_stations=None):

        """
        Charge les données en fonction du type de fichier et des paramètres donnés (satellite, période, stations).

        :param type_fichier: str, Le type de fichier à charger. Options disponibles : "smooth_pos", "final_residual", "smooth_tdp", "positions_stations".
        :param nom_satellite: str, Le nom du satellite pour lequel les données sont chargées.
        :param jour_debut: str, La date de début sous le format 'YYYY-MM-DD'.
        :param jour_fin: str, La date de fin sous le format 'YYYY-MM-DD'.
        :param noms_stations: list, Liste des stations (optionnel) utilisée pour charger des données spécifiques.
        """


        if type_fichier == "smooth_pos":
            self.donnees = self.lecture_fichier.lire_smooth_pos(nom_satellite, jour_debut, jour_fin)
        elif type_fichier == "final_residual":
            self.donnees = self.lecture_fichier.lire_final_residual(nom_satellite, jour_debut, jour_fin, noms_stations)
        elif type_fichier == "smooth_tdp":
            self.donnees = self.lecture_fichier.lire_fichiers_tdp(nom_satellite, jour_debut, jour_fin)
        elif type_fichier == "positions_stations":
            chemin_fichier = self.current_dir / "stations_data.txt"
            self.donnees = self.lecture_fichier.lire_position_stations(chemin_fichier)
        else:
            print("Type de fichier non reconnu. Les options valides sont : 'smooth_pos', 'final_residual', 'smooth_tdp'.")

        if not self.donnees.empty:
            print(f"Chargement des données {type_fichier} réussi. Nombre de lignes : {len(self.donnees)}")
        else:
            print("Aucune donnée n'a été chargée.")



    def obtenir_stations_final_residual(self, nom_satellite, jour_debut, jour_fin):
        """
        Récupère les abréviations uniques des stations associées à un satellite dans les fichiers finalResiduals.out pour une période donnée.

        :param nom_satellite: str, Nom du satellite.
        :param jour_debut: str, Date de début sous le format 'YYYY-MM-DD'.
        :param jour_fin: str, Date de fin sous le format 'YYYY-MM-DD'.

        :return: list, Liste des abréviations uniques des stations (sous forme triée).
        """
        donnees = self.lecture_fichier.lire_final_residual(nom_satellite, jour_debut, jour_fin)
        if donnees.empty:
            print("Aucune donnée n'a été trouvée.")
            return []

        # Extraire la colonne contenant les stations
        stations = donnees['satellite_station'].apply(lambda x: x.split('-')[1].split('(')[0])
        # Renvoyer les abréviations uniques triées
        stations_uniques = sorted(set(stations))

        return stations_uniques


