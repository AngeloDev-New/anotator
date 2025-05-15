from flask import Blueprint, request, jsonify, current_app
import json, os , cv2 ,io,base64
from app.utils.helpers import *
from flask import Response,send_file, abort,Flask, request, jsonify
from app.galore import predictor
import numpy as np
from io import BytesIO

# Definindo o Blueprint para agrupar as rotas de usuários
main_bp = Blueprint('main', __name__)
# def audio/save.php
@main_bp.route('/', methods=['GET'])
def home():
    return getHtml('app/web/index.html')
     
@main_bp.route('/image/<int:n>', methods=['GET'])
def image(n):
    return getImage(n)

@main_bp.route('/lndata', methods=['GET'])
def lndata():
    return str(getDataSetLen())

@main_bp.route('/masc/<int:n>', methods=['GET'])
def masc(n):
    return getMasc(n)

@main_bp.route('/style.css', methods=['GET'])
def style():
    return getCss('app/web/style.css')

@main_bp.route('/script.js', methods=['GET'])
def script():
    return getJs('app/web/script.js')



@main_bp.route('/enviar-semantic', methods=['POST'])
def receber_semantic():
    data = request.get_json()
    index = data['index']
    image_data = data['imageData']

    # Remove o prefixo do Base64 (ex: "data:image/png;base64,")
    image_data = image_data.split(",")[1]

    # Decodifica o base64 em bytes
    image_bytes = base64.b64decode(image_data)
    np_arr = np.frombuffer(image_bytes, np.uint8)

    # Decodifica a imagem usando OpenCV (incluindo canal alpha)
    semantic = cv2.imdecode(np_arr, cv2.IMREAD_UNCHANGED)

    # Salva a imagem como PNG com canal alpha
    cv2.imwrite(f'app/dataset/time/semantics/{index}_image.png', semantic)

    # Carrega a imagem original para dividir em canais
    image = cv2.imread(f'app/data/{index}_image.png', cv2.IMREAD_COLOR)

    # Divide a imagem nos canais B, G, R
    B, G, R = cv2.split(image)

    # Salva cada canal individualmente
    cv2.imwrite(f'app/dataset/time/images/{index}_image_B.png', B)
    cv2.imwrite(f'app/dataset/time/images/{index}_image_G.png', G)
    cv2.imwrite(f'app/dataset/time/images/{index}_image_R.png', R)

    return jsonify({"status": "sucesso", "index": index})