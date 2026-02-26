import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

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

salim = tk.Tk()
salim.title("Gestion des stocks - Pharmacie")
salim.geometry("900x450")
salim.configure(bg="red")

def charger_donnees():
    for item in table.get_children():
        table.delete(item)

    cursor.execute("SELECT * FROM medicaments")
    rows = cursor.fetchall()

    for row in rows:
        table.insert("", tk.END, values=row[1:])
    verifier_stock

def ajouter_medicament():
    nom = entry_nom.get()
    prix = entry_prix.get()
    quantite = entry_quantite.get()

    if nom == "" or prix == "" or quantite == "":
        messagebox.showwarning("Erreur", "Veuillez remplir tous les champs")
        return

    heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO medicaments(nom, prix, quantite, heure_ajout, heure_retrait)
        VALUES(?,?,?,?,?)
    """, (nom, prix, quantite, heure, ""))

    conn.commit()
    charger_donnees()

def retirer_medicament():
    selected = table.focus()

    if selected == "":
        messagebox.showwarning("Erreur", "Sélectionnez un médicament")
        return

    valeur = table.item(selected, "values")
    nom = valeur[0]
    quantite_actuelle = int(valeur[2])

    try:
        qte_retrait = int(entry_retrait.get())
    except:
        messagebox.showwarning("Erreur", "Quantité invalide")
        return

    if qte_retrait <= 0:
        return

    if qte_retrait > quantite_actuelle:
        messagebox.showwarning("Erreur", "Stock insuffisant")
        return

    nouvelle_qte = quantite_actuelle - qte_retrait
    heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        UPDATE medicaments
        SET quantite=?, heure_retrait=?
        WHERE nom=?
    """, (nouvelle_qte, heure, nom))

    conn.commit()
    charger_donnees()

frame_form = tk.Frame(salim)
frame_form.pack(pady=5)

tk.Label(frame_form, text="Nom").grid(row=0, column=0)
entry_nom = tk.Entry(frame_form)
entry_nom.grid(row=0, column=1)

tk.Label(frame_form, text="Prix").grid(row=0, column=2)
entry_prix = tk.Entry(frame_form)
entry_prix.grid(row=0, column=3)

tk.Label(frame_form, text="Quantité").grid(row=0, column=4)
entry_quantite = tk.Entry(frame_form)
entry_quantite.grid(row=0, column=5)

btn_add = tk.Button(frame_form, text="Ajouter",bg="blue", command=ajouter_medicament)
btn_add.grid(row=0, column=6, padx=5)

frame_retrait = tk.Frame(salim)
frame_retrait.pack(pady=5)

tk.Label(frame_retrait, text="Quantité à retirer").grid(row=0, column=0)
entry_retrait = tk.Entry(frame_retrait)
entry_retrait.grid(row=0, column=1)

btn_remove = tk.Button(frame_retrait, text="Retirer",bg="green", command=retirer_medicament)
btn_remove.grid(row=0, column=2, padx=5)

colonnes = ("Nom", "Prix", "Stock", "Heure ajout", "Heure retrait")

table = ttk.Treeview(salim, columns=colonnes, show="headings")

for col in colonnes:
    table.heading(col, text=col)
    table.column(col, width=160)

table.pack(expand=True, fill="both", pady=10)

def verifier_stock():
    cursor.execute("""
        SELECT nom, quatite
        FROM medicaments
        WHERE quantite < 10 AND quantite > 0
        """)
    resultats=cursor.fetchall()
    if resultats:
        message=""
        for nom,qte in resultats:
            message += f"{nom}:reste{qte}\n"

        messagebox.showwarning("Alerte stock faible", "Les medicament suivants sont presque epuise : \n\n" + message)

charger_donnees()

salim.mainloop()

