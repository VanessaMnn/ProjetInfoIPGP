## ------------------------------------------------------------------------------
# Auteur : Vanessa Monnier
# Date de création : 26 Janvier 2025
# Description : Ce fichier contient des fonctions pour gérer les intéractions entre le modèle et la vue
##------------------------------------------------------------------------------



from Modele import Modele
import View
from View import fenetre_Skyplot, Skyplot
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QToolBar, QLabel, QAction, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QCheckBox, QScrollArea, QListWidget, QListWidgetItem, QAbstractItemView, QMenu
import time
import folium
from PyQt5.QtCore import QUrl
import random

class Controleur:

    """
    Classe Contrôleur qui gère la logique de l'application, les interactions entre le modèle et la vue, ainsi que les actions de l'utilisateur.
    """

    def __init__(self, modele, vue):
        self.modele = modele
        self.vue = vue(self)
        self.ajouter_actions()
        self.fenetre_Skyplot = None
        self.skyplot_windows = {}



    def ajouter_actions(self):

        """
        Ajoute des actions à la barre d'outils pour permettre à l'utilisateur d'interagir avec l'application. Les actions incluent la visualisation des données et le redémarrage de l'application.

        Les actions ajoutées comprennent :
        - Action pour ouvrir un Skyplot
        - Action pour afficher les statistiques (non implémentées ici)
        - Sous-menus pour visualiser les stations et satellites dans un Skyplot
        - Action pour redémarrer l'application
        """
        # Action pour Skyplot
        skyplot_action = QAction("Saisie-Utilisateur", self.vue)
        skyplot_action.triggered.connect(self.ouvrir_skyplot)
        self.vue.tool_bar.addAction(skyplot_action)

        # Action pour Statistiques
        statistiques_action = QAction("Statistiques", self.vue)
        statistiques_action.triggered.connect(self.afficher_statistiques)
        self.vue.tool_bar.addAction(statistiques_action)

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
        visualisation_action.setMenu(visualisation_menu)
        visualisation_action.triggered.connect(lambda: None)
        self.vue.tool_bar.addAction(visualisation_action)

        # Ajouter un bouton "Redémarrer"
        restart_action = QAction("Redémarrer", self.vue)
        restart_action.triggered.connect(self.redemarrer_appli)
        self.vue.tool_bar.addAction(restart_action)

    def recuperer_donnees_base(self):
        """
        Récupère les informations de base saisies par l'utilisateur dans la fenêtre Skyplot.

        return: Tuple contenant la date de début, la date de fin et le satellite sélectionné.
        """
        if self.fenetre_Skyplot is None:
            raise RuntimeError("La fenêtre Skyplot n'a pas été initialisée.")

        date_debut = self.fenetre_Skyplot.debut_input.text()
        date_fin = self.fenetre_Skyplot.fin_input.text()
        satellite = self.fenetre_Skyplot.satellite_combo.currentText()
        return date_debut, date_fin, satellite

    def redemarrer_appli(self):

        """
        Redémarre l'application en fermant toutes les fenêtres ouvertes, réinitialisant le modèle
        et réaffichant la vue principale. Utilisé pour réinitialiser l'état de l'application.
        """

        for station, skyplot_window in self.skyplot_windows.items():
            skyplot_window.close()

        # Réinitialiser le modèle et les données
        self.modele.reset()

        # Réinitialiser la fenêtre Skyplot, si elle est ouverte
        if self.fenetre_Skyplot is not None:
            self.fenetre_Skyplot.close()
            self.fenetre_Skyplot = None

        # Relancer l'application en réinitialisant les champs dans la vue
        self.vue.controleur.charger_donnees(
            type_fichier="positions_stations", nom_satellite=None, jour_debut=None, jour_fin=None
        )
        self.afficher_vue_principale()

    def recuperer_stations_selectionnees(self):

        """
        Récupère les stations sélectionnées par l'utilisateur dans la fenêtre Skyplot.

        return: Liste des stations sélectionnées.
        """


        stations_selectionnees = [
            self.fenetre_Skyplot.station_list.item(i).text()
            for i in range(self.fenetre_Skyplot.station_list.count())
            if self.fenetre_Skyplot.station_list.item(i).isSelected()]

        self.vue.mettre_a_jour_couleur_marqueurs(stations_selectionnees)
        return stations_selectionnees

    def ouvrir_skyplot(self, event=None):

        """
        Ouvre la fenêtre Skyplot pour permettre à l'utilisateur de saisir des informations. Si la fenêtre Skyplot n'est pas encore ouverte, elle est initialisée et affichée.
        """

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
        Affiche la visualisation du Skyplot pour les stations.

        Cette fonction appelle la fonction privée visualisation en passant le mode "station".
        """

        self._visualisation(mode="station")

    def visualisation_satellite(self, event=None):

        """
        Affiche la visualisation du Skyplot pour les satellites.

        Cette fonction appelle la fonction privée _visualisation en passant le mode "satellite".
        """

        self._visualisation(mode="satellite")



    def visualisation(self, mode):

        """
        Affiche la visualisation du Skyplot en fonction du mode (station ou satellite). Cette méthode charge les données et génère les visualisations correspondantes.

        param mode: Mode de visualisation, soit "station" soit "satellite"
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



    def charger_donnees(self, type_fichier, nom_satellite, jour_debut, jour_fin):

        """
        Charge les données nécessaires à l'application via le modèle et affiche les stations dans la vue.

        param type_fichier: Type de fichier des données à charger (par exemple, "positions_stations").
        param nom_satellite: Nom du satellite pour lequel les données sont chargées (peut être None).
        param jour_debut: Date de début de la période de données (peut être None).
        param jour_fin: Date de fin de la période de données (peut être None).
        """

        self.modele.charge_donnees(
            type_fichier=type_fichier,
            nom_satellite=nom_satellite,
            jour_debut=jour_debut,
            jour_fin=jour_fin
        )

        if isinstance(self.modele.donnees, bool) and not self.modele.donnees:
            print("Erreur : les données ne sont pas valides.")
        else:
            self.vue.afficher_stations(self.modele.donnees)

    def afficher_vue_principale(self):

        """
        Initialise et affiche la fenêtre principale de l'application, en chargeant les données nécessaires.

        Cette méthode appelle la fonction charger_donnees pour récupérer les données initiales et afficher les stations sur la vue principale.
        """
        self.charger_donnees("positions_stations", None, None, None)
        self.vue.show()

