# 🌐 无Git命令行部署指南

由于您的系统Git工具暂时不可用，可以使用以下方法部署到Vercel。

## 📋 步骤概览

1. **下载并安装Xcode命令行工具**（系统已提示）
2. **使用ZIP文件上传到GitHub**
3. **在Vercel导入仓库**

## 🔧 详细操作步骤

### 步骤1：安装Xcode命令行工具
系统已弹出安装提示，请点击"安装"按钮，或手动下载：
- 打开App Store，搜索"Xcode"安装
- 或访问：https://developer.apple.com/xcode/

### 步骤2：准备项目文件
项目已准备就绪，所有文件都在 `/Users/sunkexin02/Desktop/my_project/` 目录中。

### 步骤3：创建GitHub仓库（网页操作）
1. 访问 [github.com](https://github.com)
2. 登录您的GitHub账户
3. 点击右上角"+" → "New repository"
4. 填写仓库信息：
   - **Repository name**: `ai-tarot-app`
   - **Description**: `AI塔罗-心灵奇旅Web应用`
   - **Visibility**: `Public`（免费使用）
   - **Initialize this repository with**: 保持空白
5. 点击"Create repository"

### 步骤4：上传文件到GitHub
在新建的仓库页面：
1. 点击"Add file" → "Upload files"
2. 将整个项目文件夹拖拽到上传区域
   - 选择 `/Users/sunkexin02/Desktop/my_project/` 中的所有文件
3. 添加提交信息：`feat: AI塔罗-心灵奇旅Web应用 v1.0.0`
4. 点击"Commit changes"

### 步骤5：Vercel部署
1. 访问 [vercel.com](https://vercel.com)
2. 使用GitHub账户登录
3. 点击"New Project"
4. 选择刚创建的仓库 `ai-tarot-app`
5. Vercel会自动检测配置：
   - Framework: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
6. 确认环境变量（已配置在vercel.json中）
7. 点击"Deploy"

## 🔄 备选方案：如果GitHub上传失败

### 方案A：使用GitHub Desktop
1. 下载 [GitHub Desktop](https://desktop.github.com/)
2. 安装后创建仓库并推送

### 方案B：使用其他Git客户端
- SourceTree
- GitKraken
- TortoiseGit

## 📊 部署验证

部署成功后，检查以下内容：

1. **访问生产URL**：`https://ai-tarot-app.vercel.app`
2. **功能测试**：
   - 主页加载
   - 问题输入
   - 抽牌功能
   - AI解读
   - 追问功能
3. **响应式测试**：手机端访问

## 🔧 故障排除

### 上传文件过大
- GitHub免费账户有文件大小限制
- 如果提示文件过大，删除 `node_modules/` 文件夹（构建时Vercel会重新安装）

### 环境变量问题
- 检查Vercel项目设置中的环境变量
- 确保API密钥正确配置

### 构建失败
- 查看Vercel的构建日志
- 确保 `package.json` 中的依赖正确

## 🎯 成功后的管理

### 更新应用
修复Git工具后，可以使用正常Git流程：
```bash
# 在项目目录
git add .
git commit -m "更新描述"
git push origin main
# Vercel会自动重新部署
```

### 自定义域名
在Vercel项目设置中添加自定义域名。

---

## 💡 重要提示

- **API密钥安全**：当前API密钥已硬编码，生产环境建议使用环境变量管理
- **图片资源**：目前使用占位符，后续可以上传真实塔罗牌图片
- **监控**：Vercel提供免费的性能监控和分析

**按照上述步骤操作，您可以在不使用Git命令行的情况下成功部署应用！**]]