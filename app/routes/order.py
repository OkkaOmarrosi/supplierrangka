from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models import Transaction, TransactionItem, Product
import requests

order_bp = Blueprint('order', __name__)

# List all orders (for internal use)
@order_bp.route('/orders')
def list_orders():
    orders = Transaction.query.all()
    return render_template('order/list.html', orders=orders)

# View order details (for internal use)
@order_bp.route('/order/<int:id>')
def order_detail(id):
    order = Transaction.query.get_or_404(id)
    items = TransactionItem.query.filter_by(idtransaksi=id).all()
    return render_template('order/detail.html', order=order, items=items)

# API Retailer untuk membuat pesanan (dikirim ke Supplier)
@order_bp.route('/api/order', methods=['POST'])
def create_order_api():
    data = request.json

    # Validasi data yang diterima
    retailer_id = data.get('retail_id')
    alamat_retailer = data.get('alamat_retailer')
    namapembeli = data.get('namapembeli')
    products_data = data.get('products')
    total_price = data.get('total_price')  # Retailer sudah menghitung total harga

    if not retailer_id or not namapembeli or not products_data or total_price is None:
        return jsonify({'error': 'Missing required fields'}), 400

    total_weight = 0
    products_not_found = []

    try:
        # Proses order baru
        new_order = Transaction(
            idretail=retailer_id,
            totalharga=total_price,  # Menggunakan total harga dari retailer
            totalberat=0,  # Placeholder, akan diupdate nanti
            resi=None,  
            namapembeli=namapembeli  
        )
        
        db.session.add(new_order)
        db.session.commit()  # Commit to get new_order.idtransaksi
        
        # Proses setiap produk dalam pesanan
        for product_data in products_data:
            product_id = product_data.get('product_id')
            quantity = product_data.get('quantity')

            product = Product.query.get(product_id)

            if product is None:
                products_not_found.append(product_id)
                continue  # Skip this product and continue with the next

            if product.stok < quantity:
                return jsonify({'error': f'Not enough stock for {product.namaproduk}'}), 400

            weight = product.berat * quantity

            # Tambahkan item ke pesanan
            new_item = TransactionItem(
                idtransaksi=new_order.idtransaksi,
                idproduk=product_id,
                jumlah=quantity,
                harga=product.harga * quantity,
                berat=weight
            )
            
            total_weight += weight

            # Kurangi stok setelah pesanan dibuat
            product.stok -= quantity
            db.session.add(new_item)

        # Update berat total di order
        new_order.totalberat = total_weight
        db.session.commit()

        # Jika ada produk yang tidak ditemukan
        if products_not_found:
            return jsonify({'error': f'Products with IDs {products_not_found} not found'}), 404

        # Kirim data ke distributor untuk cek ongkos kirim
        distributor_response = cek_ongkir_ke_distributor(new_order.idtransaksi, total_weight)

        # Update transaksi dengan data dari distributor
        new_order.id_log = distributor_response.get('id_log')
        new_order.harga_pengiriman = distributor_response.get('harga_pengiriman')
        new_order.lama_pengiriman = distributor_response.get('lama_pengiriman')
        new_order.resi = distributor_response.get('no_resi')
        db.session.commit()

        return jsonify({
            'order_id': new_order.idtransaksi,
            'id_log': new_order.id_log,
            'harga_pengiriman': new_order.harga_pengiriman,
            'lama_pengiriman': new_order.lama_pengiriman,
            'no_resi': new_order.resi
        }), 201

    except Exception as e:
        db.session.rollback()  # Rollback jika ada kesalahan
        return jsonify({'error': str(e)}), 500

def cek_ongkir_ke_distributor(order_id, total_weight):
    """
    Mengirimkan permintaan ke distributor untuk cek ongkos kirim.
    URL Distributor: http://159.223.41.243:8000/api/distributors6/orders/cek_ongkir
    """
    kota_asal = "Jakarta"  # Kota asal supplier
    url = "http://159.223.41.243:8000/api/distributors6/orders/cek_ongkir"
    
    payload = {
        "order_id": order_id,
        "total_weight": total_weight,
        "kota_asal": "Jakarta"  # Mengirimkan kota asal ke distributor
    }

    try:
        response = requests.post(url, json=payload)
        response_data = response.json()

        # Pastikan respons valid
        if response.status_code == 200:
            return {
                "harga_pengiriman": response_data.get("harga_pengiriman"),
                "id_log": response_data.get("id_log"),
                "lama_pengiriman": response_data.get("lama_pengiriman"),
                "no_resi": response_data.get("no_resi"),
                "tanggal_pembelian": response_data.get("tanggal_pembelian")
            }
        else:
            raise Exception("Failed to get shipping data from distributor.")
    
    except Exception as e:
        raise Exception(f"Error connecting to distributor: {str(e)}")

# API untuk menampilkan detail pesanan ke distributor
@order_bp.route('/api/order/summary/<int:order_id>', methods=['GET'])
def send_order_summary(order_id):
    order = Transaction.query.get_or_404(order_id)
    items = TransactionItem.query.filter_by(idtransaksi=order.idtransaksi).all()

    order_summary = {
        'order_id': order.idtransaksi,
        'resi': order.resi,
        'namapembeli': order.namapembeli,
        'total_price': order.totalharga,
        'total_weight': order.totalberat,
        'items': []
    }

    for item in items:
        product = Product.query.get(item.idproduk)
        order_summary['items'].append({
            'product_id': item.idproduk,
            'nama_barang': product.namaproduk,  # Tampilkan nama barang
            'quantity': item.jumlah,
            'price': item.harga,
            'weight': item.berat
        })

    return jsonify(order_summary)
