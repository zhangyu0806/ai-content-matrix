"""
AI内容矩阵生成器 - Streamlit版本
用于HuggingFace Space部署
"""

import streamlit as st
from content_splitter import (
    generate_content_matrix,
    matrix_to_markdown,
    matrix_to_csv,
    generate_content_calendar,
    calendar_to_markdown
)

# 页面配置
st.set_page_config(
    page_title="AI内容矩阵生成器",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .platform-tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        margin: 0.25rem;
        background: #667eea;
        color: white;
        border-radius: 1rem;
        font-size: 0.875rem;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown('<h1 class="main-header">🚀 AI内容矩阵生成器 v3.0</h1>', unsafe_allow_html=True)
st.markdown("> **1篇长文 → 15+条多平台短内容** | 支持小红书/抖音/B站/公众号/知乎/微博")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置")

    platforms = st.multiselect(
        "选择目标平台",
        ["小红书", "抖音", "B站", "公众号", "知乎", "微博"],
        default=["小红书", "抖音", "公众号"]
    )

    keywords_input = st.text_input(
        "关键词（可选，逗号分隔）",
        placeholder="AI,效率,内容营销",
        help="留空则自动提取"
    )

    st.divider()

    st.markdown("### 📊 内容日历")
    enable_calendar = st.checkbox("生成内容日历", value=False)
    start_date = st.date_input("开始日期")
    posts_per_day = st.slider("每天发布数", 1, 5, 3)

    st.divider()
    st.markdown("---")
    st.markdown("### 📝 使用说明")
    st.markdown("""
    1. 粘贴或输入长文内容
    2. 选择目标平台
    3. 点击生成按钮
    4. 查看和下载结果
    """)

# 主内容区
col1, col2 = st.columns([3, 1])

with col1:
    content = st.text_area(
        "📄 输入长文内容",
        height=300,
        placeholder="粘贴你的长文内容（建议500字以上）...",
        help="支持粘贴文章、博客、论文等长文本内容"
    )

with col2:
    st.markdown("### 🎯 快速操作")

    # 示例文本按钮
    if st.button("📝 加载示例文本", use_container_width=True):
        content = st.text_area(
            "📄 输入长文内容",
            value="""我是如何用AI在1周内生成100条内容的？

作为一名新媒体运营，我每天面临的最大挑战就是：如何在有限的时间内产出大量优质内容？

以前，我每天要花8小时在内容创作上。写一篇深度文章2-3小时，改写成小红书笔记1小时，改写成抖音脚本1小时...即使这样，一周最多也只能产出20-30条内容。

直到我发现了一个革命性的工具——AI内容矩阵生成器。

这个工具的核心功能：
1. 智能关键观点提取：自动识别文章的核心观点和金句
2. SEO关键词优化：自动提取高价值关键词，提升搜索排名
3. 多平台内容适配：一键生成小红书、抖音、B站、公众号、知乎、微博六大平台的内容
4. 标题优化：提供4种风格的标题模板（钩子型/数字型/教程型/对比型）

使用这个工具后，我的工作流程彻底改变了：
1. 写一篇高质量的长文：2小时
2. 用AI工具拆解：1分钟（自动生成15+条短内容）
3. 人工筛选和微调：30分钟
4. 批量发布：1小时

总时间：3.5小时，产出15+条内容

效率提升：从20-30条/周 → 100+条/周，提升了5倍！

如果你也在为内容产出效率发愁，不妨试试这个工具。记住，在新媒体时代，内容为王，但效率为皇。""",
            height=300,
            key="content_example"
        )
        st.rerun()

    st.divider()

    # 生成按钮
    generate_btn = st.button(
        "🚀 生成内容矩阵",
        type="primary",
        use_container_width=True
    )

# 生成逻辑
if generate_btn:
    if not content.strip():
        st.error("❌ 请输入内容")
    else:
        # 处理关键词
        keywords = [k.strip() for k in keywords_input.split(',') if k.strip()] if keywords_input else None

        # 显示进度
        with st.spinner("🤖 AI正在生成内容矩阵..."):
            try:
                matrix = generate_content_matrix(content, keywords, platforms)

                # 成功提示
                st.success(f"✅ 生成完成！共 **{matrix['total_content_count']}** 条内容")
                st.balloons()

                # 创建标签页
                tab1, tab2, tab3, tab4 = st.tabs(["📱 内容预览", "📄 下载Markdown", "📊 数据统计", "📅 内容日历"])

                with tab1:
                    # 按平台展示
                    for plat, contents in matrix["platforms"].items():
                        if contents:
                            with st.expander(f"📱 {plat}（{len(contents)}条）", expanded=True):
                                for i, c in enumerate(contents, 1):
                                    col_a, col_b = st.columns([4, 1])

                                    with col_a:
                                        st.markdown(f"### {i}. {c['title']}")
                                        st.caption(f"**类型**: {c.get('type', 'N/A')}")

                                        if 'duration' in c:
                                            st.caption(f"⏱️ 时长: {c['duration']}")

                                        st.markdown(c['content'])

                                        if c.get('tags'):
                                            tags_html = " ".join([f'<span class="platform-tag">{tag}</span>' for tag in c['tags']])
                                            st.markdown(f"**标签**: {tags_html}", unsafe_allow_html=True)

                                        if c.get('tips'):
                                            st.info(f"💡 {c['tips']}")

                                    with col_b:
                                        if st.button(f"📋 复制", key=f"{plat}_{i}"):
                                            st.code(c['content'], language=None)

                                    st.divider()

                with tab2:
                    # Markdown下载
                    md = matrix_to_markdown(matrix)
                    st.download_button(
                        label="📥 下载完整Markdown",
                        data=md,
                        file_name="content_matrix.md",
                        mime="text/markdown",
                        use_container_width=True
                    )

                    st.markdown("### 预览（前500字）")
                    st.markdown(md[:500] + "...")

                with tab3:
                    # 数据统计
                    col_a, col_b, col_c = st.columns(3)

                    with col_a:
                        st.metric("🏷️ 关键词", len(matrix['keywords']))
                    with col_b:
                        st.metric("💡 关键观点", matrix['key_points_count'])
                    with col_c:
                        st.metric("📝 生成内容", matrix['total_content_count'])

                    st.divider()

                    # 关键词展示
                    st.markdown("### 🏷️ 提取的关键词")
                    keywords_html = " ".join([f'<span class="platform-tag">{kw}</span>' for kw in matrix['keywords']])
                    st.markdown(keywords_html, unsafe_allow_html=True)

                    # 关键观点展示
                    st.markdown("### 💡 关键观点")
                    for i, p in enumerate(matrix['key_points'], 1):
                        st.markdown(f"{i}. {p}")

                    # 原文摘要
                    st.markdown("### 📄 原文摘要")
                    st.info(matrix.get('source_summary', 'N/A'))

                with tab4:
                    if enable_calendar:
                        st.markdown("### 📅 内容发布日历")

                        with st.spinner("生成日历..."):
                            calendar = generate_content_calendar(matrix, str(start_date), posts_per_day)
                            cal_md = calendar_to_markdown(calendar)
                            st.markdown(cal_md)

                            st.download_button(
                                label="📥 下载日历",
                                data=cal_md,
                                file_name="content_calendar.md",
                                mime="text/markdown"
                            )
                    else:
                        st.info("💡 在侧边栏勾选'生成内容日历'以使用此功能")

            except Exception as e:
                st.error(f"❌ 生成失败: {str(e)}")
                st.exception(e)

# 底部信息
st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🚀 AI内容矩阵生成器 v3.0 | 支持平台：小红书 / 抖音 / B站 / 公众号 / 知乎 / 微博</p>
    <p>💡 提示：生成后可复制内容到对应平台发布，建议人工审核后再发布</p>
</div>
""", unsafe_allow_html=True)
