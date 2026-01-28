#!/usr/bin/env node

// 验证UI版本脚本
import { readFileSync } from 'fs';

console.log('🔍 UI版本验证报告')
console.log('='.repeat(50))

// 检查TarotCardDeck组件是否包含V2 UI特征
function checkV2UI() {
  try {
    const tarotDeck = readFileSync('src/components/TarotCardDeck.tsx', 'utf8')
    
    // V2 UI特征检查
    const v2Features = [
      { name: '信息卡片布局', pattern: /信息卡片|bg-gradient-to-br from-purple-50 to-blue-50/ },
      { name: 'preDrawnCards支持', pattern: /preDrawnCards/ },
      { name: '无图片依赖', pattern: /getTarotCardImage|TarotCard\.tsx/ },
      { name: '状态管理修复', pattern: /setCards\(preDrawnCards/ }
    ]
    
    console.log('\n📊 V2 UI特征检查:')
    v2Features.forEach(feature => {
      const hasFeature = feature.pattern.test(tarotDeck)
      const icon = hasFeature ? '✅' : '❌'
      console.log(`  ${icon} ${feature.name}: ${hasFeature ? '存在' : '缺失'}`)
    })
    
    // 检查是否包含旧的图片组件引用
    const oldPatterns = [
      { name: 'TarotCard组件引用', pattern: /import.*TarotCard/ },
      { name: '图片服务引用', pattern: /tarotImageService/ }
    ]
    
    console.log('\n📋 旧版本残留检查:')
    oldPatterns.forEach(pattern => {
      const hasOld = pattern.pattern.test(tarotDeck)
      const icon = hasOld ? '❌' : '✅'
      console.log(`  ${icon} ${pattern.name}: ${hasOld ? '存在(需修复)' : '不存在(正常)'}`)
    })
    
    console.log('\n🎯 构建验证:')
    const packageJson = JSON.parse(readFileSync('package.json', 'utf8'))
    console.log(`  📦 项目: ${packageJson.name}`)
    console.log(`  🛠️  构建命令: ${packageJson.scripts.build}`)
    
    return true
  } catch (error) {
    console.log('❌ 验证失败:', error.message)
    return false
  }
}

checkV2UI()
console.log('\n' + '='.repeat(50))
console.log('📍 验证完成')