#!/usr/bin/env python3
"""
AI内容拆解引擎 v2.0
功能：1篇长文 → 10+条短内容（小红书/抖音/B站/公众号）
特性：
  - 智能关键观点提取（TF-IDF + 位置权重 + 语义规则）
  - SEO关键词自动提取
  - 4平台适配（小红书/抖音/B站/公众号）
  - 标题优化（多种风格模板）
  - JSON/Markdown 双格式输出
"""

import json
import re
import math
from collections import Counter
from pathlib import Path
from typing import List, Dict, Tuple, Optional


# ============================================================
# SEO 关键词提取
# ============================================================

# 中文停用词（精简版）
STOP_WORDS = set(
    "的 了 在 是 我 有 和 就 不 人 都 一 一个 上 也 很 到 说 要 去 你 会 着 没有 看 好 "
    "自己 这 他 她 它 们 那 些 什么 怎么 如何 为什么 可以 能 但 而 与 或 及 等 把 被 让 "
    "从 对 向 以 因为 所以 如果 虽然 但是 然后 这个 那个 这些 那些 已经 还 又 再 才 "
    "只 比 更 最 非常 特别 真的 其实 当然 可能 应该 需要 使用 通过 进行 实现 提供 "
    "包括 以及 之后 之前 目前 现在 今天 每天 每月 每年".split()
)


def extract_keywords(text: str, top_n: int = 8) -> List[str]:
    """
    基于TF-IDF思想的关键词提取（无外部依赖）
    """
    # 简单中文分词：按标点和空格切分，再按2-4字组合
    segments = re.split(r'[，。！？；：、\s\n\r\t（）【】""''《》]+', text)
    segments = [s.strip() for s in segments if s.strip()]

    # 提取候选词（2-6字的片段）
    candidates = []
    for seg in segments:
        # 英文词
        eng_words = re.findall(r'[A-Za-z][A-Za-z0-9]+', seg)
        candidates.extend(eng_words)
        # 中文片段（2-6字）
        chinese = re.sub(r'[A-Za-z0-9]+', ' ', seg)
        for length in (4, 3, 2, 5, 6):
            for i in range(len(chinese) - length + 1):
                word = chinese[i:i + length].strip()
                if len(word) >= 2 and word not in STOP_WORDS:
                    candidates.append(word)

    # 词频统计
    freq = Counter(candidates)

    # 位置加权：出现在前20%的词加分
    text_len = len(text)
    for word, count in list(freq.items()):
        first_pos = text.find(word)
        if first_pos >= 0 and first_pos < text_len * 0.2:
            freq[word] = int(count * 1.5)

    # 过滤：至少出现2次，或者是英文专有名词
    filtered = {
        w: c for w, c in freq.items()
        if c >= 2 or (re.match(r'^[A-Z]', w) and len(w) > 2)
    }

    # 按频率排序
    sorted_words = sorted(filtered.items(), key=lambda x: x[1], reverse=True)

    # 去除子串重复（如果"内容营销"和"内容"都在，保留长的）
    result = []
    for word, _ in sorted_words:
        is_substr = False
        for existing in result:
            if word in existing or existing in word:
                if len(word) < len(existing):
                    is_substr = True
                    break
        if not is_substr:
            result.append(word)
        if len(result) >= top_n:
            break

    return result


def optimize_title(base_title: str, keywords: List[str], style: str = "hook") -> str:
    """
    标题优化器
    style: hook(悬念), number(数字), how(教程), compare(对比)
    """
    kw = keywords[0] if keywords else ""

    templates = {
        "hook": [
            f"99%的人不知道的{kw}秘密",
            f"用了{kw}之后，效率翻了10倍",
            f"别再手动做了！{kw}帮你省80%时间",
            f"震惊！{kw}居然可以这样用",
        ],
        "number": [
            f"{kw}的5个核心技巧，第3个最实用",
            f"3分钟学会{kw}，从入门到精通",
            f"用{kw}1周产出100条内容的方法",
            f"掌握这3点，{kw}效率提升10倍",
        ],
        "how": [
            f"手把手教你用{kw}",
            f"{kw}完全指南：从0到1",
            f"新手必看：{kw}入门教程",
            f"如何用{kw}实现自动化",
        ],
        "compare": [
            f"手动 vs {kw}：效率差了100倍",
            f"用{kw}前后对比，差距太大了",
            f"还在手动？试试{kw}吧",
            f"人工8小时 vs {kw}5分钟",
        ],
    }

    import random
    choices = templates.get(style, templates["hook"])
    return random.choice(choices)


