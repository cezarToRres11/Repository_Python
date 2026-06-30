"""
ATIVIDADE 01 — Configuração Flask + SQLAlchemy

Corrija este arquivo até rodar sem erro:
  python 01_corrigir_configuracao.py

Saída esperada: "Configuração OK! Banco: sqlite:///..."
"""

import os

from flask import Flask

# TODO ALUNO: importe SQLAlchemy de flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

pasta = os.path.abspath(os.path.dirname(__file__))

# TODO ALUNO: complete a chave de configuração (nome correto da setting)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(pasta, "exercicio.db")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# TODO ALUNO: crie o objeto db ligado ao app
db = SQLAlchemy(app)


if __name__ == "__main__":
    # TODO ALUNO: descomente as 2 linhas abaixo após corrigir db e config
    print("Configuração OK! Banco:", app.config["SQLALCHEMY_DATABASE_URI"])
    print("Objeto db:", db)
  