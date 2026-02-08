# 💧 Aquamitra - Frontend UI

## Overview

A modern, responsive React-based chat interface for the Aquamitra groundwater data assistant.

## Features

- 💬 **Real-time Chat Interface** - Interactive conversation with the AI assistant
- 🌐 **Multilingual Support** - Switch between 7 Indian languages
- 🎨 **Modern UI** - Clean, gradient design with Tailwind CSS
- 📱 **Responsive** - Works on desktop, tablet, and mobile
- ⚡ **Fast** - Built with Vite for lightning-fast development

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS v4** - Styling
- **Axios** - HTTP client for API calls

## Quick Start

### Run Full Stack (Recommended)

```bash
# From project root
./start-all.sh
```

Then open http://localhost:5173 in your browser!

### Run Frontend Only

```bash
cd chatbot-ui
npm run dev
```

**Note:** Backend must be running on port 8000 for the frontend to work.

## Project Structure

```
chatbot-ui/
├── src/
│   ├── components/
│   │   ├── ChatMessage.jsx      # Individual message component
│   │   └── LanguageSelector.jsx # Language dropdown
│   ├── App.jsx                  # Main app component
│   ├── main.jsx                 # React entry point
│   └── index.css                # Global styles + Tailwind
├── index.html                   # HTML template
├── vite.config.js              # Vite configuration
├── tailwind.config.js          # Tailwind configuration
├── postcss.config.js           # PostCSS configuration
└── package.json                # Dependencies
```

## Available Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
```

## API Integration

The frontend connects to the backend API at `http://localhost:8000` via Vite proxy:

- `GET /api/languages` - Fetch available languages
- `POST /api/chat` - Send chat messages
- `GET /api/health` - Health check

## Supported Languages

- 🇬🇧 English (en)
- 🇮🇳 हिंदी (hi)
- 🇮🇳 मराठी (mr)
- 🇮🇳 বাংলা (bn)
- 🇮🇳 தமிழ் (ta)
- 🇮🇳 తెలుగు (te)
- 🇮🇳 ગુજરાતી (gu)

## Development

### Install Dependencies

```bash
npm install
```

### Environment

The frontend uses Vite's proxy to forward API requests to the backend. No additional environment variables needed!

### Hot Reload

Vite provides instant hot module replacement (HMR) - changes appear immediately in the browser.

## Building for Production

```bash
npm run build
```

This creates an optimized production build in the `dist/` directory.

## Troubleshooting

### Port 5173 already in use?

```bash
# Kill the process
lsof -ti:5173 | xargs kill -9

# Or change the port in vite.config.js
```

### API calls failing?

Make sure the backend is running on port 8000:

```bash
curl http://localhost:8000/api/health
```

### Styling not working?

Make sure Tailwind CSS PostCSS plugin is installed:

```bash
npm install @tailwindcss/postcss
```

## UI Features

### Welcome Screen

- Displays when no messages are present
- Shows example queries to get started
- Clean, inviting design

### Chat Interface

- User messages appear on the right (blue)
- Bot responses appear on the left (white)
- Auto-scrolls to latest message
- Loading indicator while waiting for response

### Language Selector

- Dropdown in the header
- Shows language names in native script
- Persists selection during conversation

## Contributing

The frontend is designed to be simple and extensible. Key areas for enhancement:

- Add message history persistence
- Implement voice input
- Add data visualization for query results
- Support file uploads for custom data
- Add dark mode toggle

---

Built with ❤️ for SIH 2025

