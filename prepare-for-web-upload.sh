#!/bin/bash

# 网页上传部署准备脚本
# 创建干净的ZIP文件，排除不需要的文件

echo "🚀 准备GitHub网页上传包..."
echo "========================================"

# 创建临时目录用于清理
TEMP_DIR="ai-tarot-app-upload"
mkdir -p "$TEMP_DIR"

# 复制需要的文件，排除不需要的
echo "📋 复制项目文件..."
cp -r src/ "$TEMP_DIR/src/"
cp -r dist/ "$TEMP_DIR/dist/" 2>/dev/null || echo "⚠️ dist目录不存在，跳过"
cp *.json "$TEMP_DIR/" 2>/dev/null
cp *.md "$TEMP_DIR/" 2>/dev/null
cp *.html "$TEMP_DIR/" 2>/dev/null
cp *.js "$TEMP_DIR/" 2>/dev/null
cp *.ts "$TEMP_DIR/" 2>/dev/null
cp *.css "$TEMP_DIR/" 2>/dev/null
cp *.config.* "$TEMP_DIR/" 2>/dev/null

# 排除不需要的文件
echo "🗑️ 清理不需要的文件..."
rm -rf "$TEMP_DIR/node_modules" 2>/dev/null
rm -rf "$TEMP_DIR/.git" 2>/dev/null
rm -rf "$TEMP_DIR/.comate" 2>/dev/null
rm -rf "$TEMP_DIR/.comate.backup" 2>/dev/null
rm -f "$TEMP_DIR/.env" 2>/dev/null
rm -f "$TEMP_DIR/aitarot0127.pdf" 2>/dev/null
rm -rf "$TEMP_DIR/specmode-init" 2>/dev/null

# 创建ZIP文件
echo "📦 创建压缩包..."
zip -r "ai-tarot-app.zip" "$TEMP_DIR" -x "*.DS_Store" "*.git*" "node_modules/*"

# 清理临时文件
rm -rf "$TEMP_DIR"

echo ""
echo "✅ 上传包准备完成！"
echo "📁 生成的文件: ai-tarot-app.zip"
echo ""
echo "📋 上传步骤："
echo "1. 访问 https://github.com/new"
echo "2. 创建仓库: ai-tarot-app"
echo "3. 选择 'Upload an existing file'"
echo "4. 上传 ai-tarot-app.zip 文件"
echo "5. 或者解压ZIP后拖拽文件夹上传"
echo ""
echo "📊 文件清单："
find . -name "*.ts" -o -name "*.tsx" -o -name "*.json" -o -name "*.md" -o -name "*.css" -o -name "*.html" | wc -l | xargs echo "项目文件数量："

echo "========================================"
echo "🎉 准备上传到GitHub！"