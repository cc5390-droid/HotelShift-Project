#!/bin/bash

# MSA Investment App with AI Assistant - Quick Start Script

echo "🚀 MSA Investment App with AI Assistant"
echo "========================================"
echo ""

# Check if Ollama is running (optional but recommended)
echo "Checking Ollama status..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running"
    echo ""
else
    echo "⚠️  Ollama is not running"
    echo "To enable full AI features, run in another terminal:"
    echo "  ollama serve"
    echo ""
fi

# Start the Flask app
echo "Starting Flask application..."
echo "📊 Opening http://localhost:5001"
echo ""
echo "🤖 AI Assistant will be available via the 💬 button"
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
