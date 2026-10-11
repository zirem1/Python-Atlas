from flask import Flask
from flask_cors import CORS

from config import Config
from app.database import init_db
from app.routes import main


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Wix gibi farklı adreslerden API isteklerine izin verir.
    CORS(app)

    # API adreslerini uygulamaya kaydeder.
    app.register_blueprint(main)

    # Veritabanı tablosunu oluşturur.
    with app.app_context():
        init_db()

    return app
