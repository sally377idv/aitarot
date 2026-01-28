// 塔罗牌图片服务 - 专门处理塔罗牌相关的图片逻辑

import { preloadImages, createImagePlaceholder } from './imageService'

// 塔罗牌图片配置
export const TAROT_CARD_IMAGE_CONFIG = {
  // 基础配置
  aspectRatio: '2:3', // 标准塔罗牌宽高比
  defaultSize: { width: 200, height: 300 },
  thumbnailSize: { width: 100, height: 150 },
  
  // 动画配置
  flipDuration: 500, // 翻转动画时长(ms)
  drawAnimationDelay: 300, // 抽牌动画间隔
}

// 获取塔罗牌图片URL（别名，用于向后兼容）
export function getCardImageUrl(cardId: string): string {
  return getTarotCardImage(cardId)
}

// 获取塔罗牌图片URL
export function getTarotCardImage(cardId: string): string {
  const baseName = TAROT_CARD_IMAGES[cardId] || 'default'
  return `images/tarot/${baseName}.webp`
}

// 获取塔罗牌背图片
export function getCardBackImage(): string {
  return '/images/tarot/tarot-back.jpg' // 统一的牌背设计
}

// 临时塔罗牌图片映射（后续从imageService统一管理）
const TAROT_CARD_IMAGES: Record<string, string> = {
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

// 预加载当前牌阵所需的图片
export async function preloadTarotCards(cardIds: string[]): Promise<void> {
  return preloadImages(cardIds)
}

// 创建塔罗牌占位图
export function getCardPlaceholder(cardName: string): string {
  return createImagePlaceholder(cardName)
}

// 异步加载单张塔罗牌图片
export async function loadCardImage(cardId: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.src = getTarotCardImage(cardId)
    img.onload = () => resolve(img)
    img.onerror = () => reject(new Error(`Failed to load image for card: ${cardId}`))
  })
}

// 批量加载塔罗牌图片（优化版本）
export async function loadTarotCardImages(cardIds: string[]): Promise<Map<string, HTMLImageElement>> {
  const imageMap = new Map()
  const uniqueCardIds = [...new Set(cardIds)]
  
  const promises = uniqueCardIds.map(async (cardId) => {
    try {
      const img = await loadCardImage(cardId)
      imageMap.set(cardId, img)
    } catch (error) {
      console.warn(`Failed to load image for card ${cardId}:`, error)
      // 创建一个空的Image作为占位符
      const placeholder = new Image()
      placeholder.src = getCardPlaceholder(cardId)
      imageMap.set(cardId, placeholder)
    }
  })
  
  await Promise.all(promises)
  return imageMap
}

// 塔罗牌翻转动画的图片预加载
export function preloadCardFlipImages(cardId: string): void {
  // 预加载正反两面的图片
  const frontImage = new Image()
  const backImage = new Image()
  
  frontImage.src = getTarotCardImage(cardId)
  backImage.src = getCardBackImage() // 使用统一的牌背图片函数
  
  // 静默加载，不处理结果
}

// 检查图片加载状态
export async function checkImageAvailability(cardId: string): Promise<boolean> {
  return new Promise((resolve) => {
    const img = new Image()
    img.onload = () => resolve(true)
    img.onerror = () => resolve(false)
    img.src = getTarotCardImage(cardId)
    // 设置超时检查
    setTimeout(() => resolve(false), 2000)
  })
}

// 图片加载状态管理器
export class TarotImageManager {
  private loadedImages: Map<string, HTMLImageElement> = new Map()
  private loadingPromises: Map<string, Promise<HTMLImageElement>> = new Map()
  
  // 加载图片并缓存
  async loadCardImage(cardId: string): Promise<HTMLImageElement> {
    if (this.loadedImages.has(cardId)) {
      return this.loadedImages.get(cardId)!
    }
    
    if (this.loadingPromises.has(cardId)) {
      return this.loadingPromises.get(cardId)!
    }
    
    const promise = loadCardImage(cardId)
    this.loadingPromises.set(cardId, promise)
    
    try {
      const image = await promise
      this.loadedImages.set(cardId, image)
      this.loadingPromises.delete(cardId)
      return image
    } catch (error) {
      this.loadingPromises.delete(cardId)
      throw error
    }
  }
  
  // 预加载一组牌
  async preloadCards(cardIds: string[]): Promise<void> {
    const uniqueCardIds = cardIds.filter(id => !this.loadedImages.has(id))
    if (uniqueCardIds.length === 0) return
    
    await Promise.all(uniqueCardIds.map(id => this.loadCardImage(id)))
  }
  
  // 清除缓存（用于内存管理）
  clearCache(): void {
    this.loadedImages.clear()
    this.loadingPromises.clear()
  }
  
  // 获取已加载的图片
  getLoadedImage(cardId: string): HTMLImageElement | undefined {
    return this.loadedImages.get(cardId)
  }
}

// 创建全局图片管理器实例
export const tarotImageManager = new TarotImageManager()