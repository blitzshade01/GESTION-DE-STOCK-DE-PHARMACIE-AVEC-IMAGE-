import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
from datetime import datetime, date 
import threading
import time

class GestionPharmacie:
    def _init_(self, root):
        self.root = root
        self.root.title("Gestion de Stock - Pharmacie")
        self.root.geometry("900*700")
        self.root.resizable(True, True)
        
        # Connexion à la base de données
        self.conn = sqlite3.connect('pharmacie.db')
        self.create_table()

        # Variables
        self.seuil_alerte = 10  # Seuil pour alerte stock faible 

        # Création de l'interface
        self.setup_ui()

        # Chargement des données
        self.refresh_stock()

        # Démarrer la verification automatique 
        self.check_alerte()

    def create_table(self):
        """Création de la table médicaments"""
        cursor = self.conn.cursor()
        cursor.execute('''
             CREATE TABLE IF NOT EXISTS medicaments (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                nom TEXT NOT NULL,
                quantite INTEGER NOT NULL,
                date_expirate TEXT NOT NULL,
                date_ajout TEXT NOT NULL
            )
        ''')
        self.conn.comit()
    def setup_ui(self):
        """"Configuration de l'interface utilisateur"""

        # Stye 
        Style = ttk.Style()
        Style.theme_user('clam')

        # Couleurs 
        self.bg_color = '#f0f0f0'
        self.header_color = '#2c3e50'
        self.button_color = '#3498db'
        self.alert_color = '#e74c3c'

        self.root.configure(bg=self.bg_color)

        # Titre principal
        title_frame = tk.Frame(self.root, bg=self.header_color, height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text="Gestion de stock de Pharmacie ",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg=self.header_color
        )
        title_label.pack(expand=True)
        
        # Frame principal avec onglets
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Onglet 1: Ajouter médicament 
        self.tab_ajout = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ajout, text="Ajouter médicament")
        self.setup_tab_ajout()

        # Onglet 2: Stock actuel 
        self.tab_stock = ttk.Frame
        self.notebook.add(self.tab_stock, text="Stock actuel")
        self.setup_tab_stock()

        # Onglet 3: Entrées/Sorties
        self.tab_mouvements = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_mouvements, text="Mouvements")
        self.setup_tab_mouvements()

        # Onglet 4: Alertes
        self.tab_alertes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_alertes, text="Alertes")
        self.setup_tab_alertes()

        # Barre de statut
        self.status_bar = tk.Label(
            self.root,
            text="Pret",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
            )
        self.status_bar.pack(side=tk.BOTTOM, fill='x')
    def setup_tab_ajout(self):
        """Configuration de l'onglet d'ajout"""
        # Frame pour le formulaire
        form_frame = ttk.LabelFrame(self.tab_ajout, text="Nouveau médicament", padding=10)
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Nom
        ttk.Label(form_frame, text="Nom du médicament:").grid(row=0, column=0, sticky='w', pady=5)
        self.quantite_entry = ttk.Entry(form_frame, width=40)
        self.nom_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Quantité 
        ttk.Label(form_frame, text="Quantité:").grid(row=1, column=0, sticky='w', pady=5)
        self.quantite_entry = ttk.Entry(form_frame, width=20)
        self.quantite_entry.grid(row=1, column=1, sticky='w', padx=10, pady=5)

        # Date d'expiration 
        ttk.Label(form_frame, text="Date d'expiration (JJ/MM/AAAA):").grid(row=2, column=0, sticky='w', pady=5)
        self.date_entry = ttk.Entry(form_frame, width=20)
        self.date_entry.grid(row=2, column=1, sticky='w', padx=10, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))

        # Bouton Ajouter
        add_btn = tk.Button(
            form_frame,
            text="Ajouter médicament",
            bg=self.button_color,
            fg='white',
            font=('Arial', 10, 'bold'),
            command=self.ajouter_medicament
        )
        add_btn.grid(row=3, column=0,columnspan=2, pady=20)

        # Zone d'information 
        info_text = """
        Instructions:
        - Remplissez tous les champs
        - La quantité doit etre un nombre entier positif
        - Format de date: JJ/MM/AAAA
        """
        info_label = tk.Label(
            form_frame,
            text=info_text,
            justify='left',
            font=('Arial',9),
            fg='gray'
        )
        info_label.grid(row=4, column=0, columnspan=2, pady=10)

    def setup_tab_stock(self):
        """Configuration de l'onglet stock"""
        # Frame pour les controles
        control_frame = tk.Frame(self.tab_stock)
        control_frame.pack(fill='x', padx=10, pady=10)

        # Bouton de rafraichissement
        refresh_btn = tk.Button(
            control_frame,
            text="Rafraichir",
            bg=self.button_color,
            fg='white',
            command=self.refresh_stock
        )
        refresh_btn.pack(side='left', padx=5)

        # Recherche
        ttk.Label(control_frame, text="Recherche:").pack(side='left', padx=20)
        self.search_entry = ttk.Entry(control_frame, width=30)
        self.search_entry.pack(side='eft')
        self.search_entry.bind('<keyRelease>', self.search_medicament)

        # Treeview pour afficher le stock
        columns = ('ID', 'Nom', 'Quantité', 'Date expiration' , 'Statut')
        self.tree = ttk.Treeview(self.tab_stock, columns=columns, show='headings', height=20)

        # Definir les en-tetes
        self.tree.heading('ID' , text='ID')
        self.tree.heading('Nom' , text='Nom')
        self.tree.heading('Quantité' , text='Quantite')
        self.tree.heading('Date expiration' , text='Date expiration')
        self.tree.heading('Statut', text='statut')

        # Largeur des couleures
        self.tree.column('ID' , width=50)
        self.tree.column('Nom' , width=250)
        self.tree.column('Quantite' , width=100)
        self.tree.column('Date expiration' , width=150)
        self.tree.column('Statut' , width=100)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tab_stock, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Placement
        self.tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side='right' , fill='y', padx=(0, 10), pady=10)

        # Bind double-clic pour voir les details
        self.tree.bind('<Double-Button-1>', self.show_medicament_details)

    def setup_tab_mouvements(self):
        """Configuration de l'onglet mouvements"""
        # Frame pour les entrées
        entrees_frame = ttk.LabelFrame(self.tab_mouvements, text="Enregistre une entrée ", padding=10)
        entrees_frame.pack(fill='x', padx=10, pady=10)

        # Séletion médicament
        ttk.Label(entrees_frame, text="Médicament:").grid(row=0, column=0, sticky='W', pady=5)
        self.med_entrees_combo = ttk.Combobox(entrees_frame, width=40)
        self.med_entrees_combo.grid(row=0, column=1, padx=10, pady=5)

        # Quantité entrée
        ttk.Label(entrees_frame, text="Quantité à ajouter:").grid(row=1, column=0, sticky='W', pady=5)
        self.qte_entree_entry = ttk.Entry(entrees_frame, width=20)
        self.qte_entree_entry.grid(row=1, column=1, sticky='w', padx=10, pady=5)

        # Bouton entrée
        entree_btn = tk.Button(
            entrees_frame,
            text="Ajouter au stock",
            bg='green',
            fg='white',
            command=self.enregistrer_entree
        )
        entree_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Frame pour les sorties
        sorties_frame = ttk.LabelFrame(self.tab_mouvements, text="Enregistrer une sortie(vente)", padding=10)
        sorties_frame.pack(fill='x' , padx=10, pady=10)

        # Sélection médicament 
        ttk.Label(sorties_frame, text="Medicament:").grid(row=0, column=0, sticky='w' , pady=5)
        self.med_sorties_combo = ttk.Combobox(sorties_frame, width=40)
        self.med_sorties.grid(row=0, column=1, sticky='w', padx=10, pady=5)

        # Quantité sortie
        ttk.Label(sorties_frame, text="Quantité à vendre:").grid(row=1, column=0, sticky='w' , pady=5)
        self.qte_sorties_entry = ttk.Entry(sorties_frame, width=20)

        # Bouton sortie
        sortie_btn = tk.Button(
            sorties_frame,
            text="Vendre",
            bg='orange',
            fg='white',
            comman=self.enregistrer_sortie
        )
        sortie_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Mettre à jour les combobox
        self.update_comboboxes()

    def setup_tab_alertes(self):
        """Configuration de l'onglet alertes"""
        # Frame pour les paramètres
        param_frame = ttk.LabelFrame(self.tab_alertes, text="paramèetres d'alerte", padding=10)
        param_frame.pack(fill='x', padx=10, pady=10)

        ttk.Label(param_frame, text="seuil d'alerte (quantité minimum):").grid(row=0, column=0, sticky='w', pady=5)
        self.seuil_entry = ttk.Entry(param_frame, width=10)
        self.seuil_entry.grid(row=0, column=1, padx=10, pady=5)
        self.seuil_entry.insert(0, str(self.seuil_alerte))

        seuil_btn = tk.Button(
            param_frame,
            text="Mettre à jour",
            bg=self.button_color,
            fg='white',
            command=self.update_seuil
        )
        seuil_btn.grid(row=0, column=2, padx=10)

        # Zone d'affichage des alertes
        alert_frame = ttk.LabelFrame(self.tab_alertes, text="Alertes en cours", padding=10)
        alert_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.alert_text = scrolledtext.ScrolledText(
            alert_frame,
            height=15,
            width=80,
            font=('Arial', 10)
        )
        self.alert_text.pack(fill='both', expand=True)

        # Bouton pour vérifier les alertes
        check_btn = tk.Button(
            self.tab_alertes,
            text="Vérifier les alertes",
            bg='red',
            fg='white',
            command=self.check_and_show_alerts
        )
        check_btn.pack(pady=10)

    def ajouter_medicament(self):
        """Ajouter un nouveau medicaments"""
        