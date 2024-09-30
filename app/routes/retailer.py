from flask import Blueprint, jsonify

retailer_bp = Blueprint('retailer', __name__)

# Dummy Data Retailer
retailer_data = [
    {
        "idretail": 1,
        "name": "Retailer A",
        "contact": "contact@retailerA.com"
    },
    {
        "idretail": 2,
        "name": "Retailer B",
        "contact": "contact@retailerB.com"
    }
]

@retailer_bp.route('/api/retailers', methods=['GET'])
def get_retailers():
    return jsonify(retailer_data)
