from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from app import db
from app.models import Product

product_bp = Blueprint('product', __name__)

# List all products
@product_bp.route('/products')
def list_products():
    products = Product.query.all()
    return render_template('product/list.html', products=products)

# Create new product
@product_bp.route('/product/new', methods=['GET', 'POST'])
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


@product_bp.route('/product/edit/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    product = Product.query.get_or_404(id)
    
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
            return redirect(url_for('product.update_product', id=id))
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('product.list_products'))
    
    return render_template('product/update.html', product=product)

@product_bp.route('/product/<int:idproduk>', methods=['GET'])
def product_detail(idproduk):
    # Get the product by ID, or return 404 if not found
    product = Product.query.get_or_404(idproduk)
    return render_template('product/detail.html', product=product)


# Delete product
@product_bp.route('/product/delete/<int:id>', methods=['POST'])  # Use POST method for deletion
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('product.list_products'))

# Endpoint untuk Mengambil Informasi Produk
@product_bp.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'idproduk': p.idproduk,
        'namaproduk': p.namaproduk,
        'kategori': p.kategori,
        'harga': str(p.harga),
        'stok': p.stok,
        'deskripsi': p.deskripsi,
        'linkgambar': p.linkgambar
    } for p in products])