from flask import Flask, render_template, request, redirect
import sqlite3
import random
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Table Joueurs
    c.execute("""
    CREATE TABLE IF NOT EXISTS Joueurs (
        numero TEXT PRIMARY KEY,
        score INTEGER,
        gage_en_cours TEXT,
        etat_gage TEXT
    )
    """)

    # Table Gages
    c.execute("""
    CREATE TABLE IF NOT EXISTS Gages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        texte TEXT,
        points INTEGER,
        actif INTEGER
    )
    """)

    # Table Historique
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

init_db()

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Tirer un gage aléatoire
def tirer_gage(conn):
    gages = conn.execute("SELECT * FROM Gages WHERE actif = 1").fetchall()
    return random.choice(gages)

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()

    if request.method == "POST":
        numero = request.form["numero"]
        nouveau_gage_flag = request.form.get("nouveau_gage")

        # Vérifier si joueur existe
        joueur = conn.execute("SELECT * FROM Joueurs WHERE numero = ?", (numero,)).fetchone()

        if not joueur:
            conn.execute(
                "INSERT INTO Joueurs (numero, score, gage_en_cours, etat_gage) VALUES (?, 0, '', 'aucun')",
                (numero,))
            conn.commit()
            joueur = conn.execute("SELECT * FROM Joueurs WHERE numero = ?", (numero,)).fetchone()

        # Tirer un nouveau gage si le joueur veut juste un nouveau gage
        # ou s'il n'a pas de gage en cours
        if nouveau_gage_flag == "1" or joueur["etat_gage"] != "en_cours":
            gage_random = tirer_gage(conn)
            conn.execute(
                "UPDATE Joueurs SET gage_en_cours = ?, etat_gage = 'en_cours' WHERE numero = ?",
                (gage_random["texte"], numero))
            conn.commit()
            gage = gage_random["texte"]
        else:
            gage = joueur["gage_en_cours"]

        return render_template("index.html", gage=gage, numero=numero)

    return render_template("index.html", gage=None)

@app.route("/valider", methods=["POST"])
def valider():
    conn = get_db()
    numero = request.form["numero"]

    joueur = conn.execute("SELECT * FROM Joueurs WHERE numero = ?", (numero,)).fetchone()
    gage = conn.execute("SELECT * FROM Gages WHERE texte = ?", (joueur["gage_en_cours"],)).fetchone()

    # Ajouter points et marquer gage comme fait
    nouveau_score = joueur["score"] + gage["points"]
    conn.execute(
        "UPDATE Joueurs SET score = ?, etat_gage = 'termine' WHERE numero = ?",
        (nouveau_score, numero))

    # Ajouter à l'historique
    conn.execute(
        "INSERT INTO Historique (numero_joueur, texte_gage, points, date) VALUES (?, ?, ?, ?)",
        (numero, gage["texte"], gage["points"], datetime.now()))

    conn.commit()

    # Tirer un nouveau gage automatiquement
    gage_random = tirer_gage(conn)
    conn.execute(
        "UPDATE Joueurs SET gage_en_cours = ?, etat_gage = 'en_cours' WHERE numero = ?",
        (gage_random["texte"], numero))
    conn.commit()

    return render_template("index.html", gage=gage_random["texte"], numero=numero)

@app.route("/classement")
def classement():
    conn = get_db()
    # Nombre de gages réalisés par joueur
    joueurs = conn.execute("""
        SELECT numero, score, COUNT(Historique.id) AS gages_faits
        FROM Joueurs
        LEFT JOIN Historique ON Joueurs.numero = Historique.numero_joueur
        GROUP BY Joueurs.numero
        ORDER BY score DESC
    """).fetchall()
    return render_template("classement.html", joueurs=joueurs)


