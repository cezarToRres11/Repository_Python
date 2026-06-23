# Cenário: B - Cinema
from . import db
from .base import ModeloBase


class Sessao(ModeloBase):
    __tablename__ = "sessoes"

    # TODO ALUNO (resolvido): FK filme_id → aponta para a tabela "filmes", coluna "id"
    # nullable=False → toda sessão PRECISA ter um filme
    filme_id = db.Column(db.Integer, db.ForeignKey("filmes.id"), nullable=False)

    # TODO ALUNO (resolvido): FK sala_id → aponta para a tabela "salas", coluna "id"
    sala_id = db.Column(db.Integer, db.ForeignKey("salas.id"), nullable=False)

    data_hora = db.Column(db.DateTime, nullable=False)
    preco = db.Column(db.Float, nullable=False)

    # TODO ALUNO (resolvido): relationships
    # back_populates="sessoes" → espelho do relationship lá em Filme e Sala
    filme = db.relationship("Filme", back_populates="sessoes")
    sala = db.relationship("Sala", back_populates="sessoes")
    ingressos = db.relationship("Ingresso", back_populates="sessao")

    @classmethod
    def listar_com_detalhes(cls):
        # Retorna sessões mais recentes primeiro (desc = decrescente)
        return cls.query.order_by(cls.data_hora.desc()).all()
