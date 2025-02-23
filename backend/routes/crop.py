from flask import Blueprint
from flask import request
from controller.crop import predictCrop, detectDisease

crop_bp = Blueprint('crop', __name__)

crop_bp.route('/crop/predictcrop', methods=['POST'])(predictCrop)
crop_bp.route('/crop/detectdisease', methods=['POST'])(detectDisease)


