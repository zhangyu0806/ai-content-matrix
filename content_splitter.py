#!/usr/bin/env python3
"""
AI内容拆解脚本
功能：1篇长文 → 10条短内容（小红书/抖音/B站）
"""

import json
import re
from pathlib import Path
from typing import List, Dict

class ContentSplitter:
    """内容拆解器"""

    def __init__(self, long_form_content: str, keywords: List[str]):
        self.content = long_form_content
        self.keywords = keywords
        self.sentences = []
        self.paragraphs = []

    def preprocess(self):
        """预处理：分段、分句"""
        # 按段落分割
        self.paragraphs = [p.strip() for p in self.content.split('\n') if p.strip()]

        # 按句子分割（简单实现）
        for para in self.paragraphs:
            sentences = re.split(r'[。！？；]', para)
            self.sentences.extend([s.strip() for s in sentences if s.strip()])

    def extract_key_points(self, top_n=10) -> List[str]:
        """提取关键观点（启发式算法）"""
        key_points = []

        # 策略1：含关键词的句子
        for sentence in self.sentences:
            for keyword in self.keywords:
                if keyword in sentence:
                    key_points.append(sentence)
                    break

        # 策略2：长句（可能包含重要信息）
        long_sentences = [s for s in self.sentences if len(s) > 30]
        key_points.extend(long_sentences[:3])

        # 策略3：段落首句（通常是主题句）
        first_sentences = [para.split('，')[0] for para in self.paragraphs if para]
        key_points.extend(first_sentences[:2])

        # 去重并限制数量
        seen = set()
        unique_points = []
        for point in key_points:
            if point not in seen and len(point) > 10:
                seen.add(point)
                unique_points.append(point)
                if len(unique_points) >= top_n:
                    break

        return unique_points

class PlatformAdapter:
    """平台适配器"""

    @staticmethod
    def xiaohongshu(key_points: List[str], keywords: List[str]) -> List[Dict]:
        """小红书格式"""
        contents = []

        for i, point in enumerate(key_points, 1):
            # 标题：emoji + 关键词
            title = f"🔥 {keywords[0] if keywords else ''}真的太强了！"

            # 正文：观点+emoji
            body = f"""
{point}

💡 小贴士：记得点赞收藏哦～

#{keywords[0] if keywords else '干货'} #内容营销 #SEO
            """.strip()

            contents.append({
                "platform": "小红书",
                "type": "图文",
                "title": title,
                "content": body,
                "tags": keywords[:3]
            })

        return contents

    @staticmethod
    def douyin(key_points: List[str], keywords: List[str]) -> List[Dict]:
        """抖音格式"""
        contents = []

        for i, point in enumerate(key_points[:5], 1):  # 抖音要少一点
            # 标题：悬念式
            title = f"第{i}招：{keywords[0] if keywords else ''}秘籍"

            # 脚本：口语化
            script = f"""
（开场）
家人们！今天分享{keywords[0] if keywords else ''}的第{i}个技巧！

（正文）
{point}

（结尾）
关注我，下期更精彩！记得点赞收藏~
            """.strip()

            contents.append({
                "platform": "抖音",
                "type": "短视频",
                "title": title,
                "content": script,
                "duration": "30-60秒",
                "tags": keywords[:3]
            })

        return contents

    @staticmethod
    def bilibili(key_points: List[str], keywords: List[str]) -> List[Dict]:
        """B站格式"""
        contents = []

        for i, point in enumerate(key_points[:3], 1):  # B站要更少更长
            # 标题：教程式
            title = f"【教程】{keywords[0] if keywords else ''}完全指南（第{i}期）"

            # 脚本：详细讲解
            script = f"""
【开场】
大家好，今天来讲{keywords[0] if keywords else ''}的第{i}个重点。

【正文】
{point}

【详细讲解】
这里可以展开讲2-3分钟...

【总结】
这个方法非常实用，建议反复观看！

【结尾】
一键三连，我们下期见！
            """.strip()

            contents.append({
                "platform": "B站",
                "type": "中视频",
                "title": title,
                "content": script,
                "duration": "3-5分钟",
                "tags": keywords[:5] + ["教程", "干货"]
            })

        return contents

def generate_content_matrix(long_form_content: str, keywords: List[str]) -> Dict:
    """
    生成内容矩阵

    Args:
        long_form_content: 长文内容
        keywords: 关键词列表

    Returns:
        内容矩阵字典
    """
    # 预处理
    splitter = ContentSplitter(long_form_content, keywords)
    splitter.preprocess()

    # 提取关键观点
    key_points = splitter.extract_key_points(top_n=10)

    # 平台适配
    adapter = PlatformAdapter()

    matrix = {
        "source_content": long_form_content[:200] + "...",  # 前200字符
        "keywords": keywords,
        "key_points_count": len(key_points),
        "platforms": {}
    }

    # 小红书
    matrix["platforms"]["小红书"] = adapter.xiaohongshu(key_points, keywords)

    # 抖音
    matrix["platforms"]["抖音"] = adapter.douyin(key_points, keywords)

    # B站
    matrix["platforms"]["B站"] = adapter.bilibili(key_points, keywords)

    return matrix

def save_matrix(matrix: Dict, output_path: str):
    """保存内容矩阵"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(matrix, f, ensure_ascii=False, indent=2)

    print(f"✓ 内容矩阵已保存：{output_path}")
    print(f"  关键观点数：{matrix['key_points_count']}")
    print(f"  平台数：{len(matrix['platforms'])}")

    # 统计
    total_content = sum(len(contents) for contents in matrix["platforms"].values())
    print(f"  生成内容数：{total_content}")

def main():
    """示例使用"""
    # 示例长文
    long_form = """
企业文档自动化是提升效率的关键。

很多企业每天要处理大量PDF发票、合同、报表。传统方式是手动复制粘贴到Excel，不仅效率低，还容易出错。

使用Python自动化工具可以将这个过程自动化。首先用pdfplumber库提取PDF中的表格数据，然后用pandas清洗数据（去重、格式统一），最后用docxtpl填充Word模板生成文档。

整个流程可以处理100份文件只需5分钟，而手动方式需要8小时。效率提升近100倍。

对于律所、财务公司、招投标代理等行业，这个工具可以节省大量人力成本。商业模式可以按页收费（0.2-0.5元/页），或者月包（1000-5000元/月）。

技术实现不难，核心是选择合适的Python库和设计好工作流程。我已经开源了完整代码，可以直接使用。
    """

    # 关键词
    keywords = ["企业自动化", "Python", "效率提升", "文档处理"]

    # 生成内容矩阵
    print("\n正在生成内容矩阵...")
    matrix = generate_content_matrix(long_form, keywords)

    # 保存
    save_matrix(matrix, "output/content_matrix.json")

    # 打印预览
    print("\n" + "="*50)
    print("内容预览：")
    print("="*50)

    for platform, contents in matrix["platforms"].items():
        print(f"\n【{platform}】")
        for i, content in enumerate(contents[:2], 1):  # 只显示前2条
            print(f"\n{i}. {content['title']}")
            print(f"   {content['content'][:100]}...")

if __name__ == "__main__":
    main()
