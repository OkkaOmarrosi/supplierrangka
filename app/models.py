# app/models.py

from . import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'supplier_rangka_produk'
    idproduk = db.Column(db.Integer, primary_key=True)
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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relasi
    retail = db.relationship('Retail', backref=db.backref('transactions', lazy=True))
    items = db.relationship('TransactionItem', backref='transaction', lazy=True)

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
