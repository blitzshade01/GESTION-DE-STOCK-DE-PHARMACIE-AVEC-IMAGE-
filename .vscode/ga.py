tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from import datetime import datetime

# -------------------------
# Base de données
# -------------------------
conn = sqlite3.connect("pharmacie.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS medicaments(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    prix REAL,
    quantite INTEGER,
    heure_ajout TEXT,
    heure_retrait TEXT
)
""")
conn.commit()


