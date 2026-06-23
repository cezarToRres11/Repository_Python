# Cenário: B - Cinema
# Aqui nasce o "db" — é ele que conversa com o arquivo .db do SQLite.
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# O PONTO (.) no import = "pega da MESMA pasta models/"
# Ex.: from .filme = arquivo filme.py que está do seu lado, no mesmo apartamento.
# Já no controller a gente usa "from models import Filme" (sem ponto) porque olhamos de FORA.
from .base import ModeloBase
from .filme import Filme
from .sala import Sala
from .sessao import Sessao
from .ingresso import Ingresso

__all__ = ["db", "ModeloBase", "Filme", "Sala", "Sessao", "Ingresso"]
