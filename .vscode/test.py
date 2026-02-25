import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


fichier = "pharmacie.json"
stock = []
panier = []

if os.path.exists(fichier):
    with open(fichier, 'r') as f: stock = json.load(f)
else:
    stock = [
        {"nom": "Doliprane 500mg", "qte": 45, "prix": 2.50},
        {"nom": "Doliprane 1000mg", "qte": 12, "prix": 3.20},
        {"nom": "Aspirine", "qte": 8, "prix":1.80},
        {"nom": "Ibuprofène", "qte": 3, "prix": 4.50},
        {"nom": "Paracétamol", "qte": 2,"prix":2.00},
    ]
    
def sauver()
    with open(fichier, 'w') as f: json.dump(stock)