function LanguageSelector({ languages = [], selected, onChange }) {
  const languageNames = {
    'en': 'English',
    'hi': 'हिंदी',
    'mr': 'मराठी',
    'bn': 'বাংলা',
    'ta': 'தமிழ்',
    'te': 'తెలుగు',
    'gu': 'ગુજરાતી'
  }

  // If no languages loaded yet, show default
  if (!Array.isArray(languages) || languages.length === 0) {
    return (
      <div className="flex items-center gap-2">
        <span className="text-sm text-gray-600">🌐</span>
        <select
          value={selected}
          onChange={(e) => onChange(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
        >
          <option value="en">English</option>
        </select>
      </div>
    )
  }

  return (
    <div className="flex items-center gap-2">
      <span className="text-sm text-gray-600">🌐</span>
      <select
        value={selected}
        onChange={(e) => onChange(e.target.value)}
        className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
      >
        {languages.map(lang => (
          <option key={lang} value={lang}>
            {languageNames[lang] || lang}
          </option>
        ))}
      </select>
    </div>
  )
}

export default LanguageSelector

