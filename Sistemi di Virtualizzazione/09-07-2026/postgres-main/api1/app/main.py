from fastapi import FastAPI
import psycopg2
import time

SERVER_NAME = "api1"

app = FastAPI()

db = None

while db is None:
    try:
        db = psycopg2.connect(
            host="postgres",
            database="repository",
            user="admin",
            password="admin"
        )
    except:
        print("Attendo PostgreSQL...")
        time.sleep(2)

cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS utenti (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
)
""")

db.commit()


@app.get("/")
def home():
    return {
        "server": SERVER_NAME,
        "msg": "API pronta"
    }


@app.get("/add/{nome}")
def add(nome: str):

    cur = db.cursor()

    cur.execute(
        "INSERT INTO utenti (nome) VALUES (%s)",
        (nome,)
    )

    db.commit()

    return {
        "server": SERVER_NAME,
        "msg": f"{nome} aggiunto"
    }


@app.get("/lista")
def lista():

    cur = db.cursor()

    cur.execute(
        "SELECT * FROM utenti"
    )

    utenti = cur.fetchall()

    return {
        "server": SERVER_NAME,
        "utenti": utenti
    }