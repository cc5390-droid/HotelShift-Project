# AI Assistant Setup Guide

## 🤖 Overview

Your MSA Investment App now includes a local AI Assistant that can:
- Answer questions about MSA data
- Search the web for recent news
- Compare markets and provide investment insights
- All running completely locally with no external AI API costs!

## 📋 Prerequisites

### 1. Install Ollama (For Full LLM Features)
The AI assistant works best with Ollama - a local LLM runtime.

**Download:** https://ollama.ai

**Installation:**
- macOS: `brew install ollama` or download the app
- Linux/Windows: Download from ollama.ai

**Verify installation:**
```bash
ollama --version
```

### 2. Download a Model (Optional but Recommended)

Once Ollama is installed, download a lightweight model:

```bash
ollama pull mistral
```

Other available models:
- `ollama pull llama2` - Larger, more capable (~4GB)
- `ollama pull neural-chat` - Fast, practical (~4GB)
- `ollama pull stable-beluga` - Good for Q&A (~3GB)

## 🚀 Setup Steps

### Step 1: Install Python Dependencies

```bash
cd msa-investment-app
pip install -r requirements.txt
```

**Note:** First time installation may take a few minutes for `sentence-transformers` to download embeddings (~400MB).

### Step 2: Start Ollama Server (if using LLM features)

In a **separate terminal**, run:

```bash
ollama serve
```

You should see:
```
Starting Ollama...
Listening on [::]:11434
```

**Keep this terminal running while using the app.**

### Step 3: Run the App

In the original terminal:

```bash
python app.py
```

The app will start on `http://localhost:5001`

### Step 4: Open in Browser

Navigate to:
```
http://localhost:5001
```

Look for the **💬 AI Assistant** button in the top-right corner!

## 🎯 What You Can Ask

### About Your MSA Data:
- "What's the investment score for Austin?"
- "Show me the top 5 MSAs"
- "Compare Denver and Seattle"
- "Which MSA has the best supply index?"

### Search the Web:
- "Tell me about hotel industry news in Austin"
- "What's happening in Denver real estate?"
- "Recent economic trends in tech hubs"
- "Latest housing market reports for Seattle"

### General Questions:
- "What factors affect investment potential?"
- "How is the investment score calculated?"
- "What are the 6 investment dimensions?"

## ⚙️ Configuration

### Change the AI Model

Edit `ai_helper.py` line ~50:

```python
self.model = "mistral"  # Change this to another model
```

Available models (after downloading with ollama):
- `mistral` (fast, practical)
- `llama2` (more capable)
- `neural-chat` (conversational)
- `stable-beliza` (good Q&A)

### Disable Web Search

In the chat function, `include_web_search` parameter can be set to `False`:

```python
result = ai_assistant.process_query(user_query, include_web_search=False)
```

### Change Ollama Port

If Ollama is running on a different port, edit `ai_helper.py`:

```python
assistant = AIAssistant(ollama_url="http://localhost:11434")  # Change port if needed
```

## 🐛 Troubleshooting

### "Ollama is not running" Message

**Solution:** Start Ollama in a separate terminal:
```bash
ollama serve
```

The app still works without Ollama, but LLM features won't be available.

### Web Search Not Working

**Possible causes:**
1. Internet connection issue
2. DuckDuckGo blocking requests

**Solution:** Try restarting the app or check your internet connection.

### Slow Response Times

**Causes:**
- First model load (normal, takes 10-30 seconds first time)
- Running on slower hardware

**Solution:** Use a smaller model like `mistral` instead of `llama2`

### Port Already in Use

If port 5001 is busy:

```bash
PORT=3000 python app.py
```

Then visit `http://localhost:3000`

### Memory Issues

If you get out-of-memory errors:

1. Use a smaller model:
   ```bash
   ollama pull mistral
   ```

2. Or reduce model size in `ai_helper.py`:
   ```python
   self.model = "mistral"  # Use smaller model
   ```

## 📊 Performance Tips

1. **First Run:** First response takes 10-15 seconds (model loading)
2. **Subsequent Responses:** 2-5 seconds typically
3. **Web Search:** 3-5 seconds (depends on internet speed)
4. **Vector Search:** < 1 second

## 🔒 Privacy & Data

✅ **Everything runs locally:**
- Your data never leaves your computer
- No API calls to external AI services
- No data collection or logging
- MSA data stays in the app

⚠️ **Web search:**
- Uses DuckDuckGo (privacy-focused)
- Searches are anonymous
- Results are summarized, not stored

## 📝 What's Built-In

### AI Features:
- ✅ Local LLM (Ollama)
- ✅ Vector similarity search (MSA data)
- ✅ Web search (DuckDuckGo)
- ✅ Question classification
- ✅ Conversational responses

### Technologies:
- **LLM:** Ollama + Mistral 7B
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **Search:** DuckDuckGo + BeautifulSoup
- **Backend:** Flask
- **Frontend:** Vanilla JavaScript

## 🚀 Next Steps

1. Install Ollama from ollama.ai
2. Run `ollama pull mistral`
3. Start Ollama: `ollama serve`
4. Run the app: `python app.py`
5. Click the **💬 AI Assistant** button and start chatting!

## 💡 Tips for Best Results

- **Be specific:** "What's the investment score for Denver?" works better than "Austin"
- **Ask in natural language:** The AI understands conversational questions
- **Combine queries:** "Tell me about Austin hotels news and compare to Denver"
- **Share context:** Reference MSAs mentioned earlier in conversation

---

**Questions?** Check the README.md for more about the MSA Investment App.

Enjoy your local AI assistant! 🎉
