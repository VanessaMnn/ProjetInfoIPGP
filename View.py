from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QToolBar, QLabel, QAction, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QCheckBox, QScrollArea, QListWidget, QListWidgetItem, QAbstractItemView, QMessageBox, QFileDialog, QDesktopWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium
from PyQt5.QtCore import QUrl, pyqtSignal, QPoint, Qt
import os
from PyQt5 import QtCore

from PyQt5.QtCore import Qt, QObject
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from gnss_lib_py.navdata.navdata import NavData
from gnss_lib_py.visualizations.plot_skyplot import plot_skyplot

import numpy as np
import matplotlib.pyplot as plt
import random

# Classe abstraite Vue
class Vue(ABC):

    @abstractmethod
    def afficher_donnees(self, donnees):
        """ Affiche les données chargées. """
        pass


    @abstractmethod
    def afficher_details_station(self):
        """ Méthode pour afficher les détails d'une station """
        pass

    @abstractmethod
    def afficher_stations(self):
        """ Méthode pour afficher les stations sur la carte """
        pass




class fenetre_Skyplot(QWidget):

    stations_selectionnees_signal = pyqtSignal(dict)
    def __init__(self, modele):
        super().__init__()
        self.modele = modele
        self.setWindowTitle("Skyplot")
        self.setGeometry(200, 200, 400, 300)

        #Contenu de la fenêtre skyplot

        layout = QVBoxLayout()
        # Champ pour la date de début
        self.debut_label = QLabel("Date de début (YYYY-MM-DD):")
        self.debut_input = QLineEdit()
        layout.addWidget(self.debut_label)
        layout.addWidget(self.debut_input)

        # Champ pour la date de fin
        self.fin_label = QLabel("Date de fin (YYYY-MM-DD):")
        self.fin_input = QLineEdit()
        layout.addWidget(self.fin_label)
        layout.addWidget(self.fin_input)

        # Sélection du satellite
        self.satellite_label = QLabel("Satellite sélectionné:")
        self.satellite_combo = QComboBox()
        self.satellite_combo.addItems(["CS2", "JA3", "S3A", "S3B", "S6A", "SRL"])
        layout.addWidget(self.satellite_label)
        layout.addWidget(self.satellite_combo)

        # Bouton pour charger les stations
        self.charger_stations_button = QPushButton("Charger stations")
        self.charger_stations_button.clicked.connect(self.charger_stations)
        layout.addWidget(self.charger_stations_button)

        # Sélection des stations au sol
        self.station_label = QLabel("Stations au sol sélectionnées:")
        self.station_list = QListWidget()
        self.station_list.setSelectionMode(QAbstractItemView.MultiSelection)                        # Permet de sélectionner plusieurs éléments

        layout.addWidget(self.station_label)
        layout.addWidget(self.station_list)

        # Bouton pour valider
        self.valider_btn = QPushButton("Valider")
        self.valider_btn.clicked.connect(self.valider)
        layout.addWidget(self.valider_btn)

        self.setLayout(layout)


    def charger_stations(self):

        """Filtre les stations selon les informations saisies."""
        date_debut = self.debut_input.text()
        date_fin = self.fin_input.text()
        satellite = self.satellite_combo.currentText()

        if not (date_debut and date_fin and satellite):
            QMessageBox.warning(self, "Erreur", "Veuillez remplir toutes les informations avant de continuer.")
            return

        stations = self.modele.obtenir_stations_final_residual(satellite, date_debut, date_fin)
        print("voici les stations", stations)
        if not stations:
            QMessageBox.information(self, "Aucune station", "Aucune station trouvée pour les critères spécifiés.")
            return

        self.station_list.clear()
        for station in stations:
            self.station_list.addItem(QListWidgetItem(station))


    def valider(self):
        """Ferme la fenêtre après validation."""

        self.close()

class Skyplot(QWidget):


    def __init__(self, date_debut, date_fin, satellite, stations_selectionnees, azimut, elevation, residus, couleur):
        super().__init__()
        self.setWindowTitle(f"Skyplot pour {satellite}")
        self.setGeometry(200, 200, 800, 600)

        self.date_debut = date_debut
        self.date_fin = date_fin
        self.satellite = satellite
        self.stations_selectionnees = stations_selectionnees
        self.azimut = azimut
        self.elevation = elevation
        self.residus = residus
        self.couleur = couleur

        # Style de la fenêtre basé sur la couleur
        self.setStyleSheet(f"""
        QWidget {{
            border: 5px solid {self.couleur};
            background-color: white;
        }}
    """)

        # Initialiser le graphique
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Disposition verticale
        layout = QVBoxLayout()

        # Ajouter le canvas pour le graphique
        layout.addWidget(self.canvas)

        # Appliquer le layout au widget principal
        self.setLayout(layout)

        # Tracer le Skyplot
        self.tracer_skyplot()

        # Ajouter le bouton "Sauvegarder"
        self.save_button = QPushButton("Sauvegarder le Skyplot")
        self.save_button.clicked.connect(self.sauvegarder_skyplot)
        layout.addWidget(self.save_button)

    def sauvegarder_skyplot(self):
        """
        Sauvegarde le Skyplot en tant qu'image sur le disque.
        """
        # Ouvrir une boîte de dialogue pour choisir l'emplacement du fichier
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Sauvegarder le Skyplot",
            "",
            "Images PNG (*.png);;Tous les fichiers (*)",
            options=options
        )

        if file_path:
            # Sauvegarder le graphique (à adapter selon la bibliothèque utilisée)
            # Exemple avec Matplotlib :
            self.canvas.print_figure(file_path, dpi=300)
            print(f"Skyplot sauvegardé dans {file_path}")

    def tracer_skyplot(self):

        """Trace le graphique du skyplot."""

        #Explication : c'est skyplot avec satellite fixe, qui regarde la station au sol que je souhaite visualiser, celui que j'avais au début c'était skyplot de la station fixe avec le satellite qui bouge au dessus


        if self.azimut.empty or self.elevation.empty or self.residus.empty:
            print("Erreur : Les données d'azimut, d'élévation ou de résidus sont vides.")
            return

        print("azimut", self.azimut)
        print("elevation", self.elevation)


        # Convertir les angles en radians
        elevation_rad = np.deg2rad(self.elevation)
        azimut_rad = np.deg2rad(self.azimut)

        print("Longueur Azimut :", len(azimut_rad))
        print("Longueur Élévation :", len(elevation_rad))


        ax = self.figure.add_subplot(111, projection='polar')
        sc = ax.scatter(azimut_rad, 90 - self.elevation, c=self.residus, cmap='viridis', s=50)

        # Ajouter une barre de couleur
        cbar = plt.colorbar(sc)
        cbar.set_label('Residus')


        # Définir le titre et autres propriétés du graphique
        ax.set_title(f"Skyplot pour {self.satellite} et {self.stations_selectionnees} ({self.date_debut} à {self.date_fin})")
        ax.set_ylim(0, 90)
        ax.set_yticks([0, 30, 60, 90])
        ax.set_yticklabels(['90°', '60°', '30°', '0°'])
        ax.set_xticks(np.deg2rad(np.arange(0, 360, 30)))
        ax.set_xticklabels(['N', '30°', '60°', 'E', '120°', '150°', 'S',
        '210°', '240°', 'W', '300°', '330°'])
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)

        self.canvas.draw()






    def afficher(self):
        """Affiche la fenêtre Skyplot."""
        self.show()

