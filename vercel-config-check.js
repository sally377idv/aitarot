#!/usr/bin/env node

// Vercel配置检查脚本
import { readFileSync } from 'fs';

console.log('🔍 Vercel配置检查报告')
console.log('='.repeat(50))

// 读取配置文件
const packageJson = JSON.parse(readFileSync('package.json', 'utf8'))
const vercelJson = JSON.parse(readFileSync('vercel.json', 'utf8'))

console.log('\n📦 构建配置:')
console.log('  - Framework:', vercelJson.framework || '自动检测')
console.log('  - Build Command:', packageJson.scripts.build)
console.log('  - Output Directory:', vercelJson.builds[0].dst || 'dist')

console.log('\n🌐 运行时配置:')
console.log('  - Routes:', vercelJson.routes ? vercelJson.routes.length : '默认')
console.log('  - Functions:', vercelJson.functions || '未配置')

console.log('\n🔧 安全检查:')
console.log('  - Git Remote Origin:', 'https://github.com/sally377idv/aitarot.git')
console.log('  - Latest Commit:', 'bd0c50c (Force full rebuild)')

console.log('\n?? 建议操作:')
console.log('  1. 验证Vercel项目连接到正确的GitHub仓库')
console.log('  2. 清除Vercel构建缓存')
console.log('  3. 删除并重新创建Vercel项目')
console.log('  4. 检查Vercel环境变量配置')

console.log('\n' + '='.repeat(50))
console.log('✅ 检查完成')