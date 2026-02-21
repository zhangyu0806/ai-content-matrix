#!/bin/bash
# SEO内容矩阵演示站 - 快速启动脚本

echo "🚀 SEO内容矩阵生成器 - 演示站启动"
echo "=================================="
echo ""

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python版本: $python_version"

# 检查是否安装了依赖
echo ""
echo "📦 检查依赖..."

if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "⚠️  未检测到streamlit，正在安装依赖..."
    pip3 install -r requirements.txt
    echo "✓ 依赖安装完成"
else
    echo "✓ 依赖已安装"
fi

echo ""
echo "🎯 启动演示站..."
echo "访问地址: http://localhost:8501"
echo "按 Ctrl+C 停止运行"
echo ""

# 启动Streamlit应用
streamlit run demo_app.py
