#!/usr/bin/env python3
"""
AI内容矩阵生成器 - Flask Web API
用法：python app.py
访问：http://localhost:5000
"""

import json
import sys
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory

sys.path.insert(0, str(Path(__file__).parent))
from content_splitter import generate_content_matrix, matrix_to_markdown

app = Flask(__name__, static_folder='docs', static_url_path='')


@app.route('/')
def index():
    return send_from_directory('docs', 'index.html')


@app.route('/api/generate', methods=['POST'])
def generate():
    """
    POST /api/generate
    Body: { "content": "...", "keywords": ["kw1","kw2"], "platforms": ["小红书","抖音"] }
    Returns: content matrix JSON
    """
    data = request.get_json(force=True)
    content = data.get('content', '').strip()
    if not content:
        return jsonify({"error": "content is required"}), 400

    keywords = data.get('keywords', [])
    platforms = data.get('platforms', None)

    try:
        matrix = generate_content_matrix(content, keywords or None, platforms)
        return jsonify({"ok": True, "data": matrix})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/generate/markdown', methods=['POST'])
def generate_markdown():
    """Same as /api/generate but returns Markdown text"""
    data = request.get_json(force=True)
    content = data.get('content', '').strip()
    if not content:
        return jsonify({"error": "content is required"}), 400

    keywords = data.get('keywords', [])
    platforms = data.get('platforms', None)

    try:
        matrix = generate_content_matrix(content, keywords or None, platforms)
        md = matrix_to_markdown(matrix)
        return md, 200, {'Content-Type': 'text/markdown; charset=utf-8'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/health')
def health():
    return jsonify({"status": "ok", "version": "2.0"})


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    print(f"\n🚀 AI内容矩阵生成器 v2.0")
    print(f"   本地访问: http://localhost:{port}")
    print(f"   API文档:  http://localhost:{port}/api/health")
    app.run(host='0.0.0.0', port=port, debug=False)
