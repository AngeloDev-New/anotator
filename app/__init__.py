from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configurações básicas
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'

    # Importa e registra as rotas
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
