from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def save_to_db(self):
        """Save user to the database."""
        db.session.add(self)
        db.session.commit()

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)

# Buat supplier dummy untuk testing
def seed_data():
    if not Supplier.query.first():
        supplier = Supplier(name="Supplier Jakarta", location="Jakarta")
        db.session.add(supplier)
        db.session.commit()

class Product(db.Model):
    __tablename__ = 'supplier_rangka_produk'
    idproduk = db.Column(db.String(255), primary_key=True)  # Pastikan tipe data sesuai
    namaproduk = db.Column(db.String(255), nullable=False)
    kategori = db.Column(db.Enum('frame', 'fork', 'stang'), nullable=False)
    linkgambar = db.Column(db.String(255))
    stok = db.Column(db.Integer, nullable=False)
    harga = db.Column(db.Numeric(10, 2), nullable=False)
    deskripsi = db.Column(db.Text)
    berat = db.Column(db.Numeric(5, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Retail(db.Model):
    __tablename__ = 'supplier_rangka_retail'
    idretail = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Transaction(db.Model):
    __tablename__ = 'supplier_rangka_transaksi'
    idtransaksi = db.Column(db.Integer, primary_key=True)
    idretail = db.Column(db.Integer, db.ForeignKey('supplier_rangka_retail.idretail'))
    totalharga = db.Column(db.Numeric(10, 2))
    totalberat = db.Column(db.Numeric(5, 2))
    resi = db.Column(db.String(255))
    namapembeli = db.Column(db.String(255))  
    kota_asal = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    # Relasi dengan tabel Retail
    retail = db.relationship('Retail', backref=db.backref('transactions', lazy=True))

    # Relasi dengan tabel TransactionItem
    items = db.relationship('TransactionItem', backref='transaction', lazy=True)

    def __repr__(self):
        return f'<Transaction {self.idtransaksi}>'
    
class Order(db.Model):
    __tablename__ = 'orders'  # Nama tabel dalam database
    id = db.Column(db.Integer, primary_key=True)  # ID unik untuk setiap order
    id_log = db.Column(db.String, nullable=False)  # ID log yang unik
    kota_asal = db.Column(db.String, nullable=False)  # Kota asal
    kota_tujuan = db.Column(db.String, nullable=False)  # Kota tujuan
    berat = db.Column(db.Float, nullable=False)  # Berat total
    harga_pengiriman = db.Column(db.Float, nullable=False)  # Biaya pengiriman
    lama_pengiriman = db.Column(db.String, nullable=False),  # Lama pengiriman
    no_resi = db.Column(db.VARCHAR(255))

    def __init__(self, id_log, kota_asal, kota_tujuan, berat, harga_pengiriman, lama_pengiriman, no_resi):
        self.id_log = id_log
        self.kota_asal = kota_asal
        self.kota_tujuan = kota_tujuan
        self.berat = berat
        self.harga_pengiriman = harga_pengiriman
        self.lama_pengiriman = lama_pengiriman
        self.no_resi = no_resi

class TransactionItem(db.Model):
    __tablename__ = 'supplier_rangka_transaksi_barang'
    idtransaksibarang = db.Column(db.Integer, primary_key=True)
    idtransaksi = db.Column(db.Integer, db.ForeignKey('supplier_rangka_transaksi.idtransaksi'))
    idproduk = db.Column(db.Integer, db.ForeignKey('supplier_rangka_produk.idproduk'))
    jumlah = db.Column(db.Integer, nullable=False)
    harga = db.Column(db.Numeric(10, 2))
    berat = db.Column(db.Numeric(5, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relasi
    product = db.relationship('Product', backref=db.backref('transaction_items', lazy=True))

class Shipping(db.Model):
    __tablename__ = 'supplier_rangka_pengirimanbarang'
    idpengiriman = db.Column(db.Integer, primary_key=True)
    idorder = db.Column(db.Integer, db.ForeignKey('supplier_rangka_transaksi.idtransaksi'))
    ongkir = db.Column(db.Numeric(10, 2))
    resi = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relasi
    transaction = db.relationship('Transaction', backref=db.backref('shipping', uselist=False))
