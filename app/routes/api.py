from flask import Blueprint, jsonify, request
from app.models import Supplier, db  # Pastikan Anda mengimpor db


api_bp = Blueprint('api', __name__)

@api_bp.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    supplier_list = [{"name": supplier.name, "location": supplier.location} for supplier in suppliers]
    return jsonify(supplier_list)

@api_bp.route('/api/add/suppliers', methods=['POST'])  # Pastikan user harus login untuk bisa menginsert data
def add_supplier():
    data = request.get_json()  # Ambil data dari body permintaan JSON
    if not data or 'name' not in data or 'location' not in data:
        return jsonify({"error": "Bad Request", "message": "Name and location are required."}), 400

    new_supplier = Supplier(name=data['name'], location=data['location'])
    db.session.add(new_supplier)
    db.session.commit()
    return jsonify({"message": "Supplier added successfully!"}), 201

