# 部署到 HuggingFace Space

## 方法1: 使用 Streamlit

### 1. 创建 app_streamlit.py

```python
import streamlit as st
from content_splitter import generate_content_matrix, matrix_to_markdown

st.set_page_config(page_title="AI内容矩阵生成器", page_icon="🚀", layout="wide")

st.title("🚀 AI内容矩阵生成器 v3.0")
st.markdown("> 1篇长文 → 15+条多平台短内容")

col1, col2 = st.columns([2, 1])

with col1:
    content = st.text_area("输入长文内容", height=300, placeholder="粘贴你的长文内容...")

with col2:
    platforms = st.multiselect(
        "选择平台",
        ["小红书", "抖音", "B站", "公众号", "知乎", "微博"],
        default=["小红书", "抖音", "B站"]
    )
    keywords_input = st.text_input("关键词（逗号分隔）", placeholder="AI,效率,自动化")
    posts_per_day = st.slider("每天发布数", 1, 5, 3)

if st.button("生成内容矩阵", type="primary"):
    if not content.strip():
        st.error("请输入内容")
    else:
        keywords = [k.strip() for k in keywords_input.split(',') if k.strip()] if keywords_input else None

        with st.spinner("AI正在生成内容..."):
            matrix = generate_content_matrix(content, keywords, platforms)

        st.success(f"✅ 生成完成！共 {matrix['total_content_count']} 条内容")

        tab1, tab2, tab3 = st.tabs(["内容预览", "Markdown", "数据统计"])

        with tab1:
            for plat, contents in matrix["platforms"].items():
                with st.expander(f"📱 {plat}（{len(contents)}条）"):
                    for i, c in enumerate(contents, 1):
                        st.markdown(f"### {i}. {c['title']}")
                        st.markdown(f"**类型**: {c.get('type', 'N/A')}")
                        if 'duration' in c:
                            st.caption(f"⏱️ {c['duration']}")
                        st.markdown(c['content'])
                        st.markdown(f"**标签**: {', '.join(c.get('tags', []))}")
                        if 'tips' in c:
                            st.info(f"💡 {c['tips']}")
                        st.divider()

        with tab2:
            md = matrix_to_markdown(matrix)
            st.download_button("下载Markdown", md, file_name="content_matrix.md", mime="text/markdown")

        with tab3:
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("关键词数量", len(matrix['keywords']))
            col_b.metric("关键观点", matrix['key_points_count'])
            col_c.metric("生成内容", matrix['total_content_count'])

            st.markdown("### 提取的关键词")
            st.write(matrix['keywords'])

            st.markdown("### 关键观点")
            for i, p in enumerate(matrix['key_points'], 1):
                st.markdown(f"{i}. {p}")
```

### 2. 更新 requirements.txt

```
flask
streamlit
```

### 3. 创建 README.md for HF Space

```markdown
---
title: AI内容矩阵生成器
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.28.0
app_file: app_streamlit.py
pinned: false
license: mit
---

# AI内容矩阵生成器

1篇长文 → 15+条多平台短内容

支持平台：小红书 / 抖音 / B站 / 公众号 / 知乎 / 微博
```

## 方法2: 使用 Gradio

```python
import gradio as gr
from content_splitter import generate_content_matrix, matrix_to_markdown
import json

def generate(content, platforms, keywords_input):
    if not content.strip():
        return "请输入内容", "", ""

    keywords = [k.strip() for k in keywords_input.split(',') if k.strip()] if keywords_input else None
    platform_list = [p.strip() for p in platforms.split(',') if p.strip()] if platforms else None

    matrix = generate_content_matrix(content, keywords, platform_list)

    summary = f"""## 生成完成

- **关键词**: {', '.join(matrix['keywords'][:5])}
- **关键观点**: {matrix['key_points_count']}个
- **生成内容**: {matrix['total_content_count']}条
"""

    preview = ""
    for plat, contents in matrix["platforms"].items():
        preview += f"\n### 📱 {plat}（{len(contents)}条）\n\n"
        for i, c in enumerate(contents[:2], 1):
            preview += f"**{i}. {c['title']}**\n\n{c['content'][:100]}...\n\n"

    md = matrix_to_markdown(matrix)

    return summary, preview, md

demo = gr.Interface(
    fn=generate,
    inputs=[
        gr.Textbox(label="输入长文内容", lines=10, placeholder="粘贴你的长文内容..."),
        gr.Textbox(label="平台（逗号分隔）", value="小红书,抖音,B站"),
        gr.Textbox(label="关键词（逗号分隔，可选）", placeholder="AI,效率,自动化")
    ],
    outputs=[
        gr.Markdown(label="生成摘要"),
        gr.Markdown(label="内容预览"),
        gr.Textbox(label="完整Markdown（可复制）")
    ],
    title="🚀 AI内容矩阵生成器 v3.0",
    description="1篇长文 → 15+条多平台短内容"
)

demo.launch()
```

## 部署步骤

1. 在 HuggingFace 创建新 Space
2. 选择 SDK: Streamlit 或 Gradio
3. 上传文件
4. 等待构建完成
