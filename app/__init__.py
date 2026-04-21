"""Inicialização da aplicação Flask."""
import os
from flask import Flask
from app.database import db


def create_app():
    """Factory function para criar a aplicação Flask."""
    app = Flask(__name__)

    # Definir caminho base
    base_dir = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(os.path.dirname(base_dir), 'data')

    # Criar pasta data se não existir
    os.makedirs(data_dir, exist_ok=True)

    # Configuração do banco de dados
    db_path = os.path.join(data_dir, 'tasks.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar banco de dados
    db.init_app(app)

    # Registrar blueprints (importa modelos também)
    from app.routes import task_bp
    app.register_blueprint(task_bp)

    # Criar tabelas
    with app.app_context():
        print(f'📊 Criando tabelas no banco de dados: {db_path}')
        db.create_all()
        print('✅ Tabelas criadas com sucesso!')

    return app