# ============================================================
# 内容拆解引擎
# ============================================================

class ContentSplitter:
    """内容拆解器 v2"""

    def __init__(self, content: str, keywords: Optional[List[str]] = None):
        self.content = content.strip()
        self.keywords = keywords or []
        self.sentences: List[str] = []
        self.paragraphs: List[str] = []
        self.sections: List[Dict] = []  # {title, body, sentences}

    def preprocess(self):
        """预处理：分段、分句、识别结构"""
        # 按段落分割
        raw_paras = self.content.split('\n')
        self.paragraphs = [p.strip() for p in raw_paras if p.strip()]

        # 识别章节结构
        current_section = {"title": "", "body": [], "sentences": []}
        for para in self.paragraphs:
            # 检测标题行（短句、以冒号结尾、或全大写/加粗）
            is_title = (
                len(para) < 30 and (
                    para.endswith('：') or para.endswith(':') or
                    re.match(r'^[#\*]+\s', para) or
                    re.match(r'^\d+[\.、]', para) or
                    re.match(r'^[一二三四五六七八九十]+[、.]', para)
                )
            )
            if is_title and current_section["body"]:
                self.sections.append(current_section)
                current_section = {"title": para, "body": [], "sentences": []}
            else:
                current_section["body"].append(para)

        if current_section["body"]:
            self.sections.append(current_section)

        # 分句
        for para in self.paragraphs:
            sents = re.split(r'[。！？\n]', para)
            for s in sents:
                s = s.strip().strip('，；：、')
                if s and len(s) > 5:
                    self.sentences.append(s)

        # 如果没有提供关键词，自动提取
        if not self.keywords:
            self.keywords = extract_keywords(self.content, top_n=6)

    def _score_sentence(self, sentence: str, position: int, total: int) -> float:
        """给句子打分"""
        score = 0.0

        # 关键词命中
        kw_hits = sum(1 for kw in self.keywords if kw in sentence)
        score += kw_hits * 3.0

        # 长度分（20-80字最佳）
        length = len(sentence)
        if 20 <= length <= 80:
            score += 2.0
        elif 10 <= length <= 120:
            score += 1.0

        # 位置分（开头和结尾更重要）
        rel_pos = position / max(total, 1)
        if rel_pos < 0.15:  # 前15%
            score += 2.5
        elif rel_pos > 0.85:  # 后15%
            score += 1.5
        elif rel_pos < 0.3:  # 前30%
            score += 1.0

        # 数字/数据分（含数字的句子更有说服力）
        if re.search(r'\d+', sentence):
            score += 1.5

        # 对比/转折分
        contrast_words = ['但是', '然而', '不过', '相比', '对比', 'vs', '从', '到', '提升', '节省', '降低']
        if any(w in sentence for w in contrast_words):
            score += 1.0

        # 行动词分
        action_words = ['方法', '技巧', '步骤', '流程', '策略', '秘诀', '关键', '核心', '重点']
        if any(w in sentence for w in action_words):
            score += 1.0

        # 列表项加分（通常是要点）
        if re.match(r'^[\d\-\*•✅❌]', sentence):
            score += 0.5

        return score

    def extract_key_points(self, top_n: int = 10) -> List[str]:
        """提取关键观点（带评分）"""
        if not self.sentences:
            self.preprocess()

        scored = []
        total = len(self.sentences)
        for i, sent in enumerate(self.sentences):
            score = self._score_sentence(sent, i, total)
            scored.append((sent, score))

        # 按分数排序
        scored.sort(key=lambda x: x[1], reverse=True)

        # 去重（相似度>0.5的去掉）
        result = []
        for sent, score in scored:
            is_dup = False
            for existing in result:
                # 简单相似度：共同字符比例
                common = len(set(sent) & set(existing))
                similarity = common / max(len(set(sent)), len(set(existing)), 1)
                if similarity > 0.6:
                    is_dup = True
                    break
            if not is_dup:
                result.append(sent)
            if len(result) >= top_n:
                break

        return result

    def extract_stats(self) -> Dict:
        """提取文章中的数据/统计信息"""
        stats = []
        for sent in self.sentences:
            numbers = re.findall(r'(\d+[\.\d]*[%％万亿元块条个份页小时分钟秒倍]?)', sent)
            if numbers:
                stats.append({"sentence": sent, "numbers": numbers})
        return stats


