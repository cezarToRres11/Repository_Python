from flask import Blueprint, redirect, render_template, request, url_for

from models import Colecionador, Figurinha, ItemOferta, OfertaTroca, db

figurinhas_bp = Blueprint("figurinhas", __name__, url_prefix="/figurinhas")


@figurinhas_bp.route("/")
def index():
    ofertas = OfertaTroca.listar_com_colecionador()
    return render_template("figurinhas/lista_ofertas.html", ofertas=ofertas)


@figurinhas_bp.route("/oferta/cadastrar", methods=["GET", "POST"])
def cadastrar_oferta():
    colecionadores = Colecionador.listar()
    figurinhas = Figurinha.listar()

    if request.method == "POST":
        oferta = OfertaTroca(
            colecionador_id=int(request.form["colecionador_id"]),
            observacao=request.form.get("observacao", "").strip(),
        )
        db.session.add(oferta)
        db.session.flush()

        item_oferece = ItemOferta(
            oferta_id=oferta.id,
            figurinha_id=int(request.form["figurinha_oferece_id"]),
            tipo="oferece",
            quantidade=1,
        )
        item_deseja = ItemOferta(
            oferta_id=oferta.id,
            figurinha_id=int(request.form["figurinha_deseja_id"]),
            tipo="deseja",
            quantidade=1,
        )
        db.session.add_all([item_oferece, item_deseja])
        db.session.commit()
        return redirect(url_for("figurinhas.index"))

    return render_template(
        "figurinhas/formulario_oferta.html",
        colecionadores=colecionadores,
        figurinhas=figurinhas,
    )
