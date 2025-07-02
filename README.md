# Intelligent Excuse Generator

FastAPI micro-service that creates believable excuses plus a chat-log “proof,”
stores history, ranks past excuses, and simulates an emergency text—powered by
Google Gemini (via LangChain).

## 1 . Setup
```bash
git clone https://github.com/<yourUser>/excuse-generator.git
cd excuse-generator
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt