from flask import Blueprint, request, jsonify, current_app
import json, os
from app.utils.helpers import *

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

@main_bp.route('/script,js', methods=['GET'])
def script():
    return getJs('app/web/script.js')



