from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from app import db
from app.models import Shipping, Product  # Import Product model here

shipping_bp = Blueprint('shipping', __name__)

def calculate_total_weight(product_ids):
    total_weight = 0
    products = Product.query.filter(Product.idproduk.in_(product_ids)).all()
    for product in products:
        total_weight += float(product.berat) * product.stok  # Assuming stok is the quantity
    return total_weight

# List all shipping entries
@shipping_bp.route('/')
def list_shippings():
    shippings = Shipping.query.all()
    return render_template('shipping/list.html', shippings=shippings)

# Update shipping information
@shipping_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update_shipping(id):
    shipping = Shipping.query.get_or_404(id)

    if request.method == 'POST':
        ongkir = request.form.get('ongkir', type=float)  # Convert to float for price
        resi = request.form.get('resi')

        # Validasi input
        if ongkir is None or not resi:
            flash('Ongkir and Resi are required!', 'error')
            return redirect(url_for('shipping.update_shipping', id=id))  # Redirect kembali jika ada kesalahan
        
        shipping.ongkir = ongkir
        shipping.resi = resi
        db.session.commit()
        flash('Shipping info updated successfully!', 'success')
        return redirect(url_for('shipping.list_shippings'))

    return render_template('shipping/update.html', shipping=shipping)

# Delete a shipping entry
@shipping_bp.route('/delete/<int:id>', methods=['POST'])
def delete_shipping(id):
    shipping = Shipping.query.get_or_404(id)
    db.session.delete(shipping)
    db.session.commit()
    flash('Shipping info deleted successfully!', 'success')
    return redirect(url_for('shipping.list_shippings'))

@shipping_bp.route('/api/orders/ship', methods=['POST'])
def send_shipping_info():
    data = request.json
    total_weight = calculate_total_weight(data['product_ids'])
    shipping_info = {
        'total_weight': total_weight,
        'address': data['address']
    }

    return jsonify({'message': 'Shipping info sent to distributors successfully.'}), 201

# Endpoint untuk Menerima Harga Jasa Pengiriman
@shipping_bp.route('/api/orders/shipping_cost', methods=['POST'])
def receive_shipping_cost():
    data = request.json
    # Proses biaya pengiriman

    return jsonify({'message': 'Shipping cost received successfully.'}), 200
