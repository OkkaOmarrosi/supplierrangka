import requests
from flask import Blueprint, jsonify, request
import uuid
from app.models import Order
from app import db

distributor_bp = Blueprint('distributor', __name__)

DISTRIBUTOR_APIS = {
    1: "http://159.223.41.243:8000/api/distributors6/orders/cek_ongkir",
    2: "http://143.244.170.95:8000/api/distributor5/orders/cek_ongkir",
    3: "http://another_distributor_api.com/orders/cek_ongkir"
}

FIX_KIRIM_URL = "http://167.99.238.114:8000/api/place_order"

@distributor_bp.route('/api/supplier/cek_harga', methods=['POST'])
def cek_harga():
    data = request.json
    cart = data.get('cart')
    total_berat_barang = data.get('total_berat_barang')
    kota_tujuan = data.get('kota_tujuan')
    id_retail = data.get('id_retail')
    id_distributor = data.get('id_distributor')

    if not cart or total_berat_barang is None or not kota_tujuan or not id_distributor:
        return jsonify({"error": "Missing required parameters"}), 400

    # ID log unik
    id_log = str(uuid.uuid1())
    kota_asal = "Semarang"

    # Memilih distributor API berdasarkan ID distributor
    distributor_url = DISTRIBUTOR_APIS.get(int(id_distributor))
    if not distributor_url:
        return jsonify({"error": "Invalid distributor ID"}), 400

    try:
        # Mengirim permintaan ke distributor
        distributor_response = requests.post(distributor_url, json={
            "id_log": id_log,
            "kota_asal": kota_asal,
            "kota_tujuan": kota_tujuan,
            "id_retail": id_retail,
            "berat": total_berat_barang
        })

        if distributor_response.status_code == 200:
            ongkir_data = distributor_response.json()
            harga_pengiriman = ongkir_data.get("harga_pengiriman")
            lama_pengiriman = ongkir_data.get("lama_pengiriman")

            # Pastikan data yang diperlukan tersedia
            if harga_pengiriman is None or lama_pengiriman is None:
                return jsonify({"error": "Invalid response data from distributor"}), 500

            # Simpan data pesanan ke dalam database
            new_order = Order(
                id_log=id_log,
                kota_asal=kota_asal,
                kota_tujuan=kota_tujuan,
                berat=total_berat_barang,
                harga_pengiriman=harga_pengiriman,
                lama_pengiriman=lama_pengiriman
            )
            db.session.add(new_order)
            db.session.commit()

            return jsonify({
                "harga_pengiriman": harga_pengiriman,
                "id_log": id_log,
                "lama_pengiriman": lama_pengiriman
            }), 200

        else:
            return jsonify({
                "error": "Failed to check shipping price from distributor",
                "details": distributor_response.text
            }), distributor_response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error connecting to distributor: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@distributor_bp.route('/api/supplier/fix_kirim', methods=['POST'])
def fix_kirim():
    data = request.json
    id_log = data.get('id_log')

    if not id_log:
        return jsonify({"error": "Missing id_log"}), 400

    try:
        # Mengirim id_log ke endpoint fix_kirim distributor
        fix_kirim_response = requests.post(FIX_KIRIM_URL, json={"id_log": id_log})

        if fix_kirim_response.status_code == 200:
            pengiriman_data = fix_kirim_response.json()

            # Mengambil data dari respons distributor
            harga_pengiriman = pengiriman_data.get("harga_pengiriman")
            lama_pengiriman = pengiriman_data.get("lama_pengiriman")
            no_resi = pengiriman_data.get("no_resi")

            # Cari order berdasarkan id_log
            order = Order.query.filter_by(id_log=id_log).first()
            if not order:
                return jsonify({"error": "Order not found"}), 404

            # Update order dengan informasi pengiriman dan nomor resi
            order.harga_pengiriman = harga_pengiriman
            order.lama_pengiriman = lama_pengiriman
            order.no_resi = no_resi
            db.session.commit()

            # Mengembalikan respons sesuai format yang diinginkan
            return jsonify({
                "harga_pengiriman": harga_pengiriman,
                "lama_pengiriman": lama_pengiriman,
                "message": "Pemesanan berhasil dilakukan",
                "no_resi": no_resi,
                "purchase_id": id_log
            }), 200

        else:
            return jsonify({
                "error": "Failed to finalize shipping",
                "details": fix_kirim_response.text
            }), fix_kirim_response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error connecting to distributor: {str(e)}"}), 500
