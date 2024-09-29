from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Menggunakan pengaturan dari file config.py

    db.init_app(app)  # Inisialisasi db dengan aplikasi Flask

    with app.app_context():
        # Buat semua tabel jika tidak ada
        db.create_all()
        
        # Import models setelah aplikasi dan db diinisialisasi
        from . import models

    # Daftarkan blueprint untuk dashboard
    from .routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)  # Tanpa url_prefix karena ini adalah halaman utama

    # Daftarkan blueprint lainnya
    from .routes.product import product_bp
    from .routes.stock import stock_bp
    from .routes.order import order_bp
    from .routes.shipping import shipping_bp

    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(stock_bp, url_prefix='/stocks')
    app.register_blueprint(order_bp, url_prefix='/orders')
    app.register_blueprint(shipping_bp, url_prefix='/shippings')
    

    return app
