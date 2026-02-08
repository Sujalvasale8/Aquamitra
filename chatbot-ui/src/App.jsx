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

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-blue-50 to-cyan-50">
      {/* Header */}
      <header className="bg-white shadow-md px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
            <span className="text-white text-xl font-bold">💧</span>
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Aquamitra</h1>
            <p className="text-sm text-gray-500">Groundwater Data Assistant</p>
          </div>
        </div>
        <LanguageSelector 
          languages={languages}
          selected={language}
          onChange={setLanguage}
        />
      </header>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-4">
        <div className="max-w-4xl mx-auto space-y-4">
          {messages.length === 0 && (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">💧</div>
              <h2 className="text-2xl font-semibold text-gray-700 mb-2">
                Welcome to Aquamitra
              </h2>
              <p className="text-gray-500">
                Ask me anything about groundwater data across India
              </p>
              <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto">
                <button
                  onClick={() => setInput('Show me critical groundwater areas')}
                  className="p-3 bg-white rounded-lg shadow hover:shadow-md transition text-left"
                >
                  <span className="text-sm text-gray-600">💡 Show me critical groundwater areas</span>
                </button>
                <button
                  onClick={() => setInput('What is the total rainfall in Maharashtra?')}
                  className="p-3 bg-white rounded-lg shadow hover:shadow-md transition text-left"
                >
                  <span className="text-sm text-gray-600">💡 What is the total rainfall in Maharashtra?</span>
                </button>
              </div>
            </div>
          )}
          
          {messages.map((msg, idx) => (
            <ChatMessage key={idx} message={msg} />
          ))}
          
          {loading && (
            <div className="flex items-center gap-2 text-gray-500">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
              <span>Thinking...</span>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Form */}
      <div className="bg-white border-t px-6 py-4">
        <form onSubmit={sendMessage} className="max-w-4xl mx-auto">
          <div className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about groundwater data..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition"
            >
              Send
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default App