# ============================================================
# 平台适配器
# ============================================================

class PlatformAdapter:
    """多平台内容适配器"""

    @staticmethod
    def xiaohongshu(key_points: List[str], keywords: List[str], stats: List[Dict] = None) -> List[Dict]:
        """小红书格式：emoji丰富、标签多、种草风"""
        contents = []
        emojis = ['🔥', '💡', '✨', '🎯', '💪', '📌', '⚡', '🌟', '💰', '🚀']
        tags = ' '.join(f'#{kw}' for kw in keywords[:5])

        for i, point in enumerate(key_points[:5]):
            emoji = emojis[i % len(emojis)]
            title = f"{emoji} {optimize_title(point[:20], keywords, 'hook')}"

            body = f"""{point}

{'─' * 20}
{tags} #干货分享 #效率工具

💬 觉得有用就点赞收藏吧～"""

            contents.append({
                "platform": "小红书",
                "type": "图文笔记",
                "title": title,
                "content": body,
                "tags": keywords[:5] + ["干货分享", "效率工具"],
                "tips": "配图建议：数据对比图/操作截图/效果展示"
            })

        return contents

    @staticmethod
    def douyin(key_points: List[str], keywords: List[str], stats: List[Dict] = None) -> List[Dict]:
        """抖音格式：口语化、节奏快、强hook"""
        contents = []

        for i, point in enumerate(key_points[:4]):
            title = optimize_title(point[:20], keywords, 'number')

            # 提取数据做hook
            hook = "家人们，这个方法真的绝了！"
            if stats:
                for s in stats:
                    if any(n in point for n in s.get("numbers", [])):
                        hook = f"你敢信？{s['sentence'][:30]}！"
                        break

            script = f"""【黄金3秒】
{hook}

【正文 - 15秒】
{point}

【转折/高潮 - 10秒】
很多人不知道这个方法，但用过的都说好！

【结尾CTA - 5秒】
关注我，每天分享{keywords[0] if keywords else '实用'}技巧！
点赞收藏，下次用得上～

#{' #'.join(keywords[:3])}"""

            contents.append({
                "platform": "抖音",
                "type": "短视频脚本",
                "title": title,
                "content": script,
                "duration": "30-45秒",
                "tags": keywords[:3],
                "tips": "拍摄建议：真人出镜+屏幕录制，前3秒必须抓眼球"
            })

        return contents

    @staticmethod
    def bilibili(key_points: List[str], keywords: List[str], stats: List[Dict] = None) -> List[Dict]:
        """B站格式：深度、教程风、知识输出"""
        contents = []

        # B站适合把多个观点合并成1-2个深度视频
        for i in range(0, min(len(key_points), 6), 3):
            batch = key_points[i:i + 3]
            title = optimize_title(batch[0][:20], keywords, 'how')

            points_text = ""
            for j, p in enumerate(batch, 1):
                points_text += f"\n【第{j}点】\n{p}\n"

            script = f"""【开场白 - 30秒】
大家好，今天来聊一个很实用的话题：{keywords[0] if keywords else '效率提升'}。
看完这期视频，你会学到{len(batch)}个核心技巧。

【正文 - 3-5分钟】
{points_text}

【实操演示 - 2分钟】
接下来我实际操作给大家看...
（此处插入屏幕录制）

【总结 - 30秒】
今天分享了{len(batch)}个要点，最重要的是第1点。
如果觉得有帮助，一键三连支持一下！

【结尾】
我是XX，专注{keywords[0] if keywords else '效率工具'}分享。
关注我，下期更精彩！"""

            contents.append({
                "platform": "B站",
                "type": "知识视频",
                "title": title,
                "content": script,
                "duration": "5-8分钟",
                "tags": keywords[:5] + ["教程", "干货", "效率"],
                "tips": "封面建议：大字标题+数据对比，缩略图要有冲击力"
            })

        return contents

    @staticmethod
    def wechat(key_points: List[str], keywords: List[str], stats: List[Dict] = None) -> List[Dict]:
        """公众号格式：深度长文、排版精美、引导关注"""
        contents = []

        # 公众号适合1篇深度文章
        title = optimize_title(key_points[0][:20] if key_points else "", keywords, 'compare')

        points_text = ""
        for i, p in enumerate(key_points[:6], 1):
            points_text += f"\n**{i}. {p[:20]}**\n\n{p}\n"

        # 数据引用
        data_section = ""
        if stats and len(stats) >= 2:
            data_section = "\n## 📊 数据说话\n\n"
            for s in stats[:3]:
                data_section += f"> {s['sentence']}\n\n"

        article = f"""# {title}

> {key_points[0][:50] if key_points else ''}...

---

## 前言

你是否也遇到过这样的问题？每天花大量时间在重复性工作上，效率低下，还容易出错。

今天分享{len(key_points[:6])}个实用技巧，帮你彻底解决这个问题。

---

## 核心要点
{points_text}
{data_section}
---

## 总结

以上就是今天分享的全部内容。如果觉得有帮助，欢迎**转发**给需要的朋友。

**关注公众号**，回复「{keywords[0] if keywords else '工具'}」获取完整资料包。

---

*本文由AI内容矩阵工具辅助生成*
*{' | '.join(f'#{kw}' for kw in keywords[:4])}*"""

        contents.append({
            "platform": "公众号",
            "type": "深度长文",
            "title": title,
            "content": article,
            "tags": keywords[:5],
            "tips": "排版建议：使用135编辑器/秀米，添加分割线和引用框"
        })

        # 公众号短推文
        if len(key_points) >= 3:
            short_title = f"【干货】{keywords[0] if keywords else '效率'}提升指南"
            short_body = f"""📌 {key_points[0]}

💡 {key_points[1]}

🔥 {key_points[2]}

👉 完整版请看今天的推文～

{''.join(f'#{kw} ' for kw in keywords[:3])}"""

            contents.append({
                "platform": "公众号",
                "type": "短推文/次条",
                "title": short_title,
                "content": short_body,
                "tags": keywords[:3],
                "tips": "适合作为次条推送，引导阅读主文"
            })

        return contents


