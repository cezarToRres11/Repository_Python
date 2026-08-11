import os
import sqlite3
from functools import wraps

import requests
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "banco.db")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao")
app.config["DEBUG"] = os.environ.get("DEBUG", "False").lower() == "true"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT NOT NULL DEFAULT 'Pendente',
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view


def get_current_user():
    if "usuario_id" not in session:
        return None

    conn = get_db()
    user = conn.execute(
        "SELECT id, nome, email FROM usuarios WHERE id = ?",
        (session["usuario_id"],)
    ).fetchone()
    conn.close()
    return user


@app.context_processor
def inject_user():
    return {"current_user": get_current_user()}


@app.route("/")
def index():
    if "usuario_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        if not nome or not email or not senha:
            return render_template(
                "cadastro.html",
                erro="Preencha todos os campos."
            )

        if len(senha) < 6:
            return render_template(
                "cadastro.html",
                erro="A senha precisa ter pelo menos 6 caracteres."
            )

        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                (nome, email, generate_password_hash(senha))
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return render_template(
                "cadastro.html",
                erro="Este e-mail já está cadastrado."
            )

        conn.close()
        return redirect(url_for("login"))

    return render_template("cadastro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM usuarios WHERE email = ?",
            (email,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["senha"], senha):
            session.clear()
            session["usuario_id"] = user["id"]
            session["usuario_nome"] = user["nome"]
            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            erro="E-mail ou senha incorretos."
        )

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db()
    tarefas = conn.execute(
        """
        SELECT id, titulo, descricao, status
        FROM tarefas
        WHERE usuario_id = ?
        ORDER BY id DESC
        """,
        (session["usuario_id"],)
    ).fetchall()
    conn.close()

    return render_template("dashboard.html", tarefas=tarefas)


@app.route("/nova_tarefa", methods=["GET", "POST"])
@login_required
def nova_tarefa():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        status = request.form.get("status", "Pendente")

        if status not in ("Pendente", "Em andamento", "Concluída"):
            status = "Pendente"

        if not titulo:
            return render_template(
                "nova_tarefa.html",
                erro="O título é obrigatório."
            )

        conn = get_db()
        conn.execute(
            """
            INSERT INTO tarefas (titulo, descricao, status, usuario_id)
            VALUES (?, ?, ?, ?)
            """,
            (titulo, descricao, status, session["usuario_id"])
        )
        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("nova_tarefa.html")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    conn = get_db()
    tarefa = conn.execute(
        """
        SELECT *
        FROM tarefas
        WHERE id = ? AND usuario_id = ?
        """,
        (id, session["usuario_id"])
    ).fetchone()

    if tarefa is None:
        conn.close()
        return "Tarefa não encontrada.", 404

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        status = request.form.get("status", "Pendente")

        if status not in ("Pendente", "Em andamento", "Concluída"):
            status = "Pendente"

        if not titulo:
            conn.close()
            return render_template(
                "editar.html",
                tarefa=tarefa,
                erro="O título é obrigatório."
            )

        conn.execute(
            """
            UPDATE tarefas
            SET titulo = ?, descricao = ?, status = ?
            WHERE id = ? AND usuario_id = ?
            """,
            (
                titulo,
                descricao,
                status,
                id,
                session["usuario_id"]
            )
        )
        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    conn.close()
    return render_template("editar.html", tarefa=tarefa)


@app.post("/excluir/<int:id>")
@login_required
def excluir(id):
    conn = get_db()
    conn.execute(
        "DELETE FROM tarefas WHERE id = ? AND usuario_id = ?",
        (id, session["usuario_id"])
    )
    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


@app.get("/api/tarefas")
@login_required
def api_tarefas():
    status = request.args.get("status", "").strip()

    conn = get_db()

    if status in ("Pendente", "Em andamento", "Concluída"):
        tarefas = conn.execute(
            """
            SELECT id, titulo, descricao, status
            FROM tarefas
            WHERE usuario_id = ? AND status = ?
            ORDER BY id DESC
            """,
            (session["usuario_id"], status)
        ).fetchall()
    else:
        tarefas = conn.execute(
            """
            SELECT id, titulo, descricao, status
            FROM tarefas
            WHERE usuario_id = ?
            ORDER BY id DESC
            """,
            (session["usuario_id"],)
        ).fetchall()

    conn.close()

    return jsonify([
        {
            "id": tarefa["id"],
            "titulo": tarefa["titulo"],
            "descricao": tarefa["descricao"] or "",
            "status": tarefa["status"]
        }
        for tarefa in tarefas
    ])


@app.get("/api/progresso")
@login_required
def api_progresso():
    conn = get_db()
    rows = conn.execute(
        """
        SELECT status, COUNT(*) AS quantidade
        FROM tarefas
        WHERE usuario_id = ?
        GROUP BY status
        """,
        (session["usuario_id"],)
    ).fetchall()
    conn.close()

    resultado = {
        "Pendente": 0,
        "Em andamento": 0,
        "Concluída": 0
    }

    for row in rows:
        resultado[row["status"]] = row["quantidade"]

    return jsonify(resultado)


@app.get("/progresso")
@login_required
def progresso():
    return render_template("progresso.html")


@app.get("/api/frase")
@login_required
def api_frase():
    try:
        resposta = requests.get(
            "https://api.adviceslip.com/advice",
            timeout=5
        )
        resposta.raise_for_status()
        return jsonify(resposta.json())
    except requests.RequestException:
        return jsonify({
            "slip": {
                "advice": "Continue avançando. Pequenos passos também são progresso."
            }
        })


if __name__ == "__main__":
    init_db()
    app.run()
