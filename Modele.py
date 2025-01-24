
from LectureFichier import LectureFichier


class Modele:

    def __init__(self):
        self.donnees = []
        self.lecture_fichier = LectureFichier("C:\\Users\\vmn\\Documents\\ENSG\\2024-2025-PPMD\\ProjetIPGP\\Archive_for_Vanessa")


    def reset(self):
        """Réinitialiser les données du modèle."""
        self.donnees = []



    def charge_donnees(self, type_fichier, nom_satellite, jour_debut, jour_fin, noms_stations=None):

        if type_fichier == "smooth_pos":
            self.donnees = self.lecture_fichier.lire_smooth_pos(nom_satellite, jour_debut, jour_fin)
        elif type_fichier == "final_residual":
            self.donnees = self.lecture_fichier.lire_final_residual(nom_satellite, jour_debut, jour_fin, noms_stations)
        elif type_fichier == "smooth_tdp":
            self.donnees = self.lecture_fichier.lire_fichiers_tdp(nom_satellite, jour_debut, jour_fin)
        elif type_fichier == "positions_stations":
            chemin_fichier = "C:/Users/vmn/Documents/ENSG/2024-2025-PPMD/ProjetIPGP/station_doris/stations_data.txt"  # Remplacer par le vrai chemin
            self.donnees = self.lecture_fichier.lire_position_stations(chemin_fichier)
        else:
            print("Type de fichier non reconnu. Les options valides sont : 'smooth_pos', 'final_residual', 'smooth_tdp'.")

        if not self.donnees.empty:
            print(f"Chargement des données {type_fichier} réussi. Nombre de lignes : {len(self.donnees)}")
        else:
            print("Aucune donnée n'a été chargée.")



    def obtenir_stations_final_residual(self, nom_satellite, jour_debut, jour_fin):
        """
        Récupère les abréviations uniques des stations associées à un satellite
        dans les fichiers finalResiduals.out pour une période donnée.

        Input :
        - nom_satellite : str, Nom du satellite.
        - jour_debut : str, Date de début au format 'YYYY-MM-DD'.
        - jour_fin : str, Date de fin au format 'YYYY-MM-DD'.

        Output :
        - Liste des abréviations uniques des stations.
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


