import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import ChatMessage from './components/ChatMessage'
import LanguageSelector from './components/LanguageSelector'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [language, setLanguage] = useState('en')
  const [languages, setLanguages] = useState([])
  const [showChat, setShowChat] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    // Fetch available languages
    axios.get('/api/languages')
      .then(res => setLanguages(res.data.languages))
      .catch(err => console.error('Failed to fetch languages:', err))
  }, [])

  useEffect(() => {
    // Scroll to bottom when messages change
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    setShowChat(true)
    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.post('/api/chat', {
        messages: [...messages, userMessage],
        language: language
      })

      const botMessage = {
        role: 'assistant',
        content: response.data.response
      }
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Error:', error)
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.'
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleSuggestedQuery = (query) => {
    setInput(query)
    setShowChat(true)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-cyan-50 via-blue-50 to-teal-50">
      {/* Top Navigation */}
      <nav className="bg-white/80 backdrop-blur-sm border-b border-gray-200 px-6 py-3">
        <div className="max-w-7xl mx-auto flex items-center justify-center">
          <div className="text-center">
            <span className="text-xl font-bold bg-gradient-to-r from-cyan-600 to-blue-600 bg-clip-text text-transparent">
              AquaMitra
            </span>
            <p className="text-xs text-gray-500">Groundwater AI Assistant</p>
          </div>
        </div>
      </nav>

      {!showChat ? (
        /* Landing Page */
        <div className="max-w-7xl mx-auto px-6">
          {/* Hero Section */}
          <div className="text-center py-16">
            <div className="inline-block px-4 py-2 bg-white/60 backdrop-blur-sm rounded-full mb-6 border border-cyan-200">
              <span className="text-cyan-700 text-sm font-medium">✨ AI-Powered Groundwater Research</span>
            </div>

            <h1 className="text-5xl md:text-6xl font-bold text-cyan-800 mb-6 leading-tight">
              Groundwater insights<br />made simple with AI
            </h1>

            <p className="text-xl text-cyan-700 mb-8 max-w-3xl mx-auto">
              Meet AquaMitra — your AI-powered groundwater chatbot, integrated with INGRES.
              Get instant access to research data, policy insights, and environmental analysis.
            </p>

            <div className="flex items-center justify-center gap-4 mb-12">
              <button
                onClick={() => setShowChat(true)}
                className="px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition font-medium flex items-center gap-2"
              >
                Ask AquaMitra
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </button>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
              <div className="bg-white/60 backdrop-blur-sm rounded-xl p-6 border border-cyan-100">
                <div className="text-3xl font-bold text-cyan-700">500+</div>
                <div className="text-sm text-cyan-600 mt-1">Research Papers</div>
              </div>
              <div className="bg-white/60 backdrop-blur-sm rounded-xl p-6 border border-cyan-100">
                <div className="text-3xl font-bold text-cyan-700">50+</div>
                <div className="text-sm text-cyan-600 mt-1">Datasets</div>
              </div>
              <div className="bg-white/60 backdrop-blur-sm rounded-xl p-6 border border-cyan-100">
                <div className="text-3xl font-bold text-cyan-700">1000+</div>
                <div className="text-sm text-cyan-600 mt-1">Users</div>
              </div>
              <div className="bg-white/60 backdrop-blur-sm rounded-xl p-6 border border-cyan-100">
                <div className="text-3xl font-bold text-cyan-700">24/7</div>
                <div className="text-sm text-cyan-600 mt-1">AI Support</div>
              </div>
            </div>
          </div>

          {/* Features Section */}
          <div className="py-16">
            <h2 className="text-4xl font-bold text-center text-cyan-800 mb-4">
              Powerful Features for Groundwater Research
            </h2>
            <p className="text-center text-cyan-700 mb-12 max-w-3xl mx-auto">
              AquaMitra combines cutting-edge AI with comprehensive groundwater datasets to provide
              researchers, policymakers, and citizens with the tools they need for informed decision-making.
            </p>

            <div className="grid md:grid-cols-3 gap-8">
              {/* Feature 1 */}
              <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-8 border border-cyan-100 hover:shadow-lg transition">
                <div className="w-12 h-12 bg-cyan-500 rounded-xl flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                  </svg>
                </div>
                <h3 className="text-xl font-bold text-gray-800 mb-3">AI-Powered Q&A</h3>
                <p className="text-gray-600 mb-4">
                  Get instant answers about groundwater datasets with natural language queries.
                  Our AI understands complex geological and hydrological concepts.
                </p>
                <p className="text-green-600 text-sm font-medium">
                  Ask anything about groundwater data in plain English
                </p>
              </div>

              {/* Feature 2 */}
              <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-8 border border-cyan-100 hover:shadow-lg transition">
                <div className="w-12 h-12 bg-cyan-500 rounded-xl flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <h3 className="text-xl font-bold text-gray-800 mb-3">Data Visualization</h3>
                <p className="text-gray-600 mb-4">
                  Transform complex datasets into clear, interactive visualizations that reveal patterns
                  and trends in groundwater data.
                </p>
                <p className="text-green-600 text-sm font-medium">
                  See the story your data tells
                </p>
              </div>

              {/* Feature 3 */}
              <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-8 border border-cyan-100 hover:shadow-lg transition">
                <div className="w-12 h-12 bg-cyan-500 rounded-xl flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                  </svg>
                </div>
                <h3 className="text-xl font-bold text-gray-800 mb-3">Integrated Datasets</h3>
                <p className="text-gray-600 mb-4">
                  Access curated groundwater datasets from multiple sources, standardized and ready
                  for analysis and research.
                </p>
                <p className="text-green-600 text-sm font-medium">
                  One platform, all the data you need
                </p>
              </div>
            </div>
          </div>
        </div>
      ) : (
        /* Chat Interface */
        <div className="max-w-4xl mx-auto px-6 py-8">
          {/* Chat Header */}
          <div className="text-center mb-8">
            <button
              onClick={() => setShowChat(false)}
              className="text-cyan-600 hover:text-cyan-700 mb-4 inline-flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
              Back to Home
            </button>
            <h2 className="text-4xl font-bold text-cyan-700 mb-2">How can I help today?</h2>
            <p className="text-cyan-600">Type a command or ask a question</p>
          </div>

          {/* Input Box */}
          {messages.length === 0 && (
            <div className="mb-8">
              <form onSubmit={sendMessage} className="bg-white rounded-2xl shadow-lg p-6 border border-cyan-100">
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask a question..."
                  className="w-full px-4 py-3 border-0 focus:outline-none resize-none text-gray-700"
                  rows="3"
                  disabled={loading}
                />
                <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
                  <div className="flex items-center gap-3">
                    <button type="button" className="p-2 text-cyan-600 hover:bg-cyan-50 rounded-lg transition">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                      </svg>
                    </button>
                    <button type="button" className="p-2 text-cyan-600 hover:bg-cyan-50 rounded-lg transition">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                      </svg>
                    </button>
                  </div>
                  <div className="flex items-center gap-3">
                    <LanguageSelector
                      languages={languages}
                      selected={language}
                      onChange={setLanguage}
                    />
                    <button
                      type="submit"
                      disabled={loading || !input.trim()}
                      className="px-5 py-2 bg-cyan-600 text-white rounded-lg hover:bg-cyan-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition flex items-center gap-2"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                      </svg>
                      Send
                    </button>
                  </div>
                </div>
              </form>

              {/* Suggested Queries */}
              <div className="mt-6 flex flex-wrap gap-3 justify-center">
                <button
                  onClick={() => handleSuggestedQuery('Groundwater extraction in Rajasthan 2023')}
                  className="px-4 py-2 bg-white rounded-full text-sm text-cyan-700 hover:bg-cyan-50 border border-cyan-200 transition flex items-center gap-2"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                  Groundwater extraction in Rajasthan 2023
                </button>
                <button
                  onClick={() => handleSuggestedQuery('Recharge in Maharashtra 2022')}
                  className="px-4 py-2 bg-white rounded-full text-sm text-cyan-700 hover:bg-cyan-50 border border-cyan-200 transition flex items-center gap-2"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  Recharge in Maharashtra 2022
                </button>
                <button
                  onClick={() => handleSuggestedQuery('Status of groundwater in Punjab')}
                  className="px-4 py-2 bg-white rounded-full text-sm text-cyan-700 hover:bg-cyan-50 border border-cyan-200 transition flex items-center gap-2"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                  Status of groundwater in Punjab
                </button>
                <button
                  onClick={() => handleSuggestedQuery('Top 5 overexploited districts')}
                  className="px-4 py-2 bg-white rounded-full text-sm text-cyan-700 hover:bg-cyan-50 border border-cyan-200 transition flex items-center gap-2"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  Top 5 overexploited districts
                </button>
              </div>
            </div>
          )}

          {/* Chat Messages */}
          {messages.length > 0 && (
            <div className="space-y-4 mb-6">
              {messages.map((msg, idx) => (
                <ChatMessage key={idx} message={msg} />
              ))}

              {loading && (
                <div className="flex items-center gap-2 text-cyan-600 bg-white rounded-lg p-4">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-cyan-600"></div>
                  <span>Thinking...</span>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>
          )}

          {/* Input Form (when chat started) */}
          {messages.length > 0 && (
            <div className="sticky bottom-0 bg-white rounded-2xl shadow-lg p-4 border border-cyan-100">
              <form onSubmit={sendMessage} className="flex gap-3">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask a follow-up question..."
                  className="flex-1 px-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-500"
                  disabled={loading}
                />
                <button
                  type="submit"
                  disabled={loading || !input.trim()}
                  className="px-6 py-3 bg-cyan-600 text-white rounded-lg hover:bg-cyan-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition"
                >
                  Send
                </button>
              </form>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default App

