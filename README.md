# AI内容矩阵生成器 v3.0 🚀

> 1篇长文 → 15+条多平台短内容，自动适配6大平台

[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Platforms](https://img.shields.io/badge/平台-6个-orange)]()

## 🎯 核心功能

- **智能拆解**：AI自动识别长文核心观点，提取10个关键要点
- **6平台适配**：小红书 / 抖音 / B站 / 公众号 / 知乎 / 微博
- **SEO优化**：TF-IDF关键词提取 + 4种标题优化风格
- **批量处理**：多篇文章一次生成，适合团队使用
- **多格式导出**：JSON / Markdown / CSV（Excel兼容）
- **内容日历**：自动生成发布排期，含最佳发布时间

## 📱 支持平台

| 平台 | 内容类型 | 特色 |
|------|---------|------|
| 小红书 | 图文笔记 | emoji丰富、标签多、种草风 |
| 抖音 | 短视频脚本 | 口语化、节奏快、强hook |
| B站 | 知识视频 | 深度教程、知识输出 |
| 公众号 | 深度长文+短推文 | 排版精美、引导关注 |
| 知乎 | 专业回答+想法 | 数据支撑、专业深度 |
| 微博 | 正文+长文 | 话题标签、短平快 |

## 🚀 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 演示模式
python3 content_splitter.py

# 处理文件
python3 content_splitter.py article.txt

# 指定关键词
python3 content_splitter.py article.txt "AI,效率,自动化"

# 启动Web API
python3 app.py
```

## 📡 API接口

```bash
# 生成内容矩阵（JSON）
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"content": "你的长文内容..."}'

# 生成CSV（Excel导入）
curl -X POST http://localhost:5000/api/generate/csv \
  -d '{"content": "你的长文内容..."}'

# 批量处理
curl -X POST http://localhost:5000/api/batch \
  -d '{"articles": [{"title": "文章1", "content": "..."}]}'

# 内容日历
curl -X POST http://localhost:5000/api/calendar \
  -d '{"content": "...", "start_date": "2026-02-24", "posts_per_day": 3}'
```

## 💰 商业模式

| 方案 | 价格 | 内容量 | 平台 |
|------|------|--------|------|
| 基础版 | ¥3,000/月 | 50条 | 3个平台 |
| 专业版 | ¥5,000/月 | 100条 | 6个平台 |
| 企业版 | ¥10,000/月 | 200条 | 全平台+定制 |

## 🏷️ 关键词

`AI内容生成` `内容矩阵` `内容营销` `新媒体运营` `一键分发` `多平台内容` `SEO优化` `小红书运营` `抖音运营` `B站运营` `公众号运营` `知乎运营` `微博运营` `内容自动化` `AI写作` `content marketing` `social media automation`

## 📄 License

MIT License
