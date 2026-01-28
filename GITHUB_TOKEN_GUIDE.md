# 🔑 GitHub个人访问令牌（PAT）获取和使用指南

由于GitHub不再支持密码认证，需要使用个人访问令牌（Personal Access Token）来推送代码。

## 📋 获取GitHub Token步骤

### 步骤1：访问Token生成页面
1. 打开 https://github.com/settings/tokens
2. 登录您的GitHub账户（sally377idv）
3. 点击"Generate new token" → "Generate new token (classic)"

### 步骤2：配置Token权限
- **Note（备注）**: `AI塔罗应用部署`
- **Expiration（有效期）**: 建议选择"90 days"或"Custom"设置更长时间
- **Select scopes（权限范围）**:
  - ✅ `repo` (全权限，包括代码推送)
  - ✅ `workflow` (可选，用于GitHub Actions)
  - ✅ `write:packages` (可选，用于包管理)

### 步骤3：生成并复制Token
- 点击"Generate token"
- **立即复制Token**（只会显示一次！）
- Token示例：`ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## 🚀 使用Token推送代码

### 方法一：命令行直接使用（推荐）
```bash
# 替换YOUR_TOKEN为实际Token
git push https://ghp_YOUR_TOKEN@github.com/sally377idv/ai-tarot-app.git main
```

### 方法二：配置凭据存储
```bash
# 1. 配置凭据存储
git config --global credential.helper store

# 2. 推送（会提示输入用户名和Token）
git push -u origin main
# 用户名：sally377idv
# 密码：粘贴您的Token
```

### 方法三：使用环境变量
```bash
# 临时设置环境变量
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
git push https://$GITHUB_TOKEN@github.com/sally377idv/ai-tarot-app.git main
```

## 🔒 Token安全提示

### 存储安全
- **不要将Token提交到代码仓库**
- **不要分享Token给他人**
- **定期更新Token**
- **使用.env文件存储（已配置在.gitignore中）**

### 权限管理
- 只授予最小必要权限
- 定期检查使用情况
- 及时撤销不需要的Token

## 🛠️ 自动部署脚本集成

如果您使用部署脚本，可以这样集成Token：

```bash
#!/bin/bash
# 在部署脚本中添加Token验证
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ 请设置GITHUB_TOKEN环境变量"
    echo "export GITHUB_TOKEN=your_token_here"
    exit 1
fi

# 使用Token推送
git push https://$GITHUB_TOKEN@github.com/sally377idv/ai-tarot-app.git main
```

## 📝 常见问题解决

### 错误：Authentication failed
- Token已过期 → 重新生成Token
- Token权限不足 → 检查repo权限
- Token格式错误 → 确保完整复制

### 错误：Repository not found
- 仓库不存在 → 确认GitHub仓库已创建
- 拼写错误 → 检查用户名和仓库名

### 错误：Permission denied
- Token权限问题 → 重新生成带repo权限的Token
- 账户问题 → 确认GitHub账户状态

## 🎯 成功标准

当出现以下输出时，表示推送成功：
```bash
Enumerating objects: 35, done.
Counting objects: 100% (35/35), done.
Writing objects: 100% (35/35), 8274 bytes | 8274.00 KiB/s, done.
Total 35 (delta 0), reused 0 (delta 0)
To https://github.com/sally377idv/ai-tarot-app.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

## 🌐 后续步骤

1. **验证GitHub仓库**：访问 https://github.com/sally377idv/ai-tarot-app
2. **Vercel部署**：在 vercel.com 导入仓库
3. **测试生产环境**：访问您的应用URL

## 📞 支持资源

- **GitHub Tokens文档**: https://docs.github.com/en/authentication
- **Git凭据存储**: https://git-scm.com/docs/git-credential-store
- **Vercel部署指南**: 参见项目中的VERCEL_DEPLOYMENT_GUIDE.md

**按照上述步骤操作，您的代码将成功推送到GitHub！**]]