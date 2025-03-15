from flask import Blueprint, jsonify , request
from controller.product import create_product , get_all_product , update_product , delete_product
from flask_jwt_extended import jwt_required
# from cloudConfig import cloudinary

product_bp = Blueprint('product' , __name__ )

@product_bp.route("/product", methods=['GET'])
def get_products():
    return get_all_product()

@product_bp.route("/product", methods=['POST'])
@jwt_required()
def product():
    try:
        if request.method=="POST":
            return create_product()
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@product_bp.route("/product/<int:product_id>", methods=['PUT'])
@jwt_required()
def update(product_id):
    return update_product(product_id)

@product_bp.route("/product/<int:product_id>", methods=['DELETE'])
@jwt_required()
def delete(product_id):
    return delete_product(product_id)