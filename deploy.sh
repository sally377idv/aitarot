#!/bin/bash

# AI塔罗-心灵奇旅 Vercel部署脚本
# 执行此脚本快速部署到Vercel

echo "🚀 开始部署AI塔罗应用到Vercel..."
echo "========================================"

# 检查Git状态
if [ ! -d ".git" ]; then
    echo "❌ 当前目录不是Git仓库"
    echo "请先执行: git init"
    exit 1
fi

# 构建验证
echo "?? 验证构建..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ 构建失败，请检查错误信息"
    exit 1
fi

echo "✅ 构建验证成功"

# 检查Git远程仓库
REMOTE_URL=$(git remote get-url origin 2>/dev/null)

if [ -z "$REMOTE_URL" ]; then
    echo "⚠️  未设置Git远程仓库"
    echo "请先设置远程仓库: git remote add origin YOUR_REPO_URL"
    exit 1
fi

echo "🔗 远程仓库: $REMOTE_URL"

# 推送代码
echo "📤 推送代码到GitHub..."
git add .
git commit -m "feat: deploy to vercel - $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ 代码推送成功"
else
    echo "❌ 代码推送失败"
    exit 1
fi

# 部署指导
echo ""
echo "🎉 代码推送完成！"
echo "========================================"
echo "下一步操作："
echo ""
echo "1. 访问 https://vercel.com"
echo "2. 使用GitHub登录"
echo "3. 点击 'New Project'"
echo "4. 选择您的仓库: ai-tarot-app"
echo "5. 确认配置后点击 'Deploy'"
echo ""
echo "📱 部署完成后，应用将在以下地址访问："
echo "   https://ai-tarot-app.vercel.app"
echo ""
echo "💡 提示：Vercel会自动从vercel.json读取配置"
echo "========================================"

# 可选：使用Vercel CLI部署（如果已安装）
if command -v vercel &> /dev/null; then
    echo ""
    read -p "检测到Vercel CLI，是否直接部署？(y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🔧 使用Vercel CLI部署..."
        vercel --prod
    fi
else
    echo ""
    echo "💡 可选：安装Vercel CLI进行命令行部署"
    echo "   npm install -g vercel"
    echo "   然后执行: vercel --prod"
fi

echo ""
echo "✨ 部署脚本执行完成！"]]
