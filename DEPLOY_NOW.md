# 🔥 立即部署指南 - SEO内容矩阵 HF Space

## 子宇，5分钟搞定，立即开始获客！

---

## 方案1：更新现有 HF Space（推荐）

你的现有 Space：https://zhangyu0806-ziyu-openclaw-ai.hf.space
当前状态：Preparing Space（需要部署）

### 步骤

**1. 准备文件**

```bash
cd /root/.openclaw/workspace/gtd/010-Project/active/SEO内容矩阵

# 确保 README_HF.md 内容正确
cat README_HF.md

# 确保 app_streamlit.py 存在
ls -la app_streamlit.py
```

**2. 获取 HF Token**
- 访问：https://huggingface.co/settings/tokens
- 创建新 token（需要 Write 权限）
- 复制 token

**3. 登录并推送**

```bash
# 安装 git-lfs（如果没装）
apt-get install git-lfs -y
git lfs install

# 登录 HuggingFace（输入你的token）
huggingface-cli login

# 添加远程仓库
git remote add hf https://huggingface.co/spaces/zhangyu0806/ziyu-openclaw-ai

# 推送
git push hf main
```

**4. 等待构建**
- 访问：https://huggingface.co/spaces/zhangyu0806/ziyu-openclaw-ai
- 等待 2-5 分钟，Space 会自动构建
- 构建完成后，访问 https://zhangyu0806-ziyu-openclaw-ai.hf.space

---

## 方案2：创建新 HF Space

如果方案1有问题，创建新 Space：

### 步骤

**1. 访问 HuggingFace**
- 打开：https://huggingface.co
- 点击右上角 "+" → "New Space"

**2. 填写信息**
- Space name: `seo-content-matrix`（或其他）
- License: MIT
- SDK: **Streamlit**
- Hardware: **CPU basic**（免费）
- Visibility: **Public**

**3. 创建后，获取 Git URL**

**4. 本地推送**

```bash
cd /root/.openclaw/workspace/gtd/010-Project/active/SEO内容矩阵

# 复制 README_HF.md 为 README.md（HF需要）
cp README_HF.md README.md

# 添加远程（替换YOUR_USERNAME）
git remote add seo-hf https://huggingface.co/spaces/YOUR_USERNAME/seo-content-matrix

# 推送
git push seo-hf main
```

---

## 文件清单（必须包含）

```
SEO内容矩阵/
├── app_streamlit.py      # Streamlit应用（必须）
├── content_splitter.py   # 核心引擎（必须）
├── requirements.txt      # Python依赖（必须）
├── README.md            # HF说明（必须，用README_HF.md内容）
└── （其他文件可选）
```

---

## requirements.txt 内容

```txt
streamlit>=1.28.0
pandas>=2.0.0
jieba>=0.42.1
scikit-learn>=1.3.0
```

---

## 部署成功后

### 立即测试
1. 访问你的 Space URL
2. 输入测试文本
3. 点击生成
4. 确认有输出

### 通知 AI
告诉我你的演示站 URL，格式：
```
演示站已部署：https://xxxxx.hf.space
```

我会立即：
1. 更新推广材料中的 URL
2. 准备发布小红书推广文
3. 准备客户联系邮件

---

## 常见问题

### Q: 推送失败？
A: 检查 token 权限，确保有 Write 权限

### Q: 构建失败？
A: 查看 HF Space 的 Settings → Logs，检查错误信息

### Q: 页面显示 "Preparing Space"？
A: 正在构建，等待 2-5 分钟

### Q: 没有 huggingface-cli？
A: 安装：pip install huggingface_hub

---

**预计耗时**：5-10分钟
**难度**：⭐⭐☆☆☆

---

*子宇，等你部署完成，我们立即开始获客！* 🚀
