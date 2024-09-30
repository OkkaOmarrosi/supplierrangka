import requests
from flask import Blueprint, jsonify, request

distributor_bp = Blueprint('distributor', __name__)

# URL API distributor untuk cek ongkos kirim
BASE_DISTRIBUTOR_API = "http://159.223.41.243:8000/api/distributors6/orders/cek_ongkir"
BASE_CONFIRM_ORDER_API = "http://167.99.238.114:8000/place_order"


@distributor_bp.route('/api/supplier/cek_harga', methods=['POST'])
def cek_harga():
    # Mendapatkan data JSON dari request body
    data = request.json
    id_log = data.get('id_log')
    kota_tujuan = data.get('kota_tujuan')
    berat = data.get('berat')

    # Validasi input
    if not id_log or not kota_tujuan or berat is None:
        return jsonify({"error": "Missing required parameters"}), 400

    # Mengatur kota asal berdasarkan situasi, misalnya menggunakan "Semarang"
    kota_asal = "Semarang"  # Ganti dengan kota asal yang relevan

    # Mengirim permintaan POST ke distributor API untuk cek ongkir
    try:
        distributor_response = requests.post(BASE_DISTRIBUTOR_API, json={
            "id_log": id_log,  # Ganti dari transaction_id ke id_log
            "kota_asal": kota_asal,
            "kota_tujuan": kota_tujuan,
            "berat": berat
        })

        # Memeriksa apakah permintaan berhasil
        if distributor_response.status_code == 200:
            # Mengambil data dari respons API distributor
            ongkir_data = distributor_response.json()
            harga_pengiriman = ongkir_data.get("harga_pengiriman")  # Mengambil sesuai nama kunci
            lama_pengiriman = ongkir_data.get("lama_pengiriman")  # Mengambil sesuai nama kunci

            # Validasi data dari distributor
            if harga_pengiriman is None or lama_pengiriman is None:
                return jsonify({"error": "Invalid response data from distributor"}), 500

            # Mengembalikan data ke retailer (response JSON)
            return jsonify({
                "harga_pengiriman": harga_pengiriman,
                "id_log": id_log,
                "lama_pengiriman": lama_pengiriman
            }), 200
        else:
            # Respons error dari API distributor
            return jsonify({
                "error": "Failed to check shipping price from distributor",
                "details": distributor_response.text
            }), distributor_response.status_code
    except requests.exceptions.RequestException as e:
        # Penanganan jika gagal koneksi ke API distributor
        return jsonify({"error": f"Error connecting to distributor: {str(e)}"}), 500


# Endpoint untuk mengonfirmasi pesanan ke distributor
@distributor_bp.route('/api/supplier/confirm_pesanan', methods=['POST'])
def confirm_pesanan():
    data = request.json
    id_log = data.get('id_log')

    # Validasi input
    if not id_log:
        return jsonify({"error": "Missing id_log parameter"}), 400

    # Mengirim permintaan konfirmasi ke API distributor
    try:
        distributor_response = requests.post(BASE_CONFIRM_ORDER_API, json={
            "id_log": id_log
        })

        # Memeriksa apakah permintaan berhasil
        if distributor_response.status_code == 200:
            return jsonify({
                "message": "Pesanan berhasil dikonfirmasi",
                "data": distributor_response.json()
            }), 200
        else:
            # Respons error dari API distributor
            return jsonify({
                "error": "Failed to confirm order with distributor",
                "details": distributor_response.text
            }), distributor_response.status_code
    except requests.exceptions.RequestException as e:
        # Penanganan jika gagal koneksi ke API distributor
        return jsonify({"error": f"Error connecting to distributor: {str(e)}"}), 500
