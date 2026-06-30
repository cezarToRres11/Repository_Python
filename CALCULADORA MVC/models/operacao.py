from datetime import datetime
from . import db

class Operacao(db.Model):
    """Model — dados e acesso ao banco (tabela operacoes)."""

    # Correção: O correto é usar dois sublinhados (__tablename__)
    __tablename__ = "operacoes"

    # Declaração das colunas exigidas pelo sistema
    id = db.Column(db.Integer, primary_key=True)
    num1 = db.Column(db.Float, nullable=False)
    num2 = db.Column(db.Float, nullable=True)  # Pode ser nulo no caso de raiz quadrada
    operacao = db.Column(db.String(10), nullable=False)
    etapas = db.Column(db.String(255), nullable=True)
    resultado = db.Column(db.String(100), nullable=False)
    
    # Campo de data e hora solicitado no comentário da linha 11
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def salvar(cls, num1, num2, operacao, etapas, resultado):
        registro = cls(
            num1=num1,
            num2=num2,
            operacao=operacao,
            etapas=etapas,
            resultado=str(resultado),
        )
        # Adicionados os métodos de gravar no banco solicitados na linha 22
        db.session.add(registro)
        db.session.commit()
        return registro

    @classmethod
    def listar_recentes(cls, limite=10):
        return (
            cls.query.order_by(cls.criado_em.desc()).limit(limite).all()
        )

    def __repr__(self):
        return f"<Operacao {self.id}: {self.etapas}>"
