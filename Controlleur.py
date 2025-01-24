from Modele import Modele
import View
from View import fenetre_Skyplot, Skyplot
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QToolBar, QLabel, QAction, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QCheckBox, QScrollArea, QListWidget, QListWidgetItem, QAbstractItemView, QMenu
import time
import folium
from PyQt5.QtCore import QUrl
import random

class Controleur:
    def __init__(self, modele, vue):
        self.modele = modele
        self.vue = vue(self)
        self.ajouter_actions()
        self.fenetre_Skyplot = None
        self.skyplot_windows = {}



    def ajouter_actions(self):
        """Ajoute des actions à la barre d'outils."""
        # Action pour Skyplot
        skyplot_action = QAction("Skyplot", self.vue)
        skyplot_action.triggered.connect(self.ouvrir_skyplot)
        self.vue.tool_bar.addAction(skyplot_action)

        # Action pour Statistiques
        statistiques_action = QAction("Statistiques", self.vue)
        statistiques_action.triggered.connect(self.afficher_statistiques)
        self.vue.tool_bar.addAction(statistiques_action)

        # Ajouter un bouton "Redémarrer"
        restart_action = QAction("ReInitialiser", self.vue)
        restart_action.triggered.connect(self.redemarrer_appli)
        self.vue.tool_bar.addAction(restart_action)

        # Menu pour Visualisation
        visualisation_menu = QMenu("Visualisation", self.vue)

        # Sous-menu Skyplot - Station
        skyplot_station_action = QAction("Skyplot - Station", self.vue)
        skyplot_station_action.triggered.connect(lambda: self.visualisation(mode="station"))
        visualisation_menu.addAction(skyplot_station_action)

        # Sous-menu Skyplot - Satellite
        skyplot_satellite_action = QAction("Skyplot - Satellite", self.vue)
        skyplot_satellite_action.triggered.connect(lambda: self.visualisation(mode="satellite"))
        visualisation_menu.addAction(skyplot_satellite_action)

        # Créer une action pour afficher le menu dans la barre d'outils
        visualisation_action = QAction("Visualisation", self.vue)
        visualisation_action.setMenu(visualisation_menu)  # Associer le menu déroulant
        visualisation_action.triggered.connect(lambda: None)  # Prévenir l'action par défaut

        # Ajouter un bouton dans la barre d'outils pour afficher le menu
        self.vue.tool_bar.addAction(visualisation_action)

    def recuperer_donnees_base(self):
        """Récupère les informations de base saisies par l'utilisateur."""
        if self.fenetre_Skyplot is None:
            raise RuntimeError("La fenêtre Skyplot n'a pas été initialisée.")

        date_debut = self.fenetre_Skyplot.debut_input.text()
        date_fin = self.fenetre_Skyplot.fin_input.text()
        satellite = self.fenetre_Skyplot.satellite_combo.currentText()
        return date_debut, date_fin, satellite

    def redemarrer_appli(self):
        """Réinitialise l'état de l'application et relance la vue principale."""
        # Réinitialiser les données du modèle
        self.modele.reset()

        # Réinitialiser l'interface utilisateur (réinitialiser tous les champs)
        self.vue.reset()

        # Relancer la vue principale
        self.afficher_vue_principale()

    def recuperer_stations_selectionnees(self):
        """Récupère les stations sélectionnées par l'utilisateur."""
        stations_selectionnees = [
            self.fenetre_Skyplot.station_list.item(i).text()
            for i in range(self.fenetre_Skyplot.station_list.count())
            if self.fenetre_Skyplot.station_list.item(i).isSelected()]

        self.vue.mettre_a_jour_couleur_marqueurs(stations_selectionnees)
        return stations_selectionnees

    def ouvrir_skyplot(self, event=None):
        """
        Ouvre la fenêtre Skyplot pour rentrer les informations"
        """
        print("Skyplot ouvert")
        if self.fenetre_Skyplot is None:
            self.fenetre_Skyplot = fenetre_Skyplot(self.modele)

        self.fenetre_Skyplot.show()


    def afficher_statistiques(self, event= None):
        """
        Affiche les statistiques (actuellement non implémentées).
        """
        self.vue.afficher_statistiques()


    def visualisation_station(self, event=None):
        """
        Affiche la visualisation du skyplot pour les stations.
        """
        self._visualisation(mode="station")

    def visualisation_satellite(self, event=None):
        """
        Affiche la visualisation du skyplot pour les satellites.
        """
        self._visualisation(mode="satellite")



    def visualisation(self, mode):
        """
        Affiche la visualisation du skyplot.
        """

        date_debut, date_fin, satellite = self.recuperer_donnees_base()

        stations_selectionnees = self.recuperer_stations_selectionnees()


        self.modele.charge_donnees(
        type_fichier="final_residual",
        nom_satellite=satellite,
        jour_debut=date_debut,
        jour_fin=date_fin,
        noms_stations=stations_selectionnees,
    )

        # Parcourir chaque station sélectionnée
        for station in stations_selectionnees:
            if 'station_abreviation' not in self.modele.donnees.columns:
                self.modele.donnees['station_abreviation'] = self.modele.donnees['satellite_station'].str.extract(r'-([A-Z]+)\(')[0]

            # Filtrer les données pour la station sélectionnée
            donnees_station = self.modele.donnees[
            self.modele.donnees['station_abreviation'] == station]

            if donnees_station.empty:
                print(f"Aucune donnée trouvée pour la station '{station}' dans 'station_abreviation")
                continue

            # Extraire les colonnes nécessaires
            azimut = donnees_station["azimut_station" if mode == "station" else "azimut_sat"]
            elevation = donnees_station["elevation_station" if mode == "station" else "elevation_sat"]
            residus = donnees_station["residuel"] if "residuel" in donnees_station.columns else None


            couleur_station = self.vue.markers[station].get("couleur")  # Par défaut bleu
            print(f"Station: {station}, Couleur utilisée pour le Skyplot: {couleur_station}")


            # Créer et afficher un skyplot pour cette station
            skyplot_window = Skyplot(
                date_debut=date_debut,
                date_fin=date_fin,
                satellite=satellite,
                stations_selectionnees=[station],
                azimut=azimut,
                elevation=elevation,
                residus=residus,
                couleur=couleur_station

            )
            self.skyplot_windows[station] = skyplot_window
            skyplot_window.afficher()

