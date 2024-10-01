from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Menggunakan pengaturan dari file config.py

    db.init_app(app)  # Inisialisasi db dengan aplikasi Flask
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Set default route ke halaman login

    with app.app_context():
        db.create_all()
    # Import models setelah aplikasi dan db diinisialisasi
    from . import models

    # Import dan daftarkan blueprint untuk login
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    # Import blueprint lainnya untuk halaman dashboard dan lainnya
    from .routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from .routes.product import product_bp
    from .routes.stock import stock_bp
    from .routes.order import order_bp
    from .routes.shipping import shipping_bp
    from .routes.distributor import distributor_bp
    from .routes.retailer import retailer_bp
    from .routes.api import api_bp

    # Dapatkan daftar blueprint yang ingin didaftarkan dengan prefix
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(stock_bp, url_prefix='/stocks')
    app.register_blueprint(order_bp, url_prefix='/orders')
    app.register_blueprint(shipping_bp, url_prefix='/shippings')
    app.register_blueprint(distributor_bp)  # Pastikan prefix sesuai
    app.register_blueprint(api_bp, url_prefix='/api')   # Pastikan prefix sesuai

    # Arahkan root URL ke halaman login jika belum login
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app
