"""
ATIVIDADE 05 — App Flask CRUD incompleto (desafio final)

Corrija TODOS os TODO ALUNO e rode:
  python 05_corrigir_app_completo.py

Abra http://127.0.0.1:5000/ e teste listar, cadastrar, editar e excluir.

Templates na pasta templates/ (também há um erro no HTML).
"""

import os

# Adicionado url_for que faltava para os redirects funcionarem
from flask import Flask, redirect, render_template, request, url_for

# TODO ALUNO: importe SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
pasta = os.path.abspath(os.path.dirname(__file__))

# TODO ALUNO: URI do banco SQLite (arquivo exercicio05.db nesta pasta)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(pasta, "exercicio05.db")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# TODO ALUNO: crie db
db = SQLAlchemy(app)


class Aluno(db.Model):
    __tablename__ = "alunos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    # TODO ALUNO: falta a coluna email
    email = db.Column(db.String(120), nullable=False)


# TODO ALUNO: criar tabelas ao iniciar
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    # TODO ALUNO: busque todos os alunos
    alunos = Aluno.query.order_by(Aluno.nome).all()
    return render_template("lista.html", alunos=alunos)


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        if nome and email:
            aluno = Aluno(nome=nome, email=email)
            db.session.add(aluno)
            # TODO ALUNO: falta commit
            db.session.commit()
            return redirect(url_for("index"))
    return render_template("formulario.html", titulo="Cadastrar aluno")


@app.route("/editar/<int:aluno_id>", methods=["GET", "POST"])
def editar(aluno_id):
    # TODO ALUNO: busque o aluno (db.session.get)
    aluno = db.session.get(Aluno, aluno_id)
    if not aluno:
        return redirect(url_for("index"))

    if request.method == "POST":
        aluno.nome = request.form.get("nome", "").strip()
        aluno.email = request.form.get("email", "").strip()
        db.session.commit()
        return redirect(url_for("index"))

    return render_template(
        "formulario.html",
        titulo="Editar aluno",s
        nome=aluno.nome,
        email=aluno.email,
        aluno_id=aluno.id,
    )


@app.route("/excluir/<int:aluno_id>", methods=["POST"])
def excluir(aluno_id):
    aluno = db.session.get(Aluno, aluno_id)
    if aluno:
        # TODO ALUNO: delete + commit (duas linhas)
        db.session.delete(aluno)
        db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
