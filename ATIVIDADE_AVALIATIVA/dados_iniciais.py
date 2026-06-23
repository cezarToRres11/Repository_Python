# Cenário: B - Cinema
from models import Filme, Sala, db


def popular_dados():
    # Só insere se o banco estiver vazio — evita duplicatas ao reiniciar
    if Filme.query.count() > 0:
        return

    filmes = [
        Filme(titulo="Vingadores: Ultimato", duracao_min=181, classificacao="12"),
        Filme(titulo="Divertidamente 2", duracao_min=96, classificacao="L"),
        Filme(titulo="Duna: Parte 2", duracao_min=166, classificacao="12"),
    ]
    salas = [
        Sala(numero=1, capacidade=120),
        Sala(numero=2, capacidade=80),
        Sala(numero=3, capacidade=200),
    ]
    db.session.add_all(filmes + salas)
    db.session.commit()
