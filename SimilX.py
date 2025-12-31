import tkinter as tk
from tkinter import ttk, filedialog
import json
import matplotlib.pyplot as plt

# Import du modèle externe
from model_loader import load_model

# Chargement du modèle
vocab, vecteurs, phrases, model_description = load_model()

# ================== CONFIG VISUELLE SIMPLE ==================

BG = "#1e1e1e"
FG = "#ffffff"
ACCENT = "#4caf50"
FRAME_BG = "#2c2c2c"
TEXT_FG = "#dcdcdc"
EDIT_BG = "#333333"
EDIT_FG = "#00ff99"
DEBUG_FG = "#ffcc66"

FONT_NORMAL = ("Segoe UI", 11)
FONT_TITLE = ("Segoe UI", 13, "bold")

THEMES = {
    "dark": {
        "bg": "#1e1e1e",
        "fg": "#ffffff",
        "accent": "#4caf50",
        "frame": "#2c2c2c",
        "text": "#dcdcdc",
        "edit_bg": "#333333",
        "edit_fg": "#00ff99",
        "debug_fg": "#ffcc66"
    },
    "light": {
        "bg": "#f0f0f0",
        "fg": "#000000",
        "accent": "#1976d2",
        "frame": "#ffffff",
        "text": "#222222",
        "edit_bg": "#e0f7fa",
        "edit_fg": "#00695c",
        "debug_fg": "#8e24aa"
    }
}

CURRENT_THEME_NAME = "dark"
CURRENT_THEME = THEMES[CURRENT_THEME_NAME]

# ================== MÉMOIRE ==================

memoire = {
    "list1": None,
    "list2": None,
    "historique": []
}

# ================== REGISTRES POUR LE THEME ==================

all_frames = []
all_labels = []
all_buttons = []
all_texts = []

# ================== FONCTIONS ==================

def update_list(num, valeurs):
    memoire[f"list{num}"] = valeurs
    zone = zone_vecteur1 if num == 1 else zone_vecteur2
    zone.config(state="normal")
    zone.delete("1.0", "end")
    zone.insert("end", f"list{num} = {valeurs}\n")
    zone.config(state="disabled")
    maj_listes_onglet2()

def maj_listes_onglet2():
    zone_listes.config(state="normal")
    zone_listes.delete("1.0", "end")
    zone_listes.insert("end", f"list1 = {memoire['list1']}\n\n")
    zone_listes.insert("end", f"list2 = {memoire['list2']}\n")
    zone_listes.config(state="disabled")

def generer_vecteur1():
    mot = entry_mot1.get().strip()
    zone_vecteur1.config(state="normal")
    zone_vecteur1.delete("1.0", "end")
    if mot not in vecteurs:
        zone_vecteur1.insert("end", f"[ERREUR] Mot inconnu : {mot}\n")
        zone_vecteur1.config(state="disabled")
        return
    update_list(1, vecteurs[mot])

def generer_vecteur2():
    mot = entry_mot2.get().strip()
    zone_vecteur2.config(state="normal")
    zone_vecteur2.delete("1.0", "end")
    if mot not in vecteurs:
        zone_vecteur2.insert("end", f"[ERREUR] Mot inconnu : {mot}\n")
        zone_vecteur2.config(state="disabled")
        return
    update_list(2, vecteurs[mot])

def appliquer_list1():
    texte = zone_edit_list1.get("1.0", "end").strip()
    try:
        valeurs = [float(x) for x in texte.replace(",", " ").split()]
        update_list(1, valeurs)
    except:
        zone_vecteur1.config(state="normal")
        zone_vecteur1.delete("1.0", "end")
        zone_vecteur1.insert("end", "[ERREUR] Format invalide. Exemple : 1 2 3.5 10\n")
        zone_vecteur1.config(state="disabled")

def appliquer_list2():
    texte = zone_edit_list2.get("1.0", "end").strip()
    try:
        valeurs = [float(x) for x in texte.replace(",", " ").split()]
        update_list(2, valeurs)
    except:
        zone_vecteur2.config(state="normal")
        zone_vecteur2.delete("1.0", "end")
        zone_vecteur2.insert("end", "[ERREUR] Format invalide. Exemple : 5 10 20.5\n")
        zone_vecteur2.config(state="disabled")

