# Intelligent Excuse Generator

FastAPI service that produces believable excuses, stores history, ranks by score,  
and simulates an emergency SMS—powered by Google Gemini (via LangChain).  
Supports multiple tones, languages, and optional voice output (MP3).

---

## 1 · Setup
    git clone https://github.com/Bhuvan-Arora-1313/excuse-generator.git
    cd excuse-generator
    python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
    pip install -r requirements.txt

Create a `.env` file:

    GOOGLE_API_KEY=AI-XXXXXXXXXXXXXXXXXXXXXXXX

---

## 2 · Run
    uvicorn excuse_api:app --reload
Swagger UI → http://localhost:8000/docs

---

## 3 · Endpoints

| Method | Path         | Body / Query                                                                                                               | Description                              |
|--------|--------------|----------------------------------------------------------------------------------------------------------------------------|------------------------------------------|
| POST   | `/generate`  | `scenario` (str, required)<br>`urgency` ("low" \| "medium" \| "panic")<br>`mode` ("normal" \| "apology")<br>`language` (ISO code, default `"en"`)<br>`voice` (bool, default `false`) | Generate excuse JSON (+ optional MP3 if `voice=true`) |
| GET    | `/top?n=5`   | `n` (query param)                                                                                                          | Top *n* excuses by score                 |
| POST   | `/emergency` | `{"number":"+1123456789","message":"Call me!"}`                                                                            | Simulate emergency SMS (logs entry)     |

---

## 4 · Example
    curl -X POST http://127.0.0.1:8000/generate \
         -H "Content-Type: application/json" \
         -d '{
               "scenario": "missed class",
               "urgency": "panic",
               "mode": "apology",
               "language": "es",
               "voice": true
             }'