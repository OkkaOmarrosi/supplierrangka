from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from app import db
from app.models import Product

stock_bp = Blueprint('stock', __name__)

# List all products for stock management
@stock_bp.route('/stocks')
def list_stocks():
    products = Product.query.all()
    return render_template('stock/list.html', products=products)

# Update product stock
@stock_bp.route('/stock/update/<int:id>', methods=['GET', 'POST'])
def update_stock(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        try:
            new_stock = request.form.get('stok', type=int)  # Convert to integer
            if new_stock is None or new_stock < 0:
                flash('Invalid stock value! Please enter a valid stock quantity.', 'error')
                return redirect(url_for('stock.update_stock', id=id))  # Redirect back if there's an error
            
            product.stok = new_stock
            db.session.commit()
            flash('Stock updated successfully!', 'success')
            return redirect(url_for('stock.list_stocks'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('stock.update_stock', id=id))

    return render_template('stock/update.html', product=product)

# Delete a product
@stock_bp.route('/stock/delete/<int:id>', methods=['POST'])
def delete_stock(id):
    product = Product.query.get_or_404(id)
    
    # Optional: Check if stock is zero before deleting
    if product.stok > 0:
        flash('Cannot delete product with stock remaining!', 'error')
        return redirect(url_for('stock.list_stocks'))

    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('stock.list_stocks'))

@stock_bp.route('x<int:id>', methods=['GET'])
def get_stock(id):
    product = Product.query.get_or_404(id)
    return jsonify({'idproduk': product.idproduk, 'stok': product.stok}), 200