def clear_resultats():
    for zone in (zone_resultat, zone_debug, zone_historique):
        zone.config(state="normal")
        zone.delete("1.0", "end")
        zone.config(state="disabled")

def comparer_vecteurs():
    zone_resultat.config(state="normal")
    zone_debug.config(state="normal")
    zone_historique.config(state="normal")

    zone_resultat.delete("1.0", "end")
    zone_debug.delete("1.0", "end")

    list1 = memoire["list1"]
    list2 = memoire["list2"]

    if list1 is None or list2 is None:
        zone_resultat.insert("end", "Erreur : list1 ou list2 n'est pas générée.\n")
        for z in (zone_resultat, zone_debug, zone_historique):
            z.config(state="disabled")
        return

    n = max(len(list1), len(list2))
    zone_resultat.insert("end", f"Nombre d'itérations : {n}\n\n")

    zone_resultat.tag_configure("proche", background="#444444", foreground="#00ff99")

    iteration_data = []

    for idx in range(n):
        v1 = list1[idx] if idx < len(list1) else None
        v2 = list2[idx] if idx < len(list2) else None
        it = idx + 1

        zone_debug.insert("end", f"it={it} | v1={v1} | v2={v2}\n")

        if v1 is not None and v2 is not None:
            similarite = 1 / (1 + abs(v1 - v2))
            similarite_pct = similarite * 100
        else:
            similarite = None
            similarite_pct = None

        iteration_data.append({
            "it": it,
            "v1": v1,
            "v2": v2,
            "similarite": similarite,
            "similarite_pct": similarite_pct
        })

        start = zone_resultat.index("end")
        zone_resultat.insert(
            "end",
            f"Iteration {it}\n"
            f"  - v1 : {v1}\n"
            f"  - v2 : {v2}\n"
            f"  - similarité : {similarite}\n"
            f"  - similarité (%) : {similarite_pct}\n\n"
        )
        end = zone_resultat.index("end")

        if v1 is not None and v2 is not None and abs(v1 - v2) < 0.1:
            zone_resultat.tag_add("proche", start, end)

    memoire["historique"].append({
        "list1": list1,
        "list2": list2,
        "iterations": iteration_data
    })

    zone_historique.insert("end", f"Comparaison {len(memoire['historique'])} : {n} itérations\n")

    for z in (zone_resultat, zone_debug, zone_historique):
        z.config(state="disabled")

# ================== EXPORT JSON ==================

def exporter_json():
    if not memoire["historique"]:
        return

    fichier = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON", "*.json")],
        title="Exporter l'historique"
    )

    if not fichier:
        return

    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(memoire, f, indent=4, ensure_ascii=False)

# ================== GRAPHIQUE ==================

def afficher_graphique():
    list1 = memoire["list1"]
    list2 = memoire["list2"]

    if list1 is None or list2 is None:
        return

    n = max(len(list1), len(list2))
    x = list(range(1, n + 1))

    y1 = [list1[i] if i < len(list1) else None for i in range(n)]
    y2 = [list2[i] if i < len(list2) else None for i in range(n)]

    plt.figure(figsize=(8, 4))
    plt.plot(x, y1, marker="o", label="v1")
    plt.plot(x, y2, marker="o", label="v2")
    plt.title("Comparaison des valeurs v1 et v2")
    plt.xlabel("Itération")
    plt.ylabel("Valeur")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# ================== THEME ==================

def appliquer_theme():
    t = CURRENT_THEME

    root.configure(bg=t["bg"])

    for frame in all_frames:
        frame.configure(bg=t["bg"])

    for label in all_labels:
        label.configure(bg=t["bg"], fg=t["fg"])

    for button in all_buttons:
        button.configure(bg=t["accent"], fg=t["fg"], activebackground=t["accent"])

    for text in all_texts:
        editable = text.cget("state") != "disabled"

        if text is zone_debug:
            text.configure(
                bg=t["frame"],
                fg=t["debug_fg"],
                insertbackground=t["debug_fg"]
            )
        elif editable:
            text.configure(
                bg=t["edit_bg"],
                fg=t["edit_fg"],
                insertbackground=t["edit_fg"]
            )
        else:
            text.configure(
                bg=t["frame"],
                fg=t["text"],
                insertbackground=t["accent"]
            )

