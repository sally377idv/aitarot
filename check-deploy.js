#!/usr/bin/env node

// 部署状态检查脚本
import { readFileSync } from 'fs';

console.log('🚀 部署状态检查报告')
console.log('='.repeat(50))

try {
  const packageJson = JSON.parse(readFileSync('package.json', 'utf8'))
  const vercelJson = JSON.parse(readFileSync('vercel.json', 'utf8'))

  console.log('\n📦 项目配置:')
  console.log('  - 项目名称:', packageJson.name)
  console.log('  - GitHub仓库:', 'sally377idv/aitarot')
  console.log('  - 最新提交:', 'bd0c50c (Force full rebuild)')

  console.log('\n🔧 Vercel配置:')
  console.log('  - Framework:', vercelJson.framework || '自动检测')
  console.log('  - Build Command:', packageJson.scripts.build)
  
  console.log('\n📊 路由配置:')
  if (vercelJson.routes && vercelJson.routes.length > 0) {
    console.log('  - SPA重写规则:', vercelJson.routes.length + '条')
  } else {
    console.log('  - 路由: 使用框架默认配置')
  }

  console.log('\n⚠️ 潜在问题排查:')
  console.log('  1. Vercel缓存问题 → 清除构建缓存')
  console.log('  2. 分支关联问题 → 检查GitHub连接')
  console.log('  3. 环境配置差异 → 对比.env变量')
  console.log('  4. 网络延迟问题 → 等待缓存刷新')

  console.log('\n🎯 立即操作建议:')
  console.log('  - 访问: https://vercel.com/sally377idv/aitarot/deployments')
  console.log('  - 检查最近的部署是否使用commit: bd0c50c')
  console.log('  - 清除Vercel构建缓存重新部署')

} catch (error) {
  console.log('❌ 配置文件读取错误:', error.message)
}

console.log('\n' + '='.repeat(50))
console.log('📍 生产URL: https://aitarot2026.vercel.app')
console.log('✅ 检查完成')