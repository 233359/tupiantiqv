from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# 跨域支持（必须添加，否则插件无法调用）
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    return response

@app.route('/extract-images', methods=['GET'])
def extract_images():
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({"error": "请输入目标网址"}), 400
    try:
        # 发送请求并解析网页
        res = requests.get(target_url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        soup = BeautifulSoup(res.text, 'html.parser')
        # 提取所有图片链接
        images = [img.get('src') for img in soup.find_all('img') if img.get('src')]
        # 补全相对路径为绝对路径
        images = [requests.compat.urljoin(target_url, img) for img in images]
        return jsonify({"success": True, "images": images})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
