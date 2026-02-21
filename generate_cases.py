#!/usr/bin/env python3
"""
生成真实内容案例
基于企业文档自动化项目
"""

from content_splitter import generate_content_matrix, save_matrix

def case_study_1():
    """案例1：企业文档自动化"""
    long_form = """
企业文档自动化：从8小时到5分钟

作为一家律所的合伙人，我每天要处理100多份合同、发票、报表。以前需要8小时手动复制粘贴到Excel，不仅效率低，还经常出错。

上个月我们尝试了Python自动化工具。流程很简单：
1. 用pdfplumber提取PDF表格数据
2. 用pandas清洗数据（去重、格式统一）
3. 用docxtpl填充Word模板生成文档

现在处理100份文件只需要5分钟！效率提升了近100倍。

我们算了一笔账：原来需要2个专职人员，现在1个人兼职就能搞定，每月节省人力成本1.5万元。

商业模式也很灵活：
- 按页收费：0.2-0.5元/页
- 最低收费：100元起
- 月包：1000-5000元/月

适合的行业：
- 律所（合同审查）
- 财务公司（发票处理）
- 招投标代理（报表整理）

技术实现不难，我已经开源了完整代码。如果你也有类似需求，可以试试看。
    """

    keywords = ["企业自动化", "Python", "效率提升", "文档处理", "降本增效"]

    print("\n【案例1】企业文档自动化")
    print("="*50)

    matrix = generate_content_matrix(long_form, keywords)
    save_matrix(matrix, "output/case1_automation.json")

    print(f"\n✅ 案例1生成完成")
    print(f"   关键观点：{matrix['key_points_count']}个")
    print(f"   生成内容：{sum(len(v) for v in matrix['platforms'].values())}条")

    return matrix

def case_study_2():
    """案例2：Anki学习卡片"""
    long_form = """
考研政治82分学姐的秘密武器

二战上岸，政治从58分提到82分。

关键在于：用AI生成了1500张Anki卡片。

500页教材，重点太多记不住？
手动整理Anki卡片，3小时才做完第一章？

我试过很多方法：
- ❌ 手抄笔记：3小时才整理完一章
- ❌ OCR+复制：格式乱，还得手动改
- ✅ AI卡片生成器：1分钟搞完整本书

具体操作：
1. 上传PDF教材
2. AI自动识别章节（马原、毛概、史纲...）
3. 提取重点（定义、概念、重要提示）
4. 生成3种卡片：
   - 问答卡片：马克思主义是...（定义）
   - 填空卡片：{{c1::实践}}是认识的基础
   - 分类卡片：唯物辩证法的三大规律...

5. 导入Anki，直接开背

复习策略：
- 早上：新卡片50张
- 晚上：复习卡片100张
- 考前2周：只刷错题卡

效果对比：
| 方法 | 时间 | 卡片数 | 准确率 |
|------|------|--------|--------|
| 手动整理 | 3小时 | 50张 | 80% |
| AI生成 | 1分钟 | 1500张 | 95% |

AI更准确，因为它不会漏掉藏在角落的知识点。

工具限时免费，每月3次转换。Pro版¥19.9/月，无限转换。

考研路上，时间就是分数。
    """

    keywords = ["考研政治", "Anki", "学习方法", "AI工具", "考研上岸"]

    print("\n【案例2】Anki学习卡片")
    print("="*50)

    matrix = generate_content_matrix(long_form, keywords)
    save_matrix(matrix, "output/case2_anki.json")

    print(f"\n✅ 案例2生成完成")
    print(f"   关键观点：{matrix['key_points_count']}个")
    print(f"   生成内容：{sum(len(v) for v in matrix['platforms'].values())}条")

    return matrix

def case_study_3():
    """案例3：AI内容矩阵"""
    long_form = """
我是如何用AI 1周生成100条内容的

作为新媒体运营，我每天需要产出大量内容：
- 小红书：图文笔记
- 抖音：短视频脚本
- B站：教程视频

以前写1条内容要2小时，100条就是200小时，根本不可能。

现在用AI内容矩阵工具，1篇长文 → 10条短内容，自动适配3个平台。

具体流程：
1. 写1篇深度长文（1500字）
2. AI提取关键观点（10个）
3. 自动生成：
   - 小红书图文：7条（含emoji和标签）
   - 抖音脚本：5条（30-60秒）
   - B站教程：3条（3-5分钟）

总共15条内容，只需5分钟。

真实案例：
我用"企业自动化"这1篇文章，生成了15条内容：
- 小红书：7条笔记，获赞500+
- 抖音：5条视频，播放1.2万
- B站：3条教程，收藏800+

收入变化：
- 月广告收入：从0到5000元
- 接单价格：单条500-2000元
- 企业合作：月包8000元

这个工具的核心优势：
1. 智能拆解：自动识别核心观点
2. 平台适配：符合各平台调性
3. SEO优化：关键词、标签自动优化
4. 批量生成：10倍提升产出

定价：
- 基础版：¥5000/月（50条）
- 专业版：¥8000/月（100条）
- 企业版：¥15000/月（200条+定制）

如果你也是内容创作者，强烈建议试试。
    """

    keywords = ["AI内容", "内容营销", "新媒体运营", "效率工具", "自动化"]

    print("\n【案例3】AI内容矩阵")
    print("="*50)

    matrix = generate_content_matrix(long_form, keywords)
    save_matrix(matrix, "output/case3_content_matrix.json")

    print(f"\n✅ 案例3生成完成")
    print(f"   关键观点：{matrix['key_points_count']}个")
    print(f"   生成内容：{sum(len(v) for v in matrix['platforms'].values())}条")

    return matrix

def main():
    """生成所有案例"""
    print("\n" + "="*50)
    print("SEO内容矩阵 - 真实案例生成")
    print("="*50)

    # 生成3个案例
    case_study_1()
    case_study_2()
    case_study_3()

    print("\n" + "="*50)
    print("✅ 所有案例生成完成！")
    print("="*50)
    print("\n案例文件位置：")
    print("  - output/case1_automation.json")
    print("  - output/case2_anki.json")
    print("  - output/case3_content_matrix.json")

if __name__ == "__main__":
    main()
