"""Inicialização da aplicação Flask."""
from flask import Flask
from app.database import db


def create_app():
    """Factory function para criar a aplicação Flask."""
    app = Flask(__name__)

    # Configuração do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar banco de dados
    db.init_app(app)

    # Criar tabelas
    with app.app_context():
        db.create_all()

    # Registrar blueprints
    from app.routes import task_bp
    app.register_blueprint(task_bp)

    return app
