# Cenário: B - Cinema
from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for

from models import Filme, Sala, Sessao, db

# Blueprint = módulo de rotas do cinema
# "cinema" → apelido usado no url_for('cinema.index')
# url_prefix="/cinema" → todas as rotas deste Blueprint começam com /cinema
cinema_bp = Blueprint("cinema", __name__, url_prefix="/cinema")


@cinema_bp.route("/")
def index():
    # TODO ALUNO (resolvido): buscar todas as sessões com detalhes de filme e sala
    sessoes = Sessao.listar_com_detalhes()
    return render_template("cinema/lista_sessoes.html", sessoes=sessoes)


@cinema_bp.route("/sessao/cadastrar", methods=["GET", "POST"])
def cadastrar_sessao():
    filmes = Filme.listar()
    salas = Sala.listar()

    if request.method == "POST":
        # TODO ALUNO (resolvido): criar Sessao com os dados do formulário
        # request.form["campo"] → pega o valor do <input name="campo"> do HTML
        nova_sessao = Sessao(
            filme_id=int(request.form["filme_id"]),
            sala_id=int(request.form["sala_id"]),
            # datetime-local do HTML chega como "2025-06-20T19:30" → convertemos
            data_hora=datetime.strptime(request.form["data_hora"], "%Y-%m-%dT%H:%M"),
            preco=float(request.form["preco"]),
        )
        db.session.add(nova_sessao)
        db.session.commit()
        # Após salvar, redireciona para a listagem (padrão POST-Redirect-GET)
        return redirect(url_for("cinema.index"))

    return render_template(
        "cinema/formulario_sessao.html",
        filmes=filmes,
        salas=salas,
    )
