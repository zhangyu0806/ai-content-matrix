#!/usr/bin/env python3
"""
AI内容矩阵生成器 v3.0 - Flask Web API
用法：python3 app.py
访问：http://localhost:5000
"""

import json
import sys
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, Response

sys.path.insert(0, str(Path(__file__).parent))
from content_splitter import (
    generate_content_matrix, matrix_to_markdown, matrix_to_csv,
    batch_generate, batch_to_csv,
    generate_content_calendar, calendar_to_markdown
)

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


@app.route('/api/generate/csv', methods=['POST'])
def generate_csv():
    """Returns CSV format for Excel import"""
    data = request.get_json(force=True)
    content = data.get('content', '').strip()
    if not content:
        return jsonify({"error": "content is required"}), 400

    keywords = data.get('keywords', [])
    platforms = data.get('platforms', None)

    try:
        matrix = generate_content_matrix(content, keywords or None, platforms)
        csv_data = matrix_to_csv(matrix)
        return Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=content_matrix.csv'}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/batch', methods=['POST'])
def batch():
    """
    POST /api/batch
    Body: { "articles": [{"title": "...", "content": "...", "keywords": [...]}], "platforms": [...] }
    """
    data = request.get_json(force=True)
    articles = data.get('articles', [])
    if not articles:
        return jsonify({"error": "articles list is required"}), 400

    platforms = data.get('platforms', None)

    try:
        results = batch_generate(articles, platforms)
        return jsonify({"ok": True, "count": len(results), "data": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/calendar', methods=['POST'])
def calendar():
    """
    POST /api/calendar
    Body: { "content": "...", "start_date": "2026-02-24", "posts_per_day": 3 }
    """
    data = request.get_json(force=True)
    content = data.get('content', '').strip()
    if not content:
        return jsonify({"error": "content is required"}), 400

    keywords = data.get('keywords', [])
    start_date = data.get('start_date', None)
    posts_per_day = data.get('posts_per_day', 3)

    try:
        matrix = generate_content_matrix(content, keywords or None)
        cal = generate_content_calendar(matrix, start_date, posts_per_day)
        fmt = data.get('format', 'json')
        if fmt == 'markdown':
            md = calendar_to_markdown(cal)
            return md, 200, {'Content-Type': 'text/markdown; charset=utf-8'}
        return jsonify({"ok": True, "calendar": cal})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/health')
def health():
    return jsonify({
        "status": "ok",
        "version": "3.0",
        "platforms": ["小红书", "抖音", "B站", "公众号", "知乎", "微博"],
        "features": ["generate", "batch", "csv", "calendar", "markdown"]
    })


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    print(f"\n🚀 AI内容矩阵生成器 v3.0")
    print(f"   本地访问: http://localhost:{port}")
    print(f"   API文档:  http://localhost:{port}/api/health")
    print(f"   支持平台: 小红书/抖音/B站/公众号/知乎/微博")
    app.run(host='0.0.0.0', port=port, debug=False)
