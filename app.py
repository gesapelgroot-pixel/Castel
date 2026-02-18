from flask import Flask, render_template, request, redirect, session
import sqlite3
import random
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "super_secret_key_2026"

# -------------------------
# DATABASE INIT
# -------------------------

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS Joueurs (
        numero TEXT PRIMARY KEY,
        score INTEGER DEFAULT 0
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS Gages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        texte TEXT,
        points INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS Historique (
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

    deja = c.execute("SELECT COUNT(*) FROM Gages").fetchone()[0]

    if deja == 0:
        gages = [
            # FUN & RAPIDES - 1 point
            ("Faire un compliment sincère à quelqu’un.", 1),
            ("Faire un check original à 3 personnes.", 1),
            ("Faire une photo drôle avec un inconnu.", 1),
            ("Lancer un “applaudissement général” sans raison.", 1),
            ("Parler avec un accent pendant 5 minutes.", 1),
            ("Faire une pose mannequin pendant 30 secondes.", 1),
            ("Inventer un slogan pour la soirée.", 1),
            ("Faire deviner ton numéro sans le dire.", 1),
            ("Danser 20 secondes sur la musique en cours.", 1),
            ("Faire un selfie avec quelqu’un de plus de 30 ans.", 1),
            ("Faire un selfie avec quelqu’un de moins de 18 ans.", 1),
            ("Dire un souvenir gênant (soft).", 1),
            ("Faire semblant d’être un serveur pendant 3 minutes.", 1),
            ("Imiter un prof du lycée.", 1),
            ("Faire une déclaration dramatique à une chaise.", 1),
            ("Faire un slow imaginaire.", 1),
            ("Changer de place avec quelqu’un au hasard.", 1),
            ("Faire rire quelqu’un en moins de 1 minute.", 1),
            ("Dire “c’est incroyable” 5 fois dans une discussion.", 1),
            ("Donner un surnom à quelqu’un pour la soirée.", 1),

            # SOCIAUX - 2 points
            ("Trouver quelqu’un né le même mois que toi.", 2),
            ("Faire un duo danse improvisé.", 2),
            ("Organiser une mini ola dans la pièce.", 2),
            ("Faire un high five à 10 personnes.", 2),
            ("Convaincre quelqu’un de faire un gage avec toi.", 2),
            ("Faire une photo de groupe improvisée.", 2),
            ("Demander un conseil de vie à un adulte.", 2),
            ("Apprendre un mot d’argot à quelqu’un de plus âgé.", 2),
            ("Complimenter 3 personnes différentes.", 2),
            ("Faire croire que tu annonces quelque chose d’important.", 2),
            ("Lancer un mini concours de pierre-feuille-ciseaux.", 2),
            ("Faire une interview rapide d’un invité.", 2),
            ("Faire dire “18 ans déjà ?!” à quelqu’un.", 2),
            ("Trouver quelqu’un qui porte la même couleur que toi.", 2),
            ("Faire un duo TikTok (même faux).", 2),
            ("Organiser une photo “génération ado vs adultes”.", 2),
            ("Faire un compliment à quelqu’un que tu connais peu.", 2),
            ("Rassembler 5 personnes pour crier “JOYEUX ANNIVERSAIRE”.", 2),

            # DRÔLES - 3 points
            ("Faire un discours de 30 secondes comme si tu étais maire.", 3),
            ("Imiter une star connue.", 3),
            ("Improviser une pub pour la soirée.", 3),
            ("Parler en rimes pendant 2 minutes.", 3),
            ("Faire une entrée dramatique dans la pièce.", 3),
            ("Jouer une scène de film connue.", 3),
            ("Faire semblant d’être le DJ.", 3),
            ("Faire un défilé de mode.", 3),
            ("Faire une déclaration d’amitié publique.", 3),
            ("Parler comme un commentateur sportif.", 3),
            ("Faire semblant d’avoir gagné un Oscar.", 3),
            ("Inventer une histoire absurde sur l’organisateur.", 3),
            ("Faire une danse robot.", 3),
            ("Faire un battle de regard.", 3),
            ("Faire une imitation animale.", 3),
            ("Faire un rap improvisé sur la soirée.", 3),
            ("Raconter la soirée comme si c’était un documentaire.", 3),
            ("Faire semblant d’être un influenceur.", 3),
            ("Jouer une scène romantique avec un objet.", 3),
            ("Faire un discours comme si tu avais 80 ans.", 3),

            # CHALLENGE - 4 points
            ("Faire 10 squats en chantant.", 4),
            ("Deviner 3 chansons au blind test rapide.", 4),
            ("Faire rire 3 personnes différentes.", 4),
            ("Réussir un défi danse imposé.", 4),
            ("Faire un compliment original à 5 personnes.", 4),
            ("Organiser un mini concours express.", 4),
            ("Faire une pyramide humaine (sécurisée).", 4),
            ("Convaincre quelqu’un de chanter avec toi.", 4),
            ("Raconter une anecdote drôle en 30 secondes.", 4),
            ("Faire un battle de danse.", 4),
            ("Garder un accent pendant 10 minutes.", 4),
            ("Réussir un défi “ne pas sourire” 1 minute.", 4),
            ("Faire un discours sérieux… qui finit absurde.", 4),
            ("Faire lever toute la pièce.", 4),
            ("Trouver 3 personnes qui ont déjà travaillé.", 4),
            ("Lancer un chant collectif.", 4),
            ("Faire une pose photo collective originale.", 4),
            ("Inventer un cri de guerre de la soirée.", 4),
            ("Faire un compliment public à un adulte.", 4),
            ("Organiser un mini toast improvisé.", 4),
        ]

        c.executemany(
            "INSERT INTO Gages (texte, points) VALUES (?, ?)",
            gages
        )

        conn.commit()

    conn.close()


init_db()
inserer_gages()

# -------------------------
# DB CONNECTION
# -------------------------

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------
# PAGE 1 - ACCUEIL
# -------------------------

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        numero = request.form.get("numero")

        if not numero:
            return redirect("/")

        session.clear()
        session["numero"] = numero

        conn = get_db()
        joueur = conn.execute(
            "SELECT * FROM Joueurs WHERE numero=?",
            (numero,)
        ).fetchone()

        if not joueur:
            conn.execute(
                "INSERT INTO Joueurs (numero, score) VALUES (?, 0)",
                (numero,)
            )
            conn.commit()

        return redirect("/jeu")

    return render_template("index.html")


# -------------------------
# PAGE 2 - JEU
# -------------------------

@app.route("/jeu")
def jeu():
    numero = session.get("numero")

    if not numero:
        return redirect("/")

    conn = get_db()

    # Tirage gage si aucun en session
    if "gage_id" not in session:
        gages = conn.execute("SELECT * FROM Gages").fetchall()
        gage = random.choice(gages)
        session["gage_id"] = gage["id"]
    else:
        gage = conn.execute(
            "SELECT * FROM Gages WHERE id=?",
            (session["gage_id"],)
        ).fetchone()

    historique = conn.execute("""
        SELECT texte_gage, points FROM Historique
        WHERE numero_joueur=?
    """, (numero,)).fetchall()

    success = request.args.get("success")

    return render_template(
        "jeu.html",
        gage=gage,
        historique=historique,
        success=success
    )


# -------------------------
# VALIDER
# -------------------------

@app.route("/valider", methods=["POST"])
def valider():
    numero = session.get("numero")
    gage_id = session.get("gage_id")

    if not numero or not gage_id:
        return redirect("/")

    conn = get_db()

    gage = conn.execute(
        "SELECT * FROM Gages WHERE id=?",
        (gage_id,)
    ).fetchone()

    joueur = conn.execute(
        "SELECT * FROM Joueurs WHERE numero=?",
        (numero,)
    ).fetchone()

    nouveau_score = joueur["score"] + gage["points"]

    conn.execute(
        "UPDATE Joueurs SET score=? WHERE numero=?",
        (nouveau_score, numero)
    )

    conn.execute(
        "INSERT INTO Historique (numero_joueur, texte_gage, points, date) VALUES (?, ?, ?, ?)",
        (numero, gage["texte"], gage["points"], datetime.now().isoformat())
    )

    conn.commit()

    session.pop("gage_id", None)

    return redirect("/jeu?success=1")


# -------------------------
# NOUVEAU GAGE
# -------------------------

@app.route("/nouveau")
def nouveau():
    session.pop("gage_id", None)
    return redirect("/jeu")


# -------------------------
# LOGOUT
# -------------------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# -------------------------
# CLASSEMENT
# -------------------------

@app.route("/classement")
def classement():
    conn = get_db()

    joueurs = conn.execute("""
        SELECT * FROM Joueurs ORDER BY score DESC
    """).fetchall()

    return render_template("classement.html", joueurs=joueurs)


# -------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
