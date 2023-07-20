from predict import load_model, classify
from flask import Flask, request, jsonify
import requests
from PIL import Image
from io import BytesIO
import os
from urllib.parse import urlparse

app = Flask(__name__)
model = load_model('/root/nsfw/nsfw_mobilenet2.224x224.h5')

@app.route('/process_image', methods=['POST'])
def process_image():
    url = request.json['url']
    response = requests.get(url)
    # 获取 Content-Type 信息
    content_type = response.headers['Content-Type']
    # 根据 Content-Type 推断文件后缀名
    extension = ''
    if content_type == 'image/jpeg':
        extension = '.jpg'
    elif content_type == 'image/jpg':
        extension = '.jpg'
    elif content_type == 'image/png':
        extension = '.png'
    else:
        errorMessage = 'Your File Type is Wrong!'
        print(errorMessage)
        return errorMessage
    img = Image.open(BytesIO(response.content))
    img_name = 'image' + extension
    if extension == '.jpg':
        # If the image mode is not RGB, convert it to RGB
        if img.mode not in ('L', 'RGB'):
            if img.mode == 'RGBA':
                # If image mode is RGBA, convert it to RGB
                img = img.convert('RGB')
            elif img.mode == 'P':
                # If image mode is P (Palette), convert it to RGB
                img = img.convert('RGB')
            elif img.mode == '1':
                # If image mode is 1 (1-bit pixels), convert it to L
                img = img.convert('L')
            else:
                # If image mode is not recognized, raise an error
                raise ValueError('Unrecognized image mode')
    img.save(img_name)
    result = classify(model, img_name)
    # 将处理结果作为JSON响应返回给客户端
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000')