def basculer_theme():
    global CURRENT_THEME_NAME, CURRENT_THEME
    CURRENT_THEME_NAME = "light" if CURRENT_THEME_NAME == "dark" else "dark"
    CURRENT_THEME = THEMES[CURRENT_THEME_NAME]
    appliquer_theme()

# ================== INTERFACE ==================

def lancer_gui():
    global root
    global entry_mot1, entry_mot2
    global zone_vecteur1, zone_vecteur2
    global zone_edit_list1, zone_edit_list2
    global zone_listes, zone_resultat, zone_debug, zone_historique
    global all_frames, all_labels, all_buttons, all_texts

    all_frames = []
    all_labels = []
    all_buttons = []
    all_texts = []

    root = tk.Tk()
    root.title("SimilX – Analyseur de similarité vectorielle")
    root.geometry("1200x800")
    root.configure(bg=BG)

    menu_bar = tk.Menu(root)

    theme_menu = tk.Menu(menu_bar, tearoff=0)
    theme_menu.add_command(label="Basculer clair/sombre", command=basculer_theme)
    menu_bar.add_cascade(label="Affichage", menu=theme_menu)

    export_menu = tk.Menu(menu_bar, tearoff=0)
    export_menu.add_command(label="Exporter en JSON", command=exporter_json)
    menu_bar.add_cascade(label="Exporter", menu=export_menu)

    root.config(menu=menu_bar)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=5, pady=5)

    onglet1 = tk.Frame(notebook, bg=BG)
    onglet2 = tk.Frame(notebook, bg=BG)
    notebook.add(onglet1, text="Vecteurs / Listes")
    notebook.add(onglet2, text="Comparaison")

    all_frames.extend([onglet1, onglet2])

    l1 = tk.Label(onglet1, text="Mot 1 :", fg=FG, bg=BG, font=FONT_TITLE)
    l1.pack(pady=5)
    all_labels.append(l1)

    entry_mot1 = tk.Entry(onglet1, font=FONT_NORMAL)
    entry_mot1.pack()

    b1 = tk.Button(onglet1, text="Générer vecteur 1 → list1", command=generer_vecteur1,
                   bg=ACCENT, fg=FG, font=FONT_NORMAL)
    b1.pack(pady=5)
    all_buttons.append(b1)

    zone_vecteur1 = tk.Text(onglet1, height=5, width=80, bg=FRAME_BG, fg=TEXT_FG,
                            insertbackground=ACCENT, font=FONT_NORMAL)
    zone_vecteur1.pack(pady=10)
    zone_vecteur1.config(state="disabled")
    all_texts.append(zone_vecteur1)

    l_edit1 = tk.Label(onglet1, text="Modifier list1 manuellement (espaces ou virgules) :",
                       fg=FG, bg=BG, font=FONT_NORMAL)
    l_edit1.pack(pady=5)
    all_labels.append(l_edit1)

    zone_edit_list1 = tk.Text(onglet1, height=3, width=80, bg=EDIT_BG, fg=EDIT_FG,
                              insertbackground=EDIT_FG, font=FONT_NORMAL)
    zone_edit_list1.pack(pady=5)
    all_texts.append(zone_edit_list1)

    b_edit1 = tk.Button(onglet1, text="Appliquer list1", command=appliquer_list1,
                        bg=ACCENT, fg=FG, font=FONT_NORMAL)
    b_edit1.pack(pady=5)
    all_buttons.append(b_edit1)

    l2 = tk.Label(onglet1, text="Mot 2 :", fg=FG, bg=BG, font=FONT_TITLE)
    l2.pack(pady=10)
    all_labels.append(l2)

    entry_mot2 = tk.Entry(onglet1, font=FONT_NORMAL)
    entry_mot2.pack()

    b2 = tk.Button(onglet1, text="Générer vecteur 2 → list2", command=generer_vecteur2,
                   bg=ACCENT, fg=FG, font=FONT_NORMAL)
    b2.pack(pady=5)
    all_buttons.append(b2)

    zone_vecteur2 = tk.Text(onglet1, height=5, width=80, bg=FRAME_BG, fg=TEXT_FG,
                            insertbackground=ACCENT, font=FONT_NORMAL)
    zone_vecteur2.pack(pady=10)
    zone_vecteur2.config(state="disabled")
    all_texts.append(zone_vecteur2)

    l_edit2 = tk.Label(onglet1, text="Modifier list2 manuellement (espaces ou virgules) :",
                       fg=FG, bg=BG, font=FONT_NORMAL)
    l_edit2.pack(pady=5)
    all_labels.append(l_edit2)

    zone_edit_list2 = tk.Text(onglet1, height=3, width=80, bg=EDIT_BG, fg=EDIT_FG,
                              insertbackground=EDIT_FG, font=FONT_NORMAL)
    zone_edit_list2.pack(pady=5)
    all_texts.append(zone_edit_list2)

    b_edit2 = tk.Button(onglet1, text="Appliquer list2", command=appliquer_list2,
                        bg=ACCENT, fg=FG, font=FONT_NORMAL)
    b_edit2.pack(pady=5)
    all_buttons.append(b_edit2)
  
    top_actions = tk.Frame(onglet2, bg=BG)
    top_actions.pack(pady=10)
    all_frames.append(top_actions)

    b_compare = tk.Button(top_actions, text="Comparer list1 et list2", command=comparer_vecteurs,
                          bg=ACCENT, fg=FG, font=FONT_NORMAL)
    b_compare.pack(side="left", padx=5)
    all_buttons.append(b_compare)

    b_clear = tk.Button(top_actions, text="Clear", command=clear_resultats,
                        bg=ACCENT, fg=FG, font=FONT_NORMAL)
    b_clear.pack(side="left", padx=5)
    all_buttons.append(b_clear)

    b_graph = tk.Button(top_actions, text="Graphique", command=afficher_graphique,
                        bg=ACCENT, fg=FG, font=FONT_NORMAL)
    b_graph.pack(side="left", padx=5)
    all_buttons.append(b_graph)

    l_listes = tk.Label(onglet2, text="Listes actuelles :", fg=FG, bg=BG, font=FONT_TITLE)
    l_listes.pack()
    all_labels.append(l_listes)

    zone_listes = tk.Text(onglet2, height=5, width=100, bg=FRAME_BG, fg=TEXT_FG,
                          insertbackground=ACCENT, font=FONT_NORMAL)
    zone_listes.pack(pady=10)
    zone_listes.config(state="disabled")
    all_texts.append(zone_listes)

    l_res = tk.Label(onglet2, text="Résultats complets :", fg=FG, bg=BG, font=FONT_TITLE)
    l_res.pack()
    all_labels.append(l_res)

    zone_resultat = tk.Text(onglet2, height=15, width=100, bg=FRAME_BG, fg=TEXT_FG,
                            insertbackground=ACCENT, font=FONT_NORMAL)
    zone_resultat.pack(pady=10)
    zone_resultat.config(state="disabled")
    all_texts.append(zone_resultat)

    l_debug = tk.Label(onglet2, text="Debug (it, v1, v2) :", fg=FG, bg=BG, font=FONT_TITLE)
    l_debug.pack()
    all_labels.append(l_debug)

    zone_debug = tk.Text(onglet2, height=8, width=100, bg=FRAME_BG, fg=DEBUG_FG,
                        insertbackground=DEBUG_FG, font=FONT_NORMAL)
    zone_debug.pack(pady=10)
    zone_debug.config(state="disabled")
    all_texts.append(zone_debug)

    l_hist = tk.Label(onglet2, text="Historique des comparaisons :", fg=FG, bg=BG, font=FONT_TITLE)
    l_hist.pack()
    all_labels.append(l_hist)

    zone_historique = tk.Text(onglet2, height=6, width=100, bg=FRAME_BG, fg=TEXT_FG,
                              insertbackground=ACCENT, font=FONT_NORMAL)
    zone_historique.pack(pady=10)
    zone_historique.config(state="disabled")
    all_texts.append(zone_historique)

    all_frames.append(onglet2)

    appliquer_theme()

    maj_listes_onglet2()

    root.mainloop()

# ================== LANCEMENT ==================

if __name__ == "__main__":
    lancer_gui()
