from flask import Response,send_file, abort,Flask, request, jsonify
import json
import os
import cv2
from app.galore import predictor
import io
import numpy as np
import base64
from io import BytesIO

dataset = ...


def getMasc(n):
    _ , mask , _ = dataset.__getitem__(n)  # Saída esperada: 2D (valores 0, 1, 2)
    # Cria imagem RGBA
    rgba = np.zeros((mask.shape[0], mask.shape[1], 4), dtype=np.uint8)

    # Fundo (transparente)
    rgba[mask == 0] = [0, 0, 0, 255]

    # Milho (verde semi-transparente)
    rgba[mask == 1] = [0, 255, 0, 0]

    # Daninha (vermelho semi-transparente)
    rgba[mask == 2] = [255, 0, 0, 0]

    # Codifica como PNG com canal alpha
    _, buffer = cv2.imencode('.png', rgba)
    io_buf = io.BytesIO(buffer)

    return send_file(io_buf, mimetype='image/png')


# def getMasc(n):
#     paths = os.listdir('app/data')
#     image_path = os.path.join('app/data', paths[n])
#     image = cv2.imread(image_path, cv2.IMREAD_COLOR)
#     mask = pd.predict(image)
#     # Converter a máscara (supondo que seja uma matriz de 0, 1 e 2)
#     # aqui vc tem a imagen e a mascara faz a sobreposicao deixando a mascara meui transparente pra imagen ficar de fundo
#     _, buffer = cv2.imencode('.png', mask)  # Converte a máscara para o formato PNG
#     io_buf = io.BytesIO(buffer)  # Cria um buffer para enviar os dados da imagem

#     return send_file(io_buf, mimetype='image/png')  


def getHtml(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
            return Response(html_content, mimetype='text/html')
    except FileNotFoundError:
        return Response("<h1>Arquivo não encontrado</h1>", status=404, mimetype='text/html')

def getDataSetLen():
    return len([img for img in os.listdir('app/data') if img.endswith('png')])

def getImage(n):
    
    try:
        path = os.path.join('data', f'{n}_image.png')
        return send_file(path, mimetype='image/png')
    except IndexError:
        return f"Imagem {n} não existe", 404
    except Exception as e:
        return f"Erro: {str(e)}", 500

def getJson(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return Response(json.dumps(data, ensure_ascii=False, indent=2), mimetype='application/json')
    except FileNotFoundError:
        return Response(json.dumps({'erro': 'Arquivo JSON não encontrado.'}), status=404, mimetype='application/json')


def getCss(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return Response(f.read(), mimetype='text/css')
    except FileNotFoundError:
        return Response("/* Arquivo CSS não encontrado */", status=404, mimetype='text/css')


import os
from flask import Response

def getJs(filepath):
    try:
        if not os.path.exists(filepath):
            return Response("// Arquivo JS não encontrado", status=404, mimetype='application/javascript')
            
        with open(filepath, 'r', encoding='utf-8') as f:
            return Response(f.read(), mimetype='application/javascript')
    except Exception as e:
        # Log de erro
        print(f"Erro ao abrir o arquivo {filepath}: {e}")
        return Response("// Erro ao carregar o arquivo JS", status=500, mimetype='application/javascript')



def getFont(filepath):
    try:
        with open(filepath, 'rb') as f:
            ext = os.path.splitext(filepath)[1].lower()
            mimetypes = {
                '.ttf': 'font/ttf',
                '.otf': 'font/otf',
                '.woff': 'font/woff',
                '.woff2': 'font/woff2'
            }
            mimetype = mimetypes.get(ext, 'application/octet-stream')
            return Response(f.read(), mimetype=mimetype)
    except FileNotFoundError:
        return Response("Arquivo de fonte não encontrado", status=404, mimetype='text/plain')
    except Exception as e:
        return Response(f"Erro ao acessar fonte: {str(e)}", status=500, mimetype='text/plain')