#['ADHC', 'AMVB', 'ASEB', 'BEMB', 'BETB', 'CIDB', 'COBB', 'CRRC', 'DIOB', 'DJIB', 'EVEB', 'GAVC', 'GONC', 'GR4B', 'GRFB', 'HBMB', 'HEMB', 'HROC', 'JIWC', 'KEYC', 'KIVC', 'KOLB', 'KRWB', 'LAOB', 'LICB', 'MAIB', 'MALC', 'MANB', 'MAVC', 'MEUB', 'MIAB', 'MLAC', 'MNAC', 'MSPB', 'NOXC', 'OWFC', 'PAUB', 'PDOC', 'REVC', 'RIMC', 'RISC', 'ROBC', 'SARC', 'SCSC', 'SJVC', 'SOFC', 'STKC', 'SVBC', 'TLSB', 'TRJB', 'YASB', 'YEMB']

    def charger_donnees(self, type_fichier, nom_satellite, jour_debut, jour_fin):
        """
        Charge les données via le modèle.
        """
        self.modele.charge_donnees(
            type_fichier=type_fichier,
            nom_satellite=nom_satellite,
            jour_debut=jour_debut,
            jour_fin=jour_fin
        )
        print("Données chargées :", self.modele.donnees)
        if isinstance(self.modele.donnees, bool) and not self.modele.donnees:
            print("Erreur : les données ne sont pas valides.")
        else:
            self.vue.afficher_stations(self.modele.donnees)

    def afficher_vue_principale(self):
        """
        Initialise et affiche la fenêtre principale de l'application.
        """
        self.charger_donnees("positions_stations", None, None, None)
        self.vue.show()

