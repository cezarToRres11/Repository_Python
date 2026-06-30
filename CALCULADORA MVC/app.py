import os
from flask import Flask
from controllers import calculadora_bp
from models import Operacao, db


def criar_app():
    # Ajustado para apontar para as pastas reais da sua raiz
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="css",  # Aponta direto para a sua pasta 'css' atual
        static_url_path="/css"
    )

    pasta_aula = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        pasta_aula, "calculadora.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(calculadora_bp)

    with app.app_context():
        db.create_all()

    return app


app = criar_app()

# Corrigido o dunder-name com dois sublinhados iniciais
if __name__ == "__main__":
    app.run(debug=True)
