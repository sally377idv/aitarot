import { useState, useEffect } from 'react'
import { DrawnCard } from '../types'
import { getTarotCardImage, getCardBackImage } from '../services/tarotImageService'

interface TarotCardProps {
  card: DrawnCard
  showDetails?: boolean
  onCardClick?: (card: DrawnCard) => void
  className?: string
}

const TarotCard: React.FC<TarotCardProps> = ({ 
  card, 
  showDetails = false, 
  onCardClick,
  className = '' 
}) => {
  const [isFlipped, setIsFlipped] = useState(false)
  const [imageLoaded, setImageLoaded] = useState(false)
  const [imageError, setImageError] = useState(false)

  // 预加载图片
  useEffect(() => {
    const img = new Image()
    img.onload = () => setImageLoaded(true)
    img.onerror = () => setImageError(true)
    img.src = getTarotCardImage(card.id)
  }, [card.id])

  const handleCardClick = () => {
    if (onCardClick) {
      onCardClick(card)
    } else {
      setIsFlipped(!isFlipped)
    }
  }

  const getCardFullDescription = (drawnCard: DrawnCard): string => {
    const orientation = drawnCard.isReversed ? '逆位' : '正位'
    const meaning = drawnCard.isReversed ? drawnCard.reversed : drawnCard.upright
    return `${drawnCard.name} ${orientation} - ${meaning}`
  }

  return (
    <div 
      className={`relative w-48 h-80 cursor-pointer transition-transform duration-500 ${className}`}
      onClick={handleCardClick}
    >
      {/* 卡牌容器 */}
      <div className={`relative w-full h-full ${isFlipped ? 'rotate-y-180' : ''}`}>
        {/* 正面 - 牌面图案 */}
        <div className="absolute inset-0 bg-white rounded-xl shadow-lg border-2 border-yellow-400 overflow-hidden">
          {imageLoaded && !imageError ? (
            <>
              {/* 牌面图片 */}
              <div className="h-3/4 overflow-hidden">
                <img 
                  src={getTarotCardImage(card.id)}
                  alt={card.name}
                  className="w-full h-full object-cover"
                  onError={() => setImageError(true)}
                />
              </div>
              <div className="h-1/4 p-3">
                <h3 className="font-bold text-lg text-gray-800">{card.name}</h3>
                <p className="text-sm text-gray-600">{card.element}</p>
                <div className="flex gap-1 mt-1">
                  {card.keywords.map((keyword: string, index: number) => (
                    <span key={index} className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded">
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
            </>
          ) : (
            <div className="w-full h-full flex flex-col items-center justify-center bg-gradient-to-br from-purple-50 to-blue-50">
              {imageError ? (
                <div className="text-center">
                  <div className="text-4xl text-gray-400 mb-2">🃏</div>
                  <div className="text-sm text-gray-500">图片加载失败</div>
                </div>
              ) : (
                <div className="text-center">
                  <div className="w-12 h-12 border-4 border-purple-200 border-t-purple-600 rounded-full animate-spin mb-2"></div>
                  <div className="text-sm text-gray-500">加载中...</div>
                </div>
              )}
              <div className="mt-2 text-center">
                <h3 className="font-bold text-gray-700">{card.name}</h3>
                <p className="text-xs text-gray-500">{card.element}</p>
              </div>
            </div>
          )}
        </div>

        {/* 背面 - 塔罗牌背图案 */}
        <div className="absolute inset-0 rounded-xl shadow-lg backface-hidden rotate-y-180 overflow-hidden">
          <img 
            src={getCardBackImage()}
            alt="塔罗牌背"
            className="w-full h-full object-cover"
          />
        </div>
      </div>

      {/* 详细说明（如果需要展示） */}
      {showDetails && (
        <div className="mt-3 p-3 bg-white rounded-lg shadow-sm border">
          <p className="text-sm text-gray-700">{card.description}</p>
          <p className="text-xs text-gray-500 mt-2">
            {getCardFullDescription(card)}
          </p>
        </div>
      )}

      {/* 翻转指示 */}
      {card.isReversed && (
        <div className="absolute top-2 right-2 w-6 h-6 bg-red-500 rounded-full flex items-center justify-center">
          <span className="text-white text-xs font-bold">逆</span>
        </div>
      )}
    </div>
  )
}

export default TarotCard

// CSS for 3D flip animation
const styles = `
.rotate-y-180 {
  transform: rotateY(180deg);
}

.backface-hidden {
  backface-visibility: hidden;
}

@keyframes flip {
  0% { transform: rotateY(0); }
  100% { transform: rotateY(180deg); }
}
`