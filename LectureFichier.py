## ------------------------------------------------------------------------------
# Auteur : Vanessa Monnier
# Date de création : 26 Janvier 2025
# Description : Ce fichier permet de lire le jeu de donnée d'entrée
##------------------------------------------------------------------------------


import pandas as pd
import os



class LectureFichier:
    def __init__(self, chemin_dossier):

        """
        chemin_dossier: str - Chemin vers le dossier contenant les fichiers.
        """

        self.chemin_dossier = chemin_dossier

    def lire_smooth_pos(self, nom_satellite, jour_debut, jour_fin):

        """
        Lecture des fichiers smooth_pos pour un satellite spécifique sur une période donnée.

        Input :
        nom_satellite: str - Nom du satellite (ex. 'CS2')
        jour_debut: str - Date de début au format 'YYYY-MM-DD' (ex. '2024-04-07').
        jour_fin: str - Date de fin au format 'YYYY-MM-DD' (ex. '2024-04-09').

        Output :
        pd.DataFrame - Contient toutes les colonnes souhaitées

        """

        jours = pd.date_range(start=jour_debut, end=jour_fin).strftime('%Y-%m-%d')


        data = []
        for jour in jours:

            nom_fichier = f"smooth_{nom_satellite}_{jour}.POS"
            chemin_fichier = os.path.join(self.chemin_dossier, nom_fichier)


            if not os.path.exists(chemin_fichier):
                print(f"Attention : Fichier {chemin_fichier} introuvable. Ignoré.")
                continue


            with open(chemin_fichier, 'r') as f:
                for ligne in f:

                    if ligne.startswith('E'):

                        colonnes = ligne.split()
                        temps = int(colonnes[2])
                        x = float(colonnes[4])
                        y = float(colonnes[5])
                        z = float(colonnes[6])

                        v_x = float(colonnes[7])
                        v_y = float(colonnes[8])
                        v_z = float(colonnes[9])
                        a_x = float(colonnes[10])
                        a_y = float(colonnes[11])
                        a_z = float(colonnes[12])
                        da_x = float(colonnes[13])
                        da_y = float(colonnes[14])
                        da_z = float(colonnes[15])
                        direction_x = float(colonnes[16])
                        direction_y = float(colonnes[17])
                        direction_z = float(colonnes[18])
                        additional_value = float(colonnes[19])
                        data.append([jour, temps, x, y, z, v_x, v_y, v_z, a_x, a_y, a_z,
                                     da_x, da_y, da_z, direction_x, direction_y, direction_z, additional_value])

        # Convertir en DataFrame pandas
        df = pd.DataFrame(data, columns=['jour', 'temps', 'x', 'y', 'z', 'v_x', 'v_y', 'v_z', 'a_x', 'a_y', 'a_z',
                                         'da_x', 'da_y', 'da_z', 'direction_x', 'direction_y', 'direction_z', 'additional_value'])


        if df.empty:
            print("Aucune donnée n'a été trouvée pour cette période.")
        return df



    def lire_final_residual(self, nom_satellite, jour_debut, jour_fin, noms_stations=None):

        """
        Lecture des fichiers FinalResidual.out pour un satellite donné sur une période définie.

        Input :
        nom_satellite: str - Nom du satellite (ex. 'CS2').
        jour_debut: str - Date de début au format 'YYYY-MM-DD'.
        jour_fin: str - Date de fin au format 'YYYY-MM-DD'.
        noms_stations: list[str] ou None - Liste des noms des stations à inclure (ex. ['ROBC', 'RISC']).
                              Si None, toutes les stations sont incluses.

        Output :
        DataFrame - Contient toutes les colonnes souhaitées.
        """
        # Générer la liste des jours dans la période spécifiée
        jours = pd.date_range(start=jour_debut, end=jour_fin).strftime('%Y-%m-%d')
        print(jours)

        colonnes = [
            'temps', 'satellite_station', 'modele', 'residuel',
            'elevation_sat', 'azimut_sat', 'elevation_station', 'azimut_station'
        ]

        data = []

        for jour in jours:
            nom_fichier = f"finalResiduals_{nom_satellite}_{jour}.OUT"
            chemin_fichier = os.path.join(self.chemin_dossier, nom_fichier)

            if not os.path.exists(chemin_fichier):
                print(f"Fichier {chemin_fichier} introuvable. Ignoré.")
                continue

            # Lecture du fichier ligne par ligne
            with open(chemin_fichier, 'r') as f:
                for ligne in f:
                    parties = ligne.split()


                    if len(parties) == 9 and parties[8] == "DELETED":
                        # Supprimer explicitement cette ligne en passant à la suivante
                        continue

                    if len(parties) < 8:
                        # Ignorez les lignes invalides ou supprimées
                        continue

                    temps = float(parties[0])
                    satellite_station = parties[1].strip('{}')
                    modele = parties[2]
                    residuel = float(parties[3])
                    elevation_sat = float(parties[4])
                    azimut_sat = float(parties[5])
                    elevation_station = float(parties[6])
                    azimut_station = float(parties[7])

                    # Séparez le satellite et la station
                    satellite, station = satellite_station.split('-')
                    satellite = satellite.split('(')[0]
                    station = station.split('(')[0]

                    if satellite != nom_satellite:
                        continue

                    if noms_stations and station not in noms_stations:
                        continue

                    data.append([
                        temps, satellite_station, modele, residuel,
                        elevation_sat, azimut_sat, elevation_station, azimut_station
                    ])

        # Convertir en DataFrame pandas
        df = pd.DataFrame(data, columns=colonnes)

        if df.empty:
            print("Aucune donnée trouvée pour les critères spécifiés.")

        return df

    def lire_fichiers_tdp(self, nom_satellite, jour_debut, jour_fin):
        """
        Lecture des fichiers Smooth.tdp pour un satellite donné sur une période définie.

        Input :
        nom_satellite: str - Nom du satellite (ex. 'CS2').
        jour_debut: str - Date de début au format 'YYYY-MM-DD'.
        jour_fin: str - Date de fin au format 'YYYY-MM-DD'.

        Output :
        DataFrame - Contient les colonnes 'temps', 'apriori', 'valeur_parametre', 'ecart_type', 'nom_parametre',
                    trié par 'nom_parametre'.
        """

        jours = pd.date_range(start=jour_debut, end=jour_fin).strftime('%Y-%m-%d')
        print(jours)

        colonnes = ['temps', 'apriori', 'valeur_parametre', 'ecart_type', 'nom_parametre']

        data = []

        for jour in jours:
            nom_fichier = f"smooth_{nom_satellite}_{jour}.tdp"
            chemin_fichier = os.path.join(self.chemin_dossier, nom_fichier)


            if not os.path.exists(chemin_fichier):
                print(f"Fichier {chemin_fichier} introuvable. Ignoré.")
                continue

            with open(chemin_fichier, 'r') as f:
                for ligne in f:
                    parties = ligne.split()

                    if len(parties) < 5:

                        continue

                    try:
                        temps = float(parties[0])
                        apriori = float(parties[1])
                        valeur_parametre = float(parties[2])
                        ecart_type = float(parties[3])
                        nom_parametre = parties[4]

                        data.append([temps, apriori, valeur_parametre, ecart_type, nom_parametre])
                    except ValueError:

                        continue

        # Convertir en DataFrame pandas
        df = pd.DataFrame(data, columns=colonnes)

        if df.empty:
            print("Aucune donnée trouvée pour les critères spécifiés.")


        return df

    def lire_position_stations(self, chemin_fichier):
        """
        Lecture des positions des stations depuis un fichier txt.

        Input: chemin_fichier
        Output: pd.DataFrame
        """
        colonnes = ['nom_complet', 'longitude', 'latitude', 'abreviation']
        data = []

        with open(chemin_fichier, 'r') as f:
            # Ignorer la première ligne (en-tête)
            next(f)

            # Lire les données ligne par ligne
            for ligne in f:
                # Utiliser split() sans argument pour gérer les espaces multiples
                colonnes_ligne = ligne.split()

                if len(colonnes_ligne) < 4:
                    continue  # Ignorer les lignes mal formatées

                nom_complet = " ".join(colonnes_ligne[:-3])  # Toutes les parties avant les 3 dernières colonnes sont le nom complet
                try:
                    longitude = float(colonnes_ligne[-3])
                    latitude = float(colonnes_ligne[-2])
                except ValueError:
                    print(f"Erreur de conversion pour la ligne: {ligne}")
                    continue  # Ignorer les lignes avec des valeurs incorrectes

                abreviation = colonnes_ligne[-1]

                # Ajouter les données de la ligne au tableau
                data.append([nom_complet, longitude, latitude, abreviation])

        # Convertir en DataFrame pandas
        df = pd.DataFrame(data, columns=colonnes)

        if df.empty:
            print("Aucune donnée valide trouvée dans le fichier.")

        return df







