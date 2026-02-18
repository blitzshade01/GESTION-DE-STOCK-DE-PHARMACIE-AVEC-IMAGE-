# GESTION-DE-STOCK-DE-PHARMACIE-AVEC-IMAGE-
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, date
import threading
import time 

class GestionPharmacie:
    def __init__(self, root):
        self.root = root
        self. root.title("Gestion de Stock - Pharmacie")
        self. root.geometry("800x600")
        self. root.resizable(True, True)

        #Connexion à la base de données
        self.conn = sqlite3.connect("pharmacie.db")
        self.create_table()

        #Variables
        self.seuil_alerte = 10 # seuil pour alerte stock faible

        #Creation de l'interface 
        self.setup_ui()

        #Chargement des données 
        self.refresh_stock()

        # Démarrer la véeification automatique 
        self.check_alerts()

    def create_tabe(self):
        """Creation de la table des medicaments"""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medicaments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                quantite INTEGER NOT NULL,
                date_expiration TEXT NOT NULL
                       
            )
        """)
        self.conn.commit()
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""

        #Style
        style = ttk.Style()
        style.theme_user('clam')

        #Couleurs
        self.bg_color = "#f0f0f0"
        self.header_color = '#2c3e50'
        self.button_color = '#3498db'
        self.alert_color = '#e74c3c'

        self.root.configure(bg=self.bg_color)

        #titre principale 
        title_frame = tk.Frame(self.root, bg=self.header_color)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text="Gestion de Stock Pharmacie",
            font=('Ariel' 20, 'bold')
            fg='white',
            bg=self.header_color
        )
        title_label.pack(expand=True)

        #Frame principale avec onglets
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        #Onglets 2:Stock actuel
        self.tab_stock = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_stock, text="Stock actuel")
        self.setup_tab_Stock()

        #Onglets 3: Entrées/sorties
        self.tab_mouvements = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_mouvements, text="Mouvements")
        self.setup_tab_mouvements()

        #Onglets 4: Alertes
        self.tab_alertes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_alertes, text="Alertes")
        self.setup_alertes()

        # Barre de statut
        self.status_bar = tk.Label(
            self.root,
            text="Pret",
            bd=1
            relief=tk.SUNKEN
            anchor=tk.w
        )
        self.status_bar.pack(side=tk.BOTTOM, fill='x')
    
    def setup_tab_ajout(self)
        """Configuration de l'onglet d'ajoute"""
        # Frame pour le formule 
        form_frame = ttk.LabelFrame(self.tab_ajout, text="Nouveau medicament", padding=10)
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Nom