# ============================================================
# 内容矩阵生成器
# ============================================================

def generate_content_matrix(
    long_form_content: str,
    keywords: Optional[List[str]] = None,
    platforms: Optional[List[str]] = None
) -> Dict:
    """
    生成内容矩阵

    Args:
        long_form_content: 长文内容
        keywords: 关键词列表（可选，自动提取）
        platforms: 目标平台列表（可选，默认全部）

    Returns:
        内容矩阵字典
    """
    # 预处理
    splitter = ContentSplitter(long_form_content, keywords)
    splitter.preprocess()

    # 自动提取的关键词
    auto_keywords = splitter.keywords

    # 合并用户提供的和自动提取的关键词
    all_keywords = list(dict.fromkeys((keywords or []) + auto_keywords))[:10]

    # 提取关键观点
    key_points = splitter.extract_key_points(top_n=10)

    # 提取统计数据
    stats = splitter.extract_stats()

    # 平台适配
    adapter = PlatformAdapter()
    all_platforms = platforms or ["小红书", "抖音", "B站", "公众号"]

    platform_map = {
        "小红书": adapter.xiaohongshu,
        "抖音": adapter.douyin,
        "B站": adapter.bilibili,
        "公众号": adapter.wechat,
    }

    matrix = {
        "source_summary": long_form_content[:300] + ("..." if len(long_form_content) > 300 else ""),
        "source_length": len(long_form_content),
        "keywords": all_keywords,
        "auto_keywords": auto_keywords,
        "key_points_count": len(key_points),
        "key_points": key_points,
        "stats_found": len(stats),
        "platforms": {},
        "total_content_count": 0,
    }

    for plat in all_platforms:
        if plat in platform_map:
            contents = platform_map[plat](key_points, all_keywords, stats)
            matrix["platforms"][plat] = contents

    matrix["total_content_count"] = sum(len(v) for v in matrix["platforms"].values())

    return matrix


