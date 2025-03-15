from flask import Flask, request, jsonify
from models.product import Product
from models import db
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import json
from cloudConfig import cloudinary
import cloudinary.uploader

def create_product():
    identity_str = get_jwt_identity()
    identity = json.loads(identity_str)

    user_id = identity.get("id")
    role = identity.get("role", "").lower()

    if not user_id or not role:
        return jsonify({"message": "Invalid token data"}), 401

    if request.method == 'POST':
        if role != "farmer":
            return jsonify({"message": "Only farmers can create products"}), 403

        data = request.form 
        image = request.files.get("image") 

        print("Received form data:", data)
        print("Received files:", request.files)

        if not image or image.filename == '':
            return jsonify({"message": "Image file is missing or empty"}), 400

        upload_result = cloudinary.uploader.upload(image)
        image_url = upload_result["secure_url"]

        new_product = Product(
            product_name=data.get('product_name'),
            product_desc=data.get('product_desc'),
            price=float(data.get('price')),
            image_url=image_url,
            user_id=user_id
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify({
            'message': 'Product created successfully',
            'product': {
                'product_name': data.get('product_name'),
                'product_desc': data.get('product_desc'),
                'price': data.get('price'),
                'image_url': image_url
            }
        }), 201

def get_all_product():
    try:
        products = Product.query.all()
        return jsonify({'products': [product.to_dict() for product in products]}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    

def update_product(product_id):
    try:
        identity_str = get_jwt_identity()
        identity = json.loads(identity_str)

        user_id = identity.get("id")
        product = Product.query.get(product_id)

        if not product:
            return jsonify({'message': 'Product not found'}), 404
        
        print(product.user_id)

        print(user_id)
        if product.user_id != user_id:

            return jsonify({'message': 'Unauthorized: You can only update your own products'}), 403

        #updated field
        data = request.json
        product.product_name = data.get('product_name', product.product_name)
        product.product_desc = data.get('product_desc', product.product_desc)
        product.price = data.get('price', product.price)

        db.session.commit()
        return jsonify({'message': 'Product updated successfully', 'product': product.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


def delete_product(product_id):
    try:
        identity_str = get_jwt_identity()  # current logged in user ID
        identity = json.loads(identity_str)

        user_id = identity.get("id")
        
        product = Product.query.get(product_id)

        if not product:
            return jsonify({'message': 'Product not found'}), 404

        if product.user_id != user_id:
            return jsonify({'message': 'Unauthorized: You can only delete your own products'}), 403

        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500