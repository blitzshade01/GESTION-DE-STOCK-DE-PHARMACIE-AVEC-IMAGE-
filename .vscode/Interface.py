import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

fichier = "pharmacie.json"

# 1. CHARGEMENT DES DONNÉES
if os.path.exists(fichier):
    with open(fichier, 'r') as f: 
        stock = json.load(f)
else:
    # Initialisation si le fichier n'existe pas
    stock = [
        {"nom": "Doliprane 500mg", "qte": 45, "prix": 2.50},
        {"nom": "Doliprane 1000mg", "qte": 12, "prix": 3.20},
        {"nom": "Aspirine", "qte": 3, "prix": 1.80},
        {"nom": "Ibuprofène", "qte": 2, "prix": 4.50},
        {"nom": "Paracétamol", "qte": 1, "prix": 2.00},
    ]

# 2. LOGIQUE D'ALERTE (Ce que tu as demandé)
def verifier_alerte():
    """Parcourt le stock et affiche une boîte de dialogue si < 5"""
    faibles = [m for m in stock if m['qte'] < 5]
    if faibles:
        msg = "🚨 STOCK CRITIQUE (< 5 unités) :\n\n"
        msg += "\n".join([f"• {m['nom']} : reste {m['qte']}" for m in faibles])
        messagebox.showwarning("Alerte Réapprovisionnement", msg)

def sauver():
    with open(fichier, 'w') as f: 
        json.dump(stock, f, indent=4)

def rafraichir_liste():
    listbox.delete(0, tk.END)
    for med in stock:
    couleur = "🔴" if med['qte'] < 5 else "✅"
        listbox.insert(tk.END, f"{couleur} {med['nom']} - Stock: {med['qte']} - {med['prix']}$")

def action_vendre():
    # Exemple de logique de vente pour tester l'alerte
    messagebox.showinfo("Succès", "Vente effectuée !")
    verifier_alerte() # On vérifie après chaque mouvement

# 3. INTERFACE GRAPHIQUE
app = tk.Tk()
app.title("GESTION PHARMACIE")
app.geometry("800x600")
app.configure(bg="lightgray")

# Titre
tk.Label(app, text="GESTION DES PRODUITS PHARMACEUTIQUES", 
         font=("Arial", 16, "bold"), bg='lightgray').pack(pady=10)

# Liste des produits
list_frame = tk.LabelFrame(app, text="Inventaire en temps réel", bg='lightgray')
list_frame.pack(pady=10, padx=10, fill='both', expand=True)

listbox = tk.Listbox(list_frame, font=("Courier", 10))
listbox.pack(fill='both', expand=True, padx=5, pady=5)

# Zone de vente
vente_frame = tk.LabelFrame(app, text="Zone de Vente", bg='lightblue')
vente_frame.pack(pady=10, padx=10, fill='x')

tk.Button(vente_frame, text="CONFIRMER LA VENTE", bg='darkgreen', fg='white', 
          font=("Arial", 10, "bold"), command=action_vendre).pack(pady=10)

# Barre de progression (Démo)
progress = ttk.Progressbar(app, length=300, mode='determinate')
progress.pack(pady=5)
progress['value'] = 75

# --- LANCEMENT ---
rafraichir_liste()
# L'alerte se déclenche automatiquement à l'ouverture du logiciel
app.after(1000, verifier_alerte) 

app.mainloop()

