"""
ATIVIDADE 02 — Model (tabela Aluno)

Corrija a classe Aluno e a criação da tabela.
Execute: python 02_corrigir_model.py
"""

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
pasta = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(pasta, "exercicio.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# TODO ALUNO: a classe deve herdar de db.Model
class Aluno(db.Model):
    # TODO ALUNO: defina o nome da tabela
    __tablename__ = "alunos"

    # TODO ALUNO: id inteiro, chave primária
    id = db.Column(db.Integer, primary_key=True)

    # TODO ALUNO: coluna nome (String 100, obrigatório)
    nome = db.Column(db.String(100), nullable=False)

    # TODO ALUNO: coluna email (String 120, obrigatório)
    email = db.Column(db.String(120), nullable=False)


with app.app_context():
    # TODO ALUNO: chame o método que CRIA as tabelas no banco
    db.create_all()


if __name__ == "__main__":
    with app.app_context():
        print("Tabelas:", db.metadata.tables.keys())
        # Deve mostrar dict_keys(['alunos'])
        aluno_teste = Aluno(nome="Teste", email="teste@mail.com")
        db.session.add(aluno_teste)
        # TODO ALUNO: falta confirmar gravação no banco
        db.session.commit()
        print("Aluno inserido:", aluno_teste)
