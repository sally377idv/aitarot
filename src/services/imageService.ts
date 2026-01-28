// 图片服务和塔罗牌图片URL管理

// 图片根路径配置（可用于切换本地/云端）
// 临时解决方案：直接使用相对路径，Vercel部署时可配置环境变量
const IMAGE_BASE_URL = '/images/tarot'

// 支持的图片格式和降级策略
const SUPPORTED_FORMATS = ['webp', 'jpg', 'png']
const PREFERRED_FORMAT = 'webp'

// 塔罗牌图片映射表
export const TAROT_CARD_IMAGES: Record<string, string> = {
  // 大阿卡纳
  'fool': 'fool',
  'magician': 'magician',
  'high-priestess': 'high-priestess',
  'empress': 'empress',
  'emperor': 'emperor',
  
  // 圣杯牌组
  'ace-cups': 'ace-cups',
  'two-cups': 'two-cups',
  
  // 宝剑牌组
  'ace-swords': 'ace-swords',
  
  // 权杖牌组
  'ace-wands': 'ace-wands',
  
  // 星币牌组
  'ace-pentacles': 'ace-pentacles'
}

// 获取塔罗牌图片URL
export function getTarotCardImage(cardId: string): string {
  const baseName = TAROT_CARD_IMAGES[cardId] || 'default'
  return `${IMAGE_BASE_URL}/${baseName}.${PREFERRED_FORMAT}`
}

// 预加载图片
export async function preloadImages(cardIds: string[]): Promise<void> {
  const uniqueCardIds = [...new Set(cardIds)]
  
  const preloadPromises = uniqueCardIds.map(cardId => {
    return new Promise<void>((resolve) => {
      const img = new Image()
      img.src = getTarotCardImage(cardId)
      img.onload = () => resolve()
      img.onerror = () => resolve() // 忽略加载失败，使用默认占位图
    })
  })
  
  await Promise.all(preloadPromises)
}

// 检测浏览器支持的图片格式
export function getSupportedFormat(): string {
  // 在实际应用中，这里可以通过特性检测决定使用哪种格式
  // 目前简单返回优先格式，实际部署时可根据浏览器特性调整
  return PREFERRED_FORMAT
}

// 创建图片占位符（用于加载中状态）
export function createImagePlaceholder(cardName: string): string {
  // 使用CSS创建简单的占位符
  return `data:image/svg+xml,${encodeURIComponent(`
    <svg width="200" height="300" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" fill="#f0f4f8"/>
      <text x="50%" y="50%" text-anchor="middle" dy="0.3em" font-family="Arial" font-size="16" fill="#8b5cf6">
        ${cardName}
      </text>
    </svg>
  `)}`
}

// 图片懒加载辅助函数
export function lazyLoadImage(element: HTMLImageElement, cardId: string): void {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target as HTMLImageElement
        img.src = getTarotCardImage(cardId)
        img.classList.remove('lazy')
        observer.unobserve(img)
      }
    })
  })
  
  observer.observe(element)
}

// 批量更新所有塔罗牌的图片URL
export function updateTarotCardsWithImages(tarotCards: any[]): any[] {
  return tarotCards.map(card => ({
    ...card,
    imageUrl: getTarotCardImage(card.id)
  }))
}

// 环境配置检查
export function checkImageConfig(): { baseUrl: string; format: string; status: string } {
  return {
    baseUrl: IMAGE_BASE_URL,
    format: PREFERRED_FORMAT,
    status: IMAGE_BASE_URL.includes('http') ? '云端部署' : '本地部署'
  }
}