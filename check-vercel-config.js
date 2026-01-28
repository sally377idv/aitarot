#!/usr/bin/env node

// 检查Vercel配置文件
import { readFileSync } from 'fs';

console.log('🔍 Vercel环境配置检查')
console.log('='.repeat(50))

try {
  const vercelJson = JSON.parse(readFileSync('vercel.json', 'utf8'))
  console.log('\n📋 vercel.json配置:')
  console.log('  📄 配置文件:', JSON.stringify(vercelJson, null, 2))
  
  if (vercelJson.env) {
    console.log('\n🧬 环境变量配置:')
    Object.keys(vercelJson.env).forEach(key => {
      const maskedValue = vercelJson.env[key].replace(/(.{4}).+(.{4})/, '$1***$2')
      console.log(`  🔑 ${key}: ${maskedValue}`)
    })
  }
  
  console.log('\n📍 关键配置检查:')
  const checks = [
    { name: 'Framework设置', value: vercelJson.framework === 'vite' },
    { name: '构建命令', value: vercelJson.buildCommand === 'npm run build' },
    { name: '输出目录', value: vercelJson.outputDirectory === 'dist' },
    { name: 'SPA重写规则', value: vercelJson.rewrites && vercelJson.rewrites.length > 0 }
  ]
  
  checks.forEach(check => {
    const icon = check.value ? '✅' : '❌'
    console.log(`  ${icon} ${check.name}: ${check.value ? '正确' : '需要检查'}`)
  })
  
} catch (error) {
  console.log('❌ 配置文件错误:', error.message)
}

console.log('\n' + '='.repeat(50))
console.log('⚠️ 提示: 请检查Vercel控制台中的实际环境变量配置')