# Cenário: B - Cinema
from . import db
from .base import ModeloBase


class Filme(ModeloBase):
    __tablename__ = "filmes"

    titulo = db.Column(db.String(150), nullable=False)

    # TODO ALUNO (resolvido): campos adicionais do filme
    duracao_min = db.Column(db.Integer, nullable=False)       # ex: 181
    classificacao = db.Column(db.String(5), nullable=False)   # ex: "12", "L", "16"

    # TODO ALUNO (resolvido): relationship — um Filme tem várias Sessoes
    # back_populates="filme" conecta com o campo "filme" lá em Sessao
    sessoes = db.relationship("Sessao", back_populates="filme")

    @classmethod
    def listar(cls):
        # @classmethod → fala com a CLASSE inteira, não com um objeto específico
        # cls = Filme aqui; retorna todos os filmes em ordem alfabética
        return cls.query.order_by(cls.titulo).all()
