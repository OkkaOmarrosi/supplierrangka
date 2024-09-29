from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from app import db
from app.models import Transaction, Retail, TransactionItem, Product  # Import semua model yang diperlukan

order_bp = Blueprint('order', __name__)

# List all orders
@order_bp.route('/orders')
def list_orders():
    orders = Transaction.query.all()
    return render_template('order/list.html', orders=orders)

# View order details
@order_bp.route('/order/<int:id>')
def order_detail(id):
    order = Transaction.query.get_or_404(id)
    items = TransactionItem.query.filter_by(idtransaksi=id).all()
    return render_template('order/detail.html', order=order, items=items)

# Create new order
@order_bp.route('/order/create', methods=['GET', 'POST'])
def create_order():
    products = Product.query.all()

    if request.method == 'POST':
        retailer_id = request.form.get('retail_id')
        total_price = 0
        total_weight = 0
        
        # Create a new Transaction (order)
        new_order = Transaction(idtoko=retailer_id)
        db.session.add(new_order)
        db.session.commit()

        # Process each product in the order
        for product_id in request.form.getlist('product_ids'):
            product = Product.query.get(product_id)
            quantity = int(request.form.get(f'quantity_{product_id}', 0))  # Default ke 0 jika tidak ada
            
            if quantity <= 0:
                flash(f'Quantity for product ID {product_id} must be greater than 0.', 'error')
                return redirect(url_for('order.create_order'))  # Redirect kembali ke form create_order jika ada masalah
            
            price = product.harga * quantity
            weight = product.berat * quantity
            
            # Add items to the order
            new_item = TransactionItem(
                idtransaksi=new_order.idtransaksi,
                idproduk=product.idproduk,
                jumlah=quantity,
                harga=price,
                berat=weight
            )
            db.session.add(new_item)

            # Update total price and weight
            total_price += price
            total_weight += weight

            # Reduce stock after order
            product.stok -= quantity
        
        db.session.commit()  # Commit stock changes after the loop

        # Update the order with total price and weight
        new_order.totalharga = total_price
        new_order.totalberat = total_weight
        db.session.commit()

        flash('Order created successfully!', 'success')
        return redirect(url_for('order.list_orders'))

    return render_template('order/create.html', products=products)

# Delete an order
@order_bp.route('/order/delete/<int:id>', methods=['POST'])
def delete_order(id):
    order = Transaction.query.get_or_404(id)
    
    # Check if order can be deleted based on your business logic
    if order.status == 'confirmed':
        flash('Cannot delete a confirmed order!', 'error')
        return redirect(url_for('order.list_orders'))

    db.session.delete(order)
    db.session.commit()
    flash('Order deleted successfully!', 'success')
    return redirect(url_for('order.list_orders'))

# Confirm an order
@order_bp.route('/order/confirm/<int:id>', methods=['POST'])
def confirm_order(id):
    order = Transaction.query.get_or_404(id)
    order.status = 'confirmed'  # Assuming there's a 'status' field in Transaction model
    db.session.commit()
    flash('Order confirmed successfully!', 'success')
    return redirect(url_for('order.list_orders'))


@order_bp.route('/api/orders/summary/<int:order_id>', methods=['GET'])
def send_order_summary(order_id):
    order = Transaction.query.get_or_404(order_id)  # Ambil pesanan berdasarkan ID

    # Siapkan ringkasan pesanan yang ingin Anda kirimkan
    order_summary = {
        'id': order.idtransaksi,
        'retail_id': order.idretail,
        'total_price': order.totalharga,
        'total_weight': order.totalberat,
        'items': []
    }

    # Tambahkan detail item dari transaksi
    items = TransactionItem.query.filter_by(idtransaksi=order.idtransaksi).all()
    for item in items:
        order_summary['items'].append({
            'product_id': item.idproduk,
            'quantity': item.jumlah,
            'price': item.harga,
            'weight': item.berat
        })

    return jsonify(order_summary)