# Classe CarteMondiale qui hérite de QWidget

class CarteMondiale(QMainWindow):

    def __init__(self, controleur=None):
        super().__init__()
        self.setWindowTitle("Logiciel de visualisation - Centre d'analyse IGN/IPGP/JPL de l'International Doris Service")

        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()

        self.setGeometry(0, 0, screen_width, screen_height)


        self.controleur = controleur
        # Créer une carte Folium
        self.m = folium.Map(location=[0, 0], zoom_start=2)
        self.carte_path = os.path.join(os.getcwd(), "carte_interactive.html")
        self.m.save(self.carte_path)

        # Vue de la carte
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl.fromLocalFile(self.carte_path))

        #Widget central
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setLayout(layout)

        # Barre d'outil
        self.tool_bar = QToolBar("Fonctionnalités", self)
        self.addToolBar(self.tool_bar)




    def afficher_donnees(self, donnees):
        """ Afficher les données sur la carte. """
        self.afficher_stations(donnees)
        self.browser.setUrl(QUrl.fromLocalFile(self.carte_path))
        self.show()

    def afficher_statistiques(self):
        """Affiche la fenêtre Statistiques (à implémenter)."""
        print("Statistiques en cours de développement.")



    def afficher_stations(self, stations_df):
        """Affiche les stations sur la carte en utilisant Folium"""
        self.m = folium.Map(location=[0, 0], zoom_start=2)  # Réinitialise la carte


        self.markers = {}

        for _, station in stations_df.iterrows():
            lat, lon = station['latitude'], station['longitude']
            station_name = station['abreviation']
            popup_content = f"""
            <div style="border: 1px solid black; padding: 10px; border-radius: 5px;">
                <b style="color: darkblue;">Station:</b> {station['nom_complet']}<br>
                <b style="color: darkblue;">Abreviation:</b> {station['abreviation']}<br>
                <b style="color: darkblue;">Longitude:</b> {lon}<br>
                <b style="color: darkblue;">Latitude:</b> {lat}
            </div>
            """
            marker = folium.Marker(
                [lat, lon],
                popup=folium.Popup(popup_content, max_width=300),
                icon=folium.Icon(color="blue"))

            marker.add_to(self.m)

            self.markers[station_name] = {
                "marker": marker,
                "latitude": lat,
                "longitude": lon,
                "popup_content": popup_content }

        self.m.save(self.carte_path)
        self.browser.setUrl(QUrl.fromLocalFile(self.carte_path))

    def generer_couleur(self):
        # Génère une couleur aléatoire en hexadécimal
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    def mettre_a_jour_couleur_marqueurs(self, stations_selectionnees):

        """Met à jour la couleur des marqueurs en fonction des stations sélectionnées."""

        self.m = folium.Map(location=[0, 0], zoom_start=2)

        couleur_par_station = {station: self.generer_couleur() for station in stations_selectionnees}


        for station, info in self.markers.items():

            couleur = couleur_par_station.get(station, "#3388FF")
            #là je change les marqueurs pour des cercles, car les marqueurs ne sont pas compatibles avec des valeurs hexadécimales. ça change simplement le visuel, rien d'autres
            folium.CircleMarker(
                location=[info["latitude"], info["longitude"]],
                radius=8,  # Taille du marqueur
                color=couleur,  # Bordure du marqueur
                fill=True,
                fill_color=couleur,  # Remplissage
                fill_opacity=0.8,
                popup=folium.Popup(info["popup_content"], max_width=300)
            ).add_to(self.m)

            if station in couleur_par_station:
                self.markers[station]["couleur"] = couleur

        # Sauvegarder la carte et la mettre à jour dans l'interface
        self.m.save(self.carte_path)
        self.browser.setUrl(QUrl.fromLocalFile(self.carte_path))




    @property
    def controleur(self):
        return self._controleur

    @controleur.setter
    def controleur(self, value):
        self._controleur = value



