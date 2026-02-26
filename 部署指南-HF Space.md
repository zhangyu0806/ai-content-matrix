# HF Space 部署指南 - SEO内容矩阵项目

## 📋 部署清单

子宇，以下是部署到HuggingFace Space的完整步骤（预计5分钟完成）：

---

## 第1步：登录HuggingFace（1分钟）

1. 访问：https://huggingface.co
2. 登录你的账号
3. 如果没有账号，先注册（免费）

---

## 第2步：创建新Space（1分钟）

1. 点击右上角 `+` → `New Space`
2. 填写信息：
   - **Owner**: 选择你的账号
   - **Space name**: `seo-content-matrix`（或其他名称）
   - **License**: MIT
   - **SDK**: Streamlit
   - **Hardware**: CPU basic（免费）

3. 点击 `Create Space`

---

## 第3步：上传文件（2分钟）

### 方法A：通过Git上传（推荐）

```bash
cd /root/.openclaw/workspace/gtd/010-Project/active/SEO内容矩阵

# 初始化git（如果还没有）
git init

# 添加远程仓库（替换YOUR_USERNAME）
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/seo-content-matrix

# 添加文件
git add app_streamlit.py content_splitter.py README_HF.md requirements.txt

# 提交
git commit -m "Initial commit: AI Content Matrix Generator v3.0"

# 推送
git push hf main
```

### 方法B：通过Web界面上传

1. 在Space页面点击 `Files`
2. 依次上传以下文件：
   - `app_streamlit.py`
   - `content_splitter.py`
   - `README_HF.md`（重命名为`README.md`）
   - `requirements.txt`

---

## 第4步：等待构建（自动，约2-5分钟）

- HF会自动检测`requirements.txt`并安装依赖
- 构建日志会在页面显示
- 构建成功后，应用会自动启动

---

## 第5步：测试演示站

- 访问：`https://huggingface.co/spaces/YOUR_USERNAME/seo-content-matrix`
- 粘贴测试文本
- 点击生成
- 查看结果

---

## 📦 需要上传的文件清单

| 文件名 | 说明 | 必需 |
|--------|------|------|
| app_streamlit.py | Streamlit应用入口 | ✅ |
| content_splitter.py | 核心引擎 | ✅ |
| README_HF.md | Space说明（需重命名为README.md） | ✅ |
| requirements.txt | Python依赖 | ✅ |

**不需要上传的文件**：
- app.py（Flask版本，HF用Streamlit）
- demo_app.py（旧版本）
- __pycache__（自动生成）
- output/（临时输出）

---

## 🎯 部署后的URL

部署成功后，你会得到一个公开URL：
```
https://huggingface.co/spaces/YOUR_USERNAME/seo-content-matrix
```

这个URL可以：
- 分享给客户做演示
- 嵌入到官网
- 用于推广引流

---

## 🔄 更新应用

修改代码后，只需：
```bash
git add .
git commit -m "Update: 描述你的修改"
git push hf main
```

HF会自动重新构建和部署。

---

## ⚠️ 常见问题

### Q1: 构建失败怎么办？
A: 检查`requirements.txt`格式，每行一个包名

### Q2: 应用启动慢？
A: HF免费版冷启动需要1-2分钟，这是正常的

### Q3: 可以改用GPU吗？
A: 可以，但GPU需要付费订阅。CPU basic对本文工具足够

### Q4: 如何自定义域名？
A: HF Space支持绑定自定义域名（在Settings中配置）

---

## 📊 预期效果

部署完成后48小时内：
- 访问量：50-200次
- 演示咨询：2-5个
- 转化测试：1-3个

---

## ✅ 完成后请通知AI

部署完成后，请告诉我：
1. Space的公开URL
2. 是否需要生成推广文章链接
3. 是否需要准备演示脚本

然后我们可以立即开始推广！

---

*预计总耗时：5-10分钟*
*难度：⭐⭐☆☆☆*
