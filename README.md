# AI内容矩阵生成器

> 1篇长文 → 10条短内容，自动适配小红书、抖音、B站、公众号

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)

## ✨ 核心功能

- 🧠 **智能拆解**：自动提取长文核心观点（TF-IDF + 位置权重算法）
- 📱 **4平台适配**：小红书图文 / 抖音脚本 / B站教程 / 公众号长文
- 🔑 **SEO关键词**：自动提取高频关键词，优化标题和标签
- ⚡ **零依赖**：核心功能纯Python标准库，无需安装额外包
- 🌐 **静态演示站**：GitHub Pages 直接部署，无需服务器

## 🚀 快速开始

```bash
git clone https://github.com/zhangyu0806/ai-content-matrix.git
cd ai-content-matrix

# 直接运行（无需安装依赖）
python3 content_splitter.py

# 从文件生成
python3 content_splitter.py my_article.txt "AI,自动化,效率" output/result.json

# 启动Web API（需要Flask）
pip install flask
python3 app.py
```

## 📊 效果演示

输入1篇1000字文章，自动生成：

| 平台 | 数量 | 格式 |
|------|------|------|
| 小红书 | 4-5条 | emoji图文 + 标签 |
| 抖音 | 3-4条 | 30-45秒短视频脚本 |
| B站 | 1-2条 | 5-8分钟知识视频 |
| 公众号 | 2条 | 深度长文 + 短推文 |

**总计：10-13条内容，5分钟完成**

## 🌐 在线演示

部署到 GitHub Pages 后访问：`https://zhangyu0806.github.io/ai-content-matrix`

## 🛠️ API 文档

```bash
# 生成内容矩阵（JSON）
POST /api/generate
{
  "content": "你的长文内容...",
  "keywords": ["关键词1", "关键词2"],  // 可选，自动提取
  "platforms": ["小红书", "抖音"]       // 可选，默认全部
}

# 生成内容矩阵（Markdown）
POST /api/generate/markdown

# 健康检查
GET /api/health
```

## 📈 定价

| 方案 | 价格 | 内容量 |
|------|------|--------|
| 基础版 | ¥5,000/月 | 50条/月 |
| 专业版 | ¥8,000/月 | 100条/月 |
| 企业版 | ¥15,000/月 | 200条/月 + 定制 |

> 💡 ROI：人工写100条内容需要¥50,000+，AI方案只需¥8,000，节省84%成本

## 🤝 合作咨询

- 📧 邮件：[联系方式见 Issues]
- 💬 免费试用3天，满意再付款

## 📄 License

MIT License
