# Cenário: B - Cinema
from flask import Blueprint, render_template

from models import Filme, Sala, Sessao

# Blueprint da home — sem url_prefix, então "/" é a raiz do site
dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    return render_template(
        "index.html",
        total_filmes=Filme.query.count(),
        total_salas=Sala.query.count(),
        total_sessoes=Sessao.query.count(),
    )
