# 🚀 Vercel部署操作指南

## 📋 前置要求
- [ ] GitHub账户
- [ ] Vercel账户（可免费注册）
- [ ] 本地代码已准备好

## 🔄 完整部署流程

### 步骤1：创建GitHub仓库
```bash
# 1. 初始化Git仓库
git init
git add .
git commit -m "feat: AI塔罗-心灵奇旅Web应用 v1.0.0"

# 2. 在GitHub.com创建新仓库
#   仓库名：ai-tarot-app
#   可见性：Public（免费）或 Private

# 3. 关联远程仓库
git remote add origin https://github.com/YOUR_USERNAME/ai-tarot-app.git
git branch -M main
git push -u origin main
```

### 步骤2：Vercel部署（Web界面）

1. **登录Vercel**
   - 访问 [vercel.com](https://vercel.com)
   - 使用GitHub账户登录

2. **导入项目**
   - 点击"New Project"按钮
   - 选择"Import Git Repository"
   - 授权访问GitHub账户
   - 找到并选择 `ai-tarot-app` 仓库

3. **配置项目**
   ```
   Project Name: ai-tarot-app (自动生成)
   Framework Preset: Vite (自动检测)
   Root Directory: ./
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

4. **环境变量验证**
   - 确保Vercel自动读取了`vercel.json`中的配置
   - 或手动添加：
     ```
     VITE_DEEPSEEK_API_KEY=sk-d20e3e5963754634ab8d9d391bf5bd3d
     VITE_IMAGE_BASE_URL=/images/tarot
     ```

5. **部署**
   - 点击"Deploy"按钮
   - 等待构建完成（约1-2分钟）

### 步骤3：获取生产URL

部署成功后，Vercel会提供：
```
主域名：https://ai-tarot-app.vercel.app
备用域名：https://ai-tarot-app-git-main-YOUR_USERNAME.vercel.app
```

### 步骤4：测试生产环境

1. **功能测试**
   - 访问生产URL
   - 测试完整流程：主页 → 抽牌 → 解读 → 追问
   - 验证AI功能正常

2. **性能检查**
   - 检查页面加载速度
   - 测试移动端响应式
   - 验证图片和资源加载

## ⚙️ Vercel配置详情

### 自动构建配置（vercel.json）
```json
{
  "version": 2,
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### 环境变量管理
| 变量名 | 值 | 说明 |
|-------|----|------|
| VITE_DEEPSEEK_API_KEY | sk-d20e3e5963754634ab8d9d391bf5bd3d | AI服务密钥 |
| VITE_IMAGE_BASE_URL | /images/tarot | 图片资源路径 |

## 🔧 故障排除

### 常见问题

**1. 构建失败**
```bash
# 检查本地构建
npm run build

# 查看构建日志
复制错误信息到GitHub Issues
```

**2. 路由问题（刷新404）**
- ✅ 已配置SPA重写规则
- 确保所有路由指向index.html

**3. API调用失败**
- 检查网络连接
- 验证API密钥有效性
- 查看浏览器控制台错误

**4. 图片加载失败**
- 确保图片路径正确
- 检查CDN配置

### 性能优化建议

1. **图片优化**
   ```bash
   # 上传图片到Vercel的Edge Network
   # 或使用专业CDN服务
   ```

2. **缓存策略**
   ```json
   // 在vercel.json中添加headers
   "headers": [
     {
       "source": "/(.*)",
       "headers": [
         { "key": "Cache-Control", "value": "public, max-age=3600" }
       ]
     }
   ]
   ```

## 📱 域名自定义（可选）

### 添加自定义域名
1. Vercel项目设置 → Domains
2. 添加您的域名（如：tarot.yourdomain.com）
3. 配置DNS记录
4. 等待SSL证书自动生成

### 免费子域名
```
https://ai-tarot-app.vercel.app
https://your-app-name.vercel.app
```

## 🔄 更新部署

### 代码更新流程
```bash
# 1. 本地修改代码
git add .
git commit -m "feat: 新功能描述"

# 2. 推送到GitHub
git push origin main

# 3. Vercel自动重新部署
# 检查部署状态：Vercel Dashboard → Deployments
```

### 版本回滚
- Vercel Dashboard → Deployments
- 选择之前的部署版本
- 点击"Promote to Production"

## 📊 监控和分析

### Vercel Analytics
- 自动提供性能监控
- 查看访问统计
- 分析页面加载时间

### 自定义监控
```javascript
// 添加用户行为跟踪
// 在代码中使用 Google Analytics 或其他分析工具
```

## 🎯 部署完成检查清单

- [ ] GitHub仓库创建并推送
- [ ] Vercel项目导入成功
- [ ] 构建过程无错误
- [ ] 生产环境功能正常
- [ ] AI服务调用成功
- [ ] 移动端响应式正常
- [ ] 图片资源加载正常
- [ ] 自定义域名配置（可选）
- [ ] 性能监控设置

---

## ?? 支持资源

- **Vercel文档**: https://vercel.com/docs
- **GitHub Issues**: 报告部署问题
- **项目README**: 查看详细使用说明

**部署成功后，您的AI塔罗应用就可以通过互联网访问了！🎉**]]