function ChatMessage({ message }) {
  const isUser = message.role === 'user'
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex gap-3 max-w-3xl ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser ? 'bg-blue-600' : 'bg-gray-300'
        }`}>
          <span className="text-sm">
            {isUser ? '👤' : '💧'}
          </span>
        </div>
        
        {/* Message Content */}
        <div className={`px-4 py-3 rounded-lg ${
          isUser 
            ? 'bg-blue-600 text-white' 
            : 'bg-white text-gray-800 shadow'
        }`}>
          <p className="whitespace-pre-wrap">{message.content}</p>
        </div>
      </div>
    </div>
  )
}

export default ChatMessage

