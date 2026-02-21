#!/usr/bin/env python3
"""
SEO内容矩阵演示站
功能：1篇长文 → 10条短内容（适配小红书/抖音/B站）
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path
import sys

# 导入content_splitter模块
sys.path.insert(0, str(Path(__file__).parent))
from content_splitter import generate_content_matrix, save_matrix

# 页面配置
st.set_page_config(
    page_title="SEO内容矩阵生成器",
    page_icon="🚀",
    layout="wide"
)

# 标题
st.title("🚀 SEO内容矩阵生成器")
st.markdown("**1篇长文 → 10条短内容（自动适配多平台）**")

st.markdown("---")

# 侧边栏配置
st.sidebar.header("⚙️ 配置")

platform = st.sidebar.selectbox(
    "目标平台",
    ["小红书", "抖音", "B站", "全部生成"]
)

content_type = st.sidebar.selectbox(
    "内容类型",
    ["教程", "种草", "干货", "故事"]
)

keyword_count = st.sidebar.slider(
    "关键词数量",
    min_value=3,
    max_value=10,
    value=5
)

# 主区域
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 输入长文")

    long_form_content = st.text_area(
        "粘贴你的长文内容",
        height=400,
        placeholder="在这里粘贴你的文章、博客或任何长篇内容..."
    )

    keywords = st.text_input(
        "核心关键词（用逗号分隔）",
        placeholder="例如：AI, 自动化, Python, 效率"
    )

    generate_btn = st.button("🚀 生成内容矩阵", type="primary")

with col2:
    st.header("📊 生成预览")

    if generate_btn:
        if not long_form_content.strip():
            st.error("❌ 请先输入长文内容")
        elif not keywords.strip():
            st.error("❌ 请输入核心关键词")
        else:
            with st.spinner("正在生成内容矩阵..."):
                # 调用真实的生成函数
                keywords_list = [k.strip() for k in keywords.split(',') if k.strip()]

                try:
                    matrix = generate_content_matrix(long_form_content, keywords_list)

                    st.success(f"✅ 成功生成{matrix['key_points_count']}个关键观点，{sum(len(v) for v in matrix['platforms'].values())}条内容！")

                    # 显示生成的内容
                    st.markdown("### 生成内容预览：")

                    # 根据选择的平台显示
                    if platform == "全部生成":
                        platforms_list = ["小红书", "抖音", "B站"]
                    else:
                        platforms_list = [platform]

                    for plat in platforms_list:
                        if plat in matrix['platforms']:
                            st.markdown(f"#### 📱 {plat}")

                            contents = matrix['platforms'][plat]
                            for i, content in enumerate(contents[:3], 1):  # 只显示前3条
                                with st.expander(f"{i}. {content['title'][:50]}..."):
                                    st.markdown(f"**类型**：{content.get('type', 'N/A')}")
                                    if 'duration' in content:
                                        st.markdown(f"**时长**：{content['duration']}")
                                    st.markdown(f"**标签**：{', '.join(content.get('tags', []))}")
                                    st.markdown(f"**内容**：\n{content['content']}")

                    # 提供下载
                    st.markdown("---")

                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("💾 保存为JSON"):
                            output_path = Path("output/content_matrix.json")
                            save_matrix(matrix, str(output_path))
                            st.success(f"✅ 已保存到 {output_path}")

                    with col_b:
                        st.download_button(
                            label="📥 下载JSON文件",
                            data=json.dumps(matrix, ensure_ascii=False, indent=2),
                            file_name="content_matrix.json",
                            mime="application/json"
                        )

                except Exception as e:
                    st.error(f"❌ 生成失败：{str(e)}")
                    st.info("💡 请检查输入格式或联系技术支持")

st.markdown("---")

# 功能说明
st.header("✨ 功能特点")

features = {
    "🎯 **智能拆解**": "自动识别长文核心观点，拆分成多条短内容",
    "📱 **平台适配**": "自动适配小红书、抖音、B站等平台的格式和风格",
    "🔑 **SEO优化**": "自动优化标题、关键词、标签，提升搜索排名",
    "⚡ **批量生成**": "1篇文章 → 10条内容，10倍提升产出效率",
    "📊 **数据统计**": "追踪内容表现，优化内容策略"
}

for feature, description in features.items():
    st.markdown(f"- {feature}：{description}")

st.markdown("---")

# 定价信息
st.header("💰 定价方案")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="基础版",
        value="¥5,000/月",
        help="50条内容/月"
    )

with col2:
    st.metric(
        label="专业版",
        value="¥8,000/月",
        help="100条内容/月（推荐）"
    )

with col3:
    st.metric(
        label="企业版",
        value="¥15,000/月",
        help="200条内容/月 + 定制服务"
    )

st.markdown("---")

# 联系方式
st.header("📮 联系我们")

st.info("""
💬 **咨询合作**：请在评论区留言或私信

📦 **演示Demo**：点击上方"生成内容矩阵"按钮查看效果

⏱️ **交付周期**：MVP 1-2周上线
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: grey;'>
    <p>SEO内容矩阵生成器 | 让内容生产自动化</p>
    <p>技术支持：AI自动化服务</p>
</div>
""", unsafe_allow_html=True)
