# Cenário: B - Cinema
from . import db
from .base import ModeloBase


class Sala(ModeloBase):
    __tablename__ = "salas"

    numero = db.Column(db.Integer, nullable=False, unique=True)
    capacidade = db.Column(db.Integer, nullable=False)

    # TODO ALUNO (resolvido): relationship — uma Sala tem várias Sessoes
    sessoes = db.relationship("Sessao", back_populates="sala")

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.numero).all()
