# AI塔罗-心灵奇旅 部署指南

## 🌐 快速部署方案

### 方案一：Vercel部署（推荐）

**步骤：**
1. **准备代码仓库**
   ```bash
   git init
   git add .
   git commit -m "initial commit"
   git branch -M main
   ```

2. **推送到GitHub**
   ```bash
   # 在GitHub创建新仓库
   git remote add origin https://github.com/yourname/ai-tarot-app.git
   git push -u origin main
   ```

3. **部署到Vercel**
   - 访问 [vercel.com](https://vercel.com)
   - 使用GitHub账户登录
   - 导入项目仓库
   - 配置环境变量（可选）
   - 点击部署，自动获得生产URL

4. **配置环境变量（推荐）**
   ```
   VITE_DEEPSEEK_API_KEY=sk-d20e3e5963754634ab8d9d391bf5bd3d
   VITE_IMAGE_BASE_URL=https://your-cdn.com/images/tarot
   ```

### 方案二：Netlify部署

**步骤：**
1. 同样先推送到GitHub仓库
2. 访问 [netlify.com](https://netlify.com)
3. 导入GitHub仓库
4. 构建命令：`npm run build`
5. 发布目录：`dist`
6. 获得生产URL

### 方案三：传统服务器部署

**步骤：**
1. **构建生产版本**
   ```bash
   npm run build
   ```

2. **上传文件**
   - 将 `dist/` 目录上传到Web服务器
   - 配置服务器支持SPA路由
   - 设置正确的MIME类型

3. **配置CDN（推荐）**
   - 将图片资源上传到CDN
   - 更新图片基础URL配置

## 📁 生产环境配置

### 环境变量设置
创建 `.env.production` 文件：
```env
VITE_DEEPSEEK_API_KEY=sk-d20e3e5963754634ab8d9d391bf5bd3d
VITE_IMAGE_BASE_URL=https://cdn.yourdomain.com/images/tarot
VITE_APP_ENV=production
```

### 图片资源部署
1. **准备图片文件结构：**
   ```
   images/tarot/
   ├── fool.jpg / fool.webp
   ├── magician.jpg / magician.webp
   ├── high-priestess.jpg / high-priestess.webp
   └── tarot-back.jpg
   ```

2. **上传到CDN：**
   - 推荐使用：阿里云OSS、腾讯云COS、CloudFlare
   - 配置域名和HTTPS
   - 启用缓存和压缩

### 域名配置
获取部署URL后，可配置自定义域名：
- 在DNS添加CNAME记录指向部署平台
- 配置SSL证书（大部分平台自动提供）

## 🛠️ 部署脚本

### 自动构建脚本
创建 `deploy.sh`：
```bash
#!/bin/bash

echo "开始构建生产版本..."
npm run build

echo "检查构建结果..."
if [ -d "dist" ]; then
    echo "✅ 构建成功"
    echo "文件大小: $(du -sh dist)"
else
    echo "❌ 构建失败"
    exit 1
fi

echo "部署完成，访问地址：https://your-app.vercel.app"
```

### Docker部署（可选）
创建 `Dockerfile`：
```dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 🔧 部署后验证

### 功能检查清单
- [ ] 主页加载正常，样式正确
- [ ] 塔罗牌图片加载（使用CDN）
- [ ] AI解读功能正常调用
- [ ] 移动端响应式设计
- [ ] 页面路由正常工作
- [ ] 错误处理页面

### 性能测试
```bash
# 使用Lighthouse测试
npm install -g lighthouse
lighthouse https://your-app.vercel.app --view
```

## 🚨 常见问题解决

### 路由问题
**症状：** 刷新页面显示404
**解决：** 配置服务器将所有路由重定向到index.html

### 图片加载失败
**解决：** 
1. 检查CDN配置和图片路径
2. 确保图片格式支持
3. 验证CORS设置

### API调用失败
**解决：**
1. 验证API密钥是否正确
2. 检查网络连接和防火墙
3. 查看浏览器控制台错误信息

## 📊 监控和分析

### 推荐工具
- **Google Analytics**：用户行为分析
- **Vercel Analytics**：性能监控
- **Sentry**：错误追踪

### 自定义监控
在代码中添加：
```javascript
// 错误监控
window.onerror = function(msg, url, lineNo, columnNo, error) {
  // 发送到监控服务
  console.error('应用错误:', error)
}
```

## 🔄 更新部署

### 常规更新流程
1. 本地测试新功能
2. 推送到GitHub
3. 部署平台自动重新构建
4. 验证生产环境

### 零停机部署
- Vercel/Netlify自动支持蓝绿部署
- 新版本部署成功后自动切换流量

## 📞 支持联系

**问题报告：**
- GitHub Issues：提交代码问题
- 邮件支持：support@yourdomain.com
- 文档更新：更新此文档

---

**部署状态检查清单：**
- [ ] 代码推送到GitHub
- [ ] 部署平台配置完成
- [ ] 环境变量设置正确
- [ ] 图片CDN配置完成
- [ ] 域名解析生效
- [ ] 功能测试通过
- [ ] 性能优化完成

**完成以上步骤后，您的AI塔罗应用就正式上线了！✨**