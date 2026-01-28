import { useState, useEffect, useCallback } from 'react'
import { DrawnCard } from '../types'
import { drawCards } from '../services/tarotService'
import TarotCard from './TarotCard'

interface TarotCardDeckProps {
  cardCount?: number
  onCardsDrawn?: (cards: DrawnCard[]) => void
  autoDraw?: boolean
}

const TarotCardDeck: React.FC<TarotCardDeckProps> = ({ 
  cardCount = 3, 
  onCardsDrawn,
  autoDraw = false 
}) => {
  const [cards, setCards] = useState<DrawnCard[]>([])
  const [isDrawing, setIsDrawing] = useState(false)
  const [showCards, setShowCards] = useState(false)

  const handleDrawCards = useCallback(async () => {
    setIsDrawing(true)
    setShowCards(false)
    
    // 模拟抽牌动画延迟
    setTimeout(async () => {
      const drawnCards = await drawCards(cardCount)
      setCards(drawnCards)
      setIsDrawing(false)
      setShowCards(true)
      
      if (onCardsDrawn) {
        onCardsDrawn(drawnCards)
      }
    }, 1500)
  }, [cardCount, onCardsDrawn])

  useEffect(() => {
    if (autoDraw) {
      handleDrawCards()
    }
  }, [autoDraw, handleDrawCards])

  const handleCardClick = (clickedCard: DrawnCard) => {
    console.log('Card clicked:', clickedCard)
  }

  return (
    <div className="flex flex-col items-center">
      {/* 抽牌按钮 */}
      {!autoDraw && (
        <button 
          onClick={handleDrawCards}
          disabled={isDrawing}
          className="btn-primary mb-8"
        >
          {isDrawing ? '正在抽取中...' : '🔮 抽取塔罗牌'}
        </button>
      )}

      {/* 抽牌动画 */}
      {isDrawing && (
        <div className="flex gap-4 mb-8">
          {[...Array(cardCount)].map((_, index) => (
            <div key={index} className="relative">
              {/* 牌背动画 */}
              <div className="w-48 h-80 bg-gradient-to-br from-purple-600 to-blue-600 rounded-xl shadow-lg flex items-center justify-center">
                <div className="text-white text-4xl animate-pulse">🌙</div>
              </div>
              {/* 抽牌动画效果 */}
              <div className="absolute inset-0 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-xl opacity-0 animate-ping"></div>
            </div>
          ))}
        </div>
      )}

      {/* 抽牌结果 */}
      {showCards && cards.length > 0 && (
        <div className="w-full">
          <h3 className="text-xl font-bold text-gray-800 mb-6 text-center">
            你的塔罗牌阵 ({cards.length}张牌)
          </h3>
          
          <div className="flex flex-wrap justify-center gap-6">
            {cards.map((card, index) => (
              <div key={card.id} className="flex flex-col items-center">
                <TarotCard 
                  card={card} 
                  onCardClick={handleCardClick}
                  className="transform hover:scale-105 transition-transform"
                />
                <div className="mt-2 text-sm text-gray-600">
                  位置 {index + 1}
                </div>
              </div>
            ))}
          </div>

          {/* 牌阵总结 */}
          <div className="mt-8 p-6 bg-white rounded-xl shadow-sm border">
            <h4 className="font-semibold text-lg mb-3">牌阵分析</h4>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {cards.map((card, index) => (
                <div key={card.id} className="p-3 bg-gray-50 rounded">
                  <div className="font-medium">位置 {index + 1}: {card.name}</div>
                  <div className={`text-sm ${card.isReversed ? 'text-red-600' : 'text-green-600'}`}>
                    {card.isReversed ? '逆位' : '正位'}
                  </div>
                  <div className="text-xs text-gray-500 mt-1">{card.description}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default TarotCardDeck