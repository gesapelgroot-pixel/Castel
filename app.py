from flask import Flask, render_template, request, redirect
import sqlite3
import random
from datetime import datetime

app = Flask(__name__)

ADMIN_NUMERO = "333"

# -------------------------
# RESET DATABASE AU LANCEMENT
# -------------------------

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS Joueurs")
    c.execute("DROP TABLE IF EXISTS Historique")
    c.execute("DROP TABLE IF EXISTS Gages")

    c.execute("""
    CREATE TABLE Joueurs (
        numero TEXT PRIMARY KEY,
        score INTEGER,
        gage_en_cours TEXT,
        etat_gage TEXT
    )
    """)

    c.execute("""
    CREATE TABLE Gages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        texte TEXT,
        points INTEGER,
        actif INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE Historique (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_joueur TEXT,
        texte_gage TEXT,
        points INTEGER,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

def inserer_gages():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

        gages = [
    # FUN & RAPIDES - 1 point
    ("Faire un compliment sincère à quelqu’un.", 1, 1),
    ("Faire un check original à 3 personnes.", 1, 1),
    ("Faire une photo drôle avec un inconnu.", 1, 1),
    ("Lancer un “applaudissement général” sans raison.", 1, 1),
    ("Parler avec un accent pendant 5 minutes.", 1, 1),
    ("Faire une pose mannequin pendant 30 secondes.", 1, 1),
    ("Inventer un slogan pour la soirée.", 1, 1),
    ("Faire deviner ton numéro sans le dire.", 1, 1),
    ("Danser 20 secondes sur la musique en cours.", 1, 1),
    ("Faire un selfie avec quelqu’un de plus de 30 ans.", 1, 1),
    ("Faire un selfie avec quelqu’un de moins de 18 ans.", 1, 1),
    ("Dire un souvenir gênant (soft).", 1, 1),
    ("Faire semblant d’être un serveur pendant 3 minutes.", 1, 1),
    ("Imiter un prof du lycée.", 1, 1),
    ("Faire une déclaration dramatique à une chaise.", 1, 1),
    ("Faire un slow imaginaire.", 1, 1),
    ("Changer de place avec quelqu’un au hasard.", 1, 1),
    ("Faire rire quelqu’un en moins de 1 minute.", 1, 1),
    ("Dire “c’est incroyable” 5 fois dans une discussion.", 1, 1),
    ("Donner un surnom à quelqu’un pour la soirée.", 1, 1),

    # SOCIAUX - 2 points
    ("Trouver quelqu’un né le même mois que toi.", 2, 1),
    ("Faire un duo danse improvisé.", 2, 1),
    ("Organiser une mini ola dans la pièce.", 2, 1),
    ("Faire un high five à 10 personnes.", 2, 1),
    ("Convaincre quelqu’un de faire un gage avec toi.", 2, 1),
    ("Faire une photo de groupe improvisée.", 2, 1),
    ("Demander un conseil de vie à un adulte.", 2, 1),
    ("Apprendre un mot d’argot à quelqu’un de plus âgé.", 2, 1),
    ("Complimenter 3 personnes différentes.", 2, 1),
    ("Faire croire que tu annonces quelque chose d’important.", 2, 1),
    ("Lancer un mini concours de pierre-feuille-ciseaux.", 2, 1),
    ("Faire une interview rapide d’un invité.", 2, 1),
    ("Faire dire “18 ans déjà ?!” à quelqu’un.", 2, 1),
    ("Trouver quelqu’un qui porte la même couleur que toi.", 2, 1),
    ("Faire un duo TikTok (même faux).", 2, 1),
    ("Organiser une photo “génération ado vs adultes”.", 2, 1),
    ("Faire un compliment à quelqu’un que tu connais peu.", 2, 1),
    ("Rassembler 5 personnes pour crier “JOYEUX ANNIVERSAIRE”.", 2, 1),

    # DRÔLES - 3 points
    ("Faire un discours de 30 secondes comme si tu étais maire.", 3, 1),
    ("Imiter une star connue.", 3, 1),
    ("Improviser une pub pour la soirée.", 3, 1),
    ("Parler en rimes pendant 2 minutes.", 3, 1),
    ("Faire une entrée dramatique dans la pièce.", 3, 1),
    ("Jouer une scène de film connue.", 3, 1),
    ("Faire semblant d’être le DJ.", 3, 1),
    ("Faire un défilé de mode.", 3, 1),
    ("Faire une déclaration d’amitié publique.", 3, 1),
    ("Parler comme un commentateur sportif.", 3, 1),
    ("Faire semblant d’avoir gagné un Oscar.", 3, 1),
    ("Inventer une histoire absurde sur l’organisateur.", 3, 1),
    ("Faire une danse robot.", 3, 1),
    ("Faire un battle de regard.", 3, 1),
    ("Faire une imitation animale.", 3, 1),
    ("Faire un rap improvisé sur la soirée.", 3, 1),
    ("Raconter la soirée comme si c’était un documentaire.", 3, 1),
    ("Faire semblant d’être un influenceur.", 3, 1),
    ("Jouer une scène romantique avec un objet.", 3, 1),
    ("Faire un discours comme si tu avais 80 ans.", 3, 1),

    # CHALLENGE - 4 points
    ("Faire 10 squats en chantant.", 4, 1),
    ("Deviner 3 chansons au blind test rapide.", 4, 1),
    ("Faire rire 3 personnes différentes.", 4, 1),
    ("Réussir un défi danse imposé.", 4, 1),
    ("Faire un compliment original à 5 personnes.", 4, 1),
    ("Organiser un mini concours express.", 4, 1),
    ("Faire une pyramide humaine (sécurisée).", 4, 1),
    ("Convaincre quelqu’un de chanter avec toi.", 4, 1),
    ("Raconter une anecdote drôle en 30 secondes.", 4, 1),
    ("Faire un battle de danse.", 4, 1),
    ("Garder un accent pendant 10 minutes.", 4, 1),
    ("Réussir un défi “ne pas sourire” 1 minute.", 4, 1),
    ("Faire un discours sérieux… qui finit absurde.", 4, 1),
    ("Faire lever toute la pièce.", 4, 1),
    ("Trouver 3 personnes qui ont déjà travaillé.", 4, 1),
    ("Lancer un chant collectif.", 4, 1),
    ("Faire une pose photo collective originale.", 4, 1),
    ("Inventer un cri de guerre de la soirée.", 4, 1),
    ("Faire un compliment public à un adulte.", 4, 1),
    ("Organiser un mini toast improvisé.", 4, 1)
]

        c.executemany(
        "INSERT INTO Gages (texte, points, actif) VALUES (?, ?, ?)",
        gages
    )

    conn.commit()
    conn.close()

init_db()
inserer_gages()

# -------------------------
# DB
# -------------------------

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# -------------------------
# TIRER GAGE NON FAIT
# -------------------------

def tirer_gage(conn, numero):
    gages = conn.execute("""
        SELECT * FROM Gages
        WHERE actif = 1
        AND texte NOT IN (
            SELECT texte_gage FROM Historique WHERE numero_joueur = ?
        )
    """, (numero,)).fetchall()

    if not gages:
        return None

    return random.choice(gages)

# -------------------------
# PAGE PRINCIPALE
# -------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()

    if request.method == "POST":
        numero = request.form["numero"]

        # ADMIN
        if numero == ADMIN_NUMERO:
            return redirect("/admin")

        joueur = conn.execute(
            "SELECT * FROM Joueurs WHERE numero=?",
            (numero,)
        ).fetchone()

        if not joueur:
            conn.execute(
                "INSERT INTO Joueurs VALUES (?, 0, '', 'aucun')",
                (numero,)
            )
            conn.commit()

        gage = tirer_gage(conn, numero)

        historique = conn.execute("""
            SELECT texte_gage, points FROM Historique
            WHERE numero_joueur=?
        """, (numero,)).fetchall()

        return render_template("index.html",
                               numero=numero,
                               gage=gage,
                               historique=historique)

    return render_template("index.html", gage=None)

# -------------------------
# VALIDER DÉFI
# -------------------------

@app.route("/valider", methods=["POST"])
def valider():
    conn = get_db()
    numero = request.form["numero"]

    joueur = conn.execute(
        "SELECT * FROM Joueurs WHERE numero=?",
        (numero,)
    ).fetchone()

    gage = conn.execute(
        "SELECT * FROM Gages WHERE texte=?",
        (joueur["gage_en_cours"],)
    ).fetchone()

    if gage:
        nouveau_score = joueur["score"] + gage["points"]

        conn.execute(
            "UPDATE Joueurs SET score=?, etat_gage='termine' WHERE numero=?",
            (nouveau_score, numero)
        )

        conn.execute(
            "INSERT INTO Historique (numero_joueur, texte_gage, points, date) VALUES (?, ?, ?, ?)",
            (numero, gage["texte"], gage["points"], datetime.now())
        )

        conn.commit()

    return redirect("/?numero=" + numero + "&confetti=1")

# -------------------------
# ADMIN PANEL
# -------------------------

@app.route("/admin")
def admin():
    conn = get_db()

    joueurs = conn.execute("""
        SELECT * FROM Joueurs ORDER BY score DESC
    """).fetchall()

    historique = conn.execute("""
        SELECT * FROM Historique ORDER BY date DESC
    """).fetchall()

    return render_template("admin.html",
                           joueurs=joueurs,
                           historique=historique)

# -------------------------

@app.route("/health")
def health():
    return "OK", 200

import os

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))




