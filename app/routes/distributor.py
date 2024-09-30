import requests
from flask import Blueprint, jsonify, request
import uuid
from app.models import Order
from app import db

distributor_bp = Blueprint('distributor', __name__)

BASE_DISTRIBUTOR_API = "http://159.223.41.243:8000/api/distributors6/orders/cek_ongkir"
BASE_CONFIRM_ORDER_API = "http://167.99.238.114:8000/place_order"

@distributor_bp.route('/api/supplier/cek_harga', methods=['POST'])
def cek_harga():
    print("Received request for cek_harga")  # Tambahkan log ini
    data = request.json
    cart = data['cart']
    print(cart)
    # transaction_id = data.get('transaction_id')
    total_berat_barang = data.get('total_berat_barang')
    kota_tujuan = data.get('kota_tujuan')

    # if not cart or not transaction_id or total_berat_barang is None or not kota_tujuan:
    #     return jsonify({"error": "Missing required parameters"}), 400

    id_log = str(uuid.uuid1())
    kota_asal = "Semarang"

    try:
        distributor_response = requests.post(BASE_DISTRIBUTOR_API, json={
            "id_log": id_log,
            "kota_asal": kota_asal,
            "kota_tujuan": kota_tujuan,
            "berat": total_berat_barang
        })

        if distributor_response.status_code == 200:
            ongkir_data = distributor_response.json()
            harga_pengiriman = ongkir_data.get("harga_pengiriman")
            lama_pengiriman = ongkir_data.get("lama_pengiriman")

                    # Menyimpan data pesanan ke database
            new_order = Order(
                id_log=id_log,
                kota_asal=kota_asal,
                kota_tujuan=kota_tujuan,
                berat=total_berat_barang,
                harga_pengiriman=harga_pengiriman,
                lama_pengiriman=lama_pengiriman
            )
            db.session.add(new_order)  # Menambahkan objek Order ke session
            db.session.commit()  # Menyimpan perubahan ke database

            if harga_pengiriman is None or lama_pengiriman is None:
                return jsonify({"error": "Invalid response data from distributor"}), 500

            return jsonify({
                "harga_pengiriman": harga_pengiriman,
                "transaction_id": id_log,
                "lama_pengiriman": lama_pengiriman
            }), 200
        else:
            return jsonify({
                "error": "Failed to check shipping price from distributor",
                "details": distributor_response.text
            }), distributor_response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error connecting to distributor: {str(e)}"}), 500

