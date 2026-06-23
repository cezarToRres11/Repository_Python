# Cenário: B - Cinema
from . import db
from .base import ModeloBase


class Ingresso(ModeloBase):
    """Tabela bônus — compra de ingresso para uma sessão."""

    __tablename__ = "ingressos"

    # TODO ALUNO (resolvido): FK sessao_id → aponta para a tabela "sessoes"
    sessao_id = db.Column(db.Integer, db.ForeignKey("sessoes.id"), nullable=False)

    assento = db.Column(db.String(10), nullable=False)          # ex: "A12"
    nome_comprador = db.Column(db.String(120), nullable=False)

    # TODO ALUNO (resolvido): relationship com Sessao
    sessao = db.relationship("Sessao", back_populates="ingressos")