def save_matrix(matrix: Dict, output_path: str, fmt: str = "json"):
    """保存内容矩阵"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if fmt == "json":
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(matrix, f, ensure_ascii=False, indent=2)
    elif fmt == "markdown":
        md = matrix_to_markdown(matrix)
        with open(output_path.with_suffix('.md'), 'w', encoding='utf-8') as f:
            f.write(md)

    print(f"✓ 内容矩阵已保存：{output_path}")
    print(f"  关键词：{', '.join(matrix['keywords'][:5])}")
    print(f"  关键观点：{matrix['key_points_count']}个")
    print(f"  生成内容：{matrix['total_content_count']}条")


def matrix_to_markdown(matrix: Dict) -> str:
    """将矩阵转为Markdown格式"""
    lines = [
        f"# 内容矩阵报告",
        f"",
        f"**关键词**: {', '.join(matrix['keywords'][:5])}",
        f"**关键观点**: {matrix['key_points_count']}个",
        f"**生成内容**: {matrix['total_content_count']}条",
        f"",
        f"---",
        f"",
    ]

    for plat, contents in matrix["platforms"].items():
        lines.append(f"## {plat}（{len(contents)}条）")
        lines.append("")
        for i, c in enumerate(contents, 1):
            lines.append(f"### {i}. {c['title']}")
            lines.append(f"**类型**: {c.get('type', 'N/A')}")
            if 'duration' in c:
                lines.append(f"**时长**: {c['duration']}")
            lines.append(f"**标签**: {', '.join(c.get('tags', []))}")
            lines.append("")
            lines.append(c['content'])
            lines.append("")
            if 'tips' in c:
                lines.append(f"> 💡 {c['tips']}")
            lines.append("")
            lines.append("---")
            lines.append("")

    return '\n'.join(lines)


# ============================================================
# CLI 入口
# ============================================================

def main():
    """命令行使用"""
    import sys

    if len(sys.argv) > 1:
        # 从文件读取
        input_file = sys.argv[1]
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        keywords = sys.argv[2].split(',') if len(sys.argv) > 2 else None
        output = sys.argv[3] if len(sys.argv) > 3 else "output/content_matrix.json"

        matrix = generate_content_matrix(content, keywords)
        save_matrix(matrix, output)
        save_matrix(matrix, output, fmt="markdown")
    else:
        # 演示模式
        demo_content = """
企业文档自动化是提升效率的关键。

很多企业每天要处理大量PDF发票、合同、报表。传统方式是手动复制粘贴到Excel，不仅效率低，还容易出错。

使用Python自动化工具可以将这个过程自动化。首先用pdfplumber库提取PDF中的表格数据，然后用pandas清洗数据（去重、格式统一），最后用docxtpl填充Word模板生成文档。

整个流程可以处理100份文件只需5分钟，而手动方式需要8小时。效率提升近100倍。

对于律所、财务公司、招投标代理等行业，这个工具可以节省大量人力成本。商业模式可以按页收费（0.2-0.5元/页），或者月包（1000-5000元/月）。

技术实现不难，核心是选择合适的Python库和设计好工作流程。我已经开源了完整代码，可以直接使用。
        """

        print("\n🚀 SEO内容矩阵生成器 v2.0")
        print("=" * 50)

        matrix = generate_content_matrix(demo_content)

        print(f"\n📊 自动提取关键词：{', '.join(matrix['auto_keywords'])}")
        print(f"📝 关键观点：{matrix['key_points_count']}个")
        print(f"📱 覆盖平台：{', '.join(matrix['platforms'].keys())}")
        print(f"📦 生成内容：{matrix['total_content_count']}条")

        save_matrix(matrix, "output/content_matrix.json")
        save_matrix(matrix, "output/content_matrix.json", fmt="markdown")

        # 预览
        print("\n" + "=" * 50)
        print("内容预览：")
        for plat, contents in matrix["platforms"].items():
            print(f"\n【{plat}】({len(contents)}条)")
            for c in contents[:2]:
                print(f"  📌 {c['title'][:50]}")


if __name__ == "__main__":
    main()
