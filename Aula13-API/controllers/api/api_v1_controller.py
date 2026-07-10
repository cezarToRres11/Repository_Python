from flask import Blueprint, jsonify, request

from models import Colecionador, Figurinha, ItemOferta, OfertaTroca, db
from services import buscar_pokemon

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")


@api_v1_bp.route("/ofertas", methods=["GET"])
def api_listar_ofertas():
    ofertas = OfertaTroca.listar_com_colecionador()
    return jsonify([
        {
            "id": o.id,
            "colecionador": o.colecionador.apelido,
            "observacao": o.observacao,
            "itens": [
                {
                    "figurinha": item.figurinha.nome_jogador,
                    "numero": item.figurinha.numero,
                    "tipo": item.tipo,
                    "quantidade": item.quantidade,
                }
                for item in o.itens
            ],
        }
        for o in ofertas
    ])


@api_v1_bp.route("/ofertas/<int:oferta_id>", methods=["GET"])
def api_detalhe_oferta(oferta_id):
    oferta = db.session.get(OfertaTroca, oferta_id)
    if not oferta:
        return jsonify({"erro": "Oferta não encontrada"}), 404
    return jsonify({
        "id": oferta.id,
        "colecionador": oferta.colecionador.apelido,
        "observacao": oferta.observacao,
        "itens": [
            {
                "figurinha": item.figurinha.nome_jogador,
                "numero": item.figurinha.numero,
                "tipo": item.tipo,
                "quantidade": item.quantidade,
            }
            for item in oferta.itens
        ],
    })


@api_v1_bp.route("/ofertas", methods=["POST"])
def api_criar_oferta():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Envie JSON no body"}), 400
    try:
        oferta = OfertaTroca(
            colecionador_id=int(dados["colecionador_id"]),
            observacao=str(dados.get("observacao", "")).strip(),
        )
        figurinha_oferece_id = int(dados["figurinha_oferece_id"])
        figurinha_deseja_id = int(dados["figurinha_deseja_id"])
    except (KeyError, ValueError, TypeError):
        return jsonify({
            "erro": "Campos obrigatórios: colecionador_id, figurinha_oferece_id, figurinha_deseja_id",
        }), 400
    db.session.add(oferta)
    db.session.flush()
    db.session.add_all([
        ItemOferta(
            oferta_id=oferta.id,
            figurinha_id=figurinha_oferece_id,
            tipo="oferece",
            quantidade=1,
        ),
        ItemOferta(
            oferta_id=oferta.id,
            figurinha_id=figurinha_deseja_id,
            tipo="deseja",
            quantidade=1,
        ),
    ])
    db.session.commit()
    return jsonify({"id": oferta.id, "mensagem": "Oferta criada"}), 201


@api_v1_bp.route("/ofertas/<int:oferta_id>", methods=["PUT"])
def api_atualizar_oferta(oferta_id):
    oferta = db.session.get(OfertaTroca, oferta_id)
    if not oferta:
        return jsonify({"erro": "Oferta não encontrada"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Envie JSON no body"}), 400

    # Atualiza só o que veio no JSON — o resto fica como estava.
    if "colecionador_id" in dados:
        oferta.colecionador_id = int(dados["colecionador_id"])
    if "observacao" in dados:
        oferta.observacao = str(dados["observacao"]).strip()

    db.session.commit()
    return jsonify({
        "id": oferta.id,
        "colecionador": oferta.colecionador.apelido,
        "observacao": oferta.observacao,
        "itens": [
            {
                "figurinha": item.figurinha.nome_jogador,
                "numero": item.figurinha.numero,
                "tipo": item.tipo,
                "quantidade": item.quantidade,
            }
            for item in oferta.itens
        ],
    })


@api_v1_bp.route("/ofertas/<int:oferta_id>", methods=["DELETE"])
def api_excluir_oferta(oferta_id):
    oferta = db.session.get(OfertaTroca, oferta_id)
    if not oferta:
        return jsonify({"erro": "Oferta não encontrada"}), 404

    db.session.delete(oferta)  # cascade remove os ItemOferta junto
    db.session.commit()
    return "", 204


@api_v1_bp.route("/figurinhas", methods=["GET"])
def api_listar_figurinhas():
    return jsonify([
        {"id": f.id, "numero": f.numero, "nome_jogador": f.nome_jogador, "time": f.time}
        for f in Figurinha.listar()
    ])


@api_v1_bp.route("/colecionadores", methods=["GET"])
def api_listar_colecionadores():
    return jsonify([
        {"id": c.id, "apelido": c.apelido, "cidade": c.cidade}
        for c in Colecionador.listar()
    ])


@api_v1_bp.route("/externo/pokemon", methods=["GET"])
def api_pokemon():
    nome = request.args.get("nome", "pikachu")
    try:
        pokemon = buscar_pokemon(nome)
        return jsonify({"fonte": "PokéAPI", "pokemon": pokemon})
    except Exception:
        return jsonify({"erro": f"Pokémon '{nome}' não encontrado"}), 404


@api_v1_bp.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "API está funcionando"}), 200
