import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { useState } from 'react'
import HomePage from './pages/HomePage'
import DrawResultPage from './pages/DrawResultPage'
import InterpretationPage from './pages/InterpretationPage'
import FollowUpPage from './pages/FollowUpPage'
import { DivinationSession } from './types'

function App() {
  const [sessionCache, setSessionCache] = useState<DivinationSession | null>(null)

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50">
        <Routes>
          <Route 
            path="/" 
            element={<HomePage 
              onSessionCreated={(session) => setSessionCache(session)}
            />} 
          />
          <Route 
            path="/draw-result" 
            element={<DrawResultPage 
              cachedSession={sessionCache}
              onSessionUpdated={(session) => setSessionCache(session)}
            />} 
          />
          <Route 
            path="/interpretation" 
            element={<InterpretationPage 
              cachedSession={sessionCache}
              onSessionUpdated={(session) => setSessionCache(session)}
            />} 
          />
          <Route 
            path="/follow-up" 
            element={<FollowUpPage 
              cachedSession={sessionCache}
              onSessionUpdated={(session) => setSessionCache(session)}
            />} 
          />
        </Routes>
      </div>
    </Router>
  )
}

export default App