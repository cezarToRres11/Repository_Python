# Cenário: B - Cinema
# Esta pasta controllers/ exporta os Blueprints para o app.py registrar.
from .cinema_controller import cinema_bp
from .dashboard_controller import dashboard_bp

__all__ = ["dashboard_bp", "cinema_bp"]
