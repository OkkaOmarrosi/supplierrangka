from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from app import db
from app.models import Product
from datetime import datetime  # Pastikan datetime diimpor

product_bp = Blueprint('product', __name__)

# Fungsi untuk menghasilkan id produk unik
def generate_unique_id():
    latest_product = Product.query.order_by(Product.idproduk.desc()).first()
    if latest_product:
        try:
            last_number = int(latest_product.idproduk.split('-')[0])
            new_number = last_number + 1
        except (IndexError, ValueError):
            new_number = 10  # Jika format id tidak sesuai, mulai dari 10
    else:
        new_number = 10  # Mulai dari 10 jika tidak ada produk sebelumnya
    return f"{new_number}-PRO"

# List all products
@product_bp.route('/', methods=['GET'])
def list_products():
    products = Product.query.all()
    print(products)  # Untuk cek di terminal apakah data diambil
    return render_template('product/list.html', products=products)

# Detail product (untuk menampilkan detail produk)
@product_bp.route('/<string:idproduk>', methods=['GET'])
def product_detail(idproduk):
    product = Product.query.get_or_404(idproduk)
    return render_template('product/detail.html', product=product)

# Create new product
@product_bp.route('/new', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        namaproduk = request.form.get('namaproduk')
        kategori = request.form.get('kategori')
        linkgambar = request.form.get('linkgambar')
        stok = request.form.get('stok', type=int)
        harga = request.form.get('harga', type=float)
        deskripsi = request.form.get('deskripsi')
        berat = request.form.get('berat', type=float)

        # Validasi input
        if not namaproduk or not kategori or stok is None or harga is None:
            flash('All fields are required!', 'error')
            return redirect(url_for('product.create_product')) 

        new_product = Product(
            idproduk=generate_unique_id(),  # Menghasilkan ID unik
            namaproduk=namaproduk,
            kategori=kategori,
            linkgambar=linkgambar,
            stok=stok,
            harga=harga,
            deskripsi=deskripsi,
            berat=berat
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product created successfully!', 'success')
        return redirect(url_for('product.list_products'))

    return render_template('product/create.html')

# Update product
@product_bp.route('/edit/<string:idproduk>', methods=['GET', 'POST']) 
def update_product(idproduk):
    product = Product.query.get_or_404(idproduk)
    
    if request.method == 'POST':
        product.namaproduk = request.form.get('namaproduk')
        product.kategori = request.form.get('kategori')
        product.linkgambar = request.form.get('linkgambar')
        product.stok = request.form.get('stok', type=int)
        product.harga = request.form.get('harga', type=float)
        product.deskripsi = request.form.get('deskripsi')
        product.berat = request.form.get('berat', type=float)

        # Validasi input
        if not product.namaproduk or not product.kategori or product.stok is None or product.harga is None:
            flash('All fields are required!', 'error')
            return redirect(url_for('product.update_product', idproduk=idproduk))
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('product.list_products'))
    
    return render_template('product/update.html', product=product)

# Delete product
@product_bp.route('/delete/<string:idproduk>', methods=['POST'])  # Ubah tipe ke string
def delete_product(idproduk):
    product = Product.query.get_or_404(idproduk)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('product.list_products'))

# Endpoint untuk Mengambil Informasi Produk
@product_bp.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    
    return jsonify([{
        'id_produk': p.idproduk,
        'nama_produk': p.namaproduk,
        'harga': str(p.harga),
        'stock': p.stok,
        'berat': p.berat,
        'linkgambar': p.linkgambar
    } for p in products])
