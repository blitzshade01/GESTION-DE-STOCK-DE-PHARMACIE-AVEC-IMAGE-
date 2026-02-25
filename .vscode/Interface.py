
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
    
def sauver():
    with open(fichier, 'w') as f: json.dump(stock, f, indent=4)
    
def verifier_alerte():
    faibles=[m for m in stock if m['qte']<5]
    if faibles:
        msg="Stock faible pour:\n" + "\n".join(f"{m['nom']} (qte: {m['qte']})" for m in faibles)
        messagebox.showwarning("Alerte Stock Faible", msg)
def rafraichir_liste():
    listbox.delete(0, tk.END)
    for med in stock:
        listbox.insert(tk.END, f"{med['nom']} - Stock: {med['qte']}")
app=tk.Tk()
app.title("GESTION DES STOCKS DES PRODUITS PHARMACEUTIQUE")
app.geometry("800x500")
app.configure(bg="lightgray")
medicaments = [
    {"nom": "Doliprane 500mg", "stock": 10},
    {"nom": "Aspirine", "stock": 3},  # Stock faible pour test
    {"nom": "Ibuprofène", "stock": 8}
]

def action():
    print("Action exécutée")
    verifier_stock()  # Vérifie le stock à chaque action

def verifier_stock_medicament(med):
    if med["stock"] < 5:
        messagebox.showwarning(
            "⚠ ALERTE STOCK FAIBLE",
            f"Le médicament '{med['nom']}' a un stock faible ({med['stock']}) !"
        )
            
menubar = tk.Menu(app)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Ajouter", command=action)
file_menu.add_command(label="Quitter", command=app.quit)
menubar.add_cascade(label="Fichier", menu=file_menu)
app.config(menu=menubar)

tk.Label(app, text="GESTION DES PRODUITS PHARMACEUTIQUES", font=("Arial", 16, "bold"),
         bg='lightgray').pack(pady=5)

rech_frame = tk.Frame(app, bg='lightgray')
rech_frame.pack(pady=5)

tk.Label(rech_frame, text="Rechercher:",bg='lightgray').pack(side='left')
entry_rech = tk.Entry(rech_frame, width=30)
entry_rech.pack(side='left', padx=5)
tk.Button(rech_frame, text="recherche", command=action).pack(side='left')

btn_frame = tk.Frame(app, bg='lightgray')
btn_frame.pack(pady=5)

for txt, cmd in [("Ajouter", action), ("Modifier", action),
                 ("Supprimer", action), ("Vendre", action)]:
    tk.Button(btn_frame, text=txt, command=cmd, width=12).pack(side='left', padx=2)
    
list_frame = tk.LabelFrame(app, text="Médicaments en stock", bg='lightgray')
list_frame.pack(pady=10, padx=10, fill='both', expand=True)

listbox = tk.Listbox(list_frame, height=6)
listbox.pack(fill='both', expand=True, padx=5, pady=5)

for med in ["Doliprane 500mg - stock: 45", "Doliprane 1000mg - Stock: 12",
            "Aspirine - Stock: 8", "Ibuproféne - Stock: 23"]:
    listbox.insert(tk.END, med)
    
vente_frame = tk.LabelFrame(app, text="Vente", bg='lightblue')
vente_frame.pack(pady=5, padx=10, fill='x')

qte_frame = tk.Frame(vente_frame, bg='lightblue')
qte_frame.pack(pady=2)

tk.Label(qte_frame, text="Quantité:", bg='lightblue').pack(side='left')
spin_qte = tk.Spinbox(qte_frame, from_=1, to=10, width=5)
spin_qte.pack(side='left', padx=5)

tk.Button(qte_frame, text="Ajouter au panier", command=action,
          bg='green', fg='white').pack(side='left', padx=10)

panier_frame = tk.Frame(vente_frame, bg='lightblue')
panier_frame.pack(pady=5, fill='x')

tk.Label(panier_frame, text="Vendre", bg='lightblue').pack(side='left')
tk.Label(panier_frame, text="0.00 $", bg='lightblue', font=("Arial", 10, "bold"),
         fg='green').pack(side='left', padx=10)

tk.Button(panier_frame, text="Vendre", command=action,
          bg='darkgreen', fg='white').pack(side='right', padx=2)
tk.Button(panier_frame, text="Annuler", command=action,
          bg='red', fg='white').pack(side='right', padx=2)

progress = ttk.Progressbar(app, length=200, mode='determinate')
progress.pack(pady=5)
progress['value'] = 50

filter_frame = tk.Frame(app, bg='lightgray')
filter_frame.pack(pady=5)

radio_var = tk.StringVar(value="tout")
tk.Radiobutton(filter_frame, text="Tous", variable=radio_var,
               value="tout", bg='lightgray').pack(side='left', padx=5)
tk.Radiobutton(filter_frame, text="Stock faible", variable=radio_var,
               value="faible", bg='lightgray').pack(side='left', padx=5)
tk.Radiobutton(filter_frame, text="Périmés", variable=radio_var,
               value="perime", bg='lightgray').pack(side='left', padx=5)

check_frame = tk.Frame(app, bg='lightgray')
check_frame.pack(pady=5)

check1 = tk.IntVar()
tk.Checkbutton(check_frame, text="Urgence", variable=check1,
               bg='lightgray').pack(side='left', padx=10)
check2 = tk.IntVar()


combo_frame = tk.Frame(app, bg='lightgray')
combo_frame.pack(pady=5)

tk.Label(combo_frame, text="Trier par:", bg='lightgray').pack(side='left')
combo = ttk.Combobox(combo_frame, values=["Nom", "Prix","Stock"], width=10)
combo.set("Nom")
combo.pack(side='left', padx=5)

app.mainloop()