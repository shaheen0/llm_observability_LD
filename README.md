# LLM Observability with LaunchDarkly

**What it does:** Summarizes text using OpenAI + tracks token usage, cost, latency in LaunchDarkly dashboard.

---

## 1. Clone the Repository

```bash
git clone https://github.com/shaheen0/llm_evaluation.git
cd llm_observability
```

---

## 2. Install Dependencies

```bash
uv sync
#or
uv pip install -r requirements.txt
```

---

## 3. Create a .env File

In the root folder, create `.env` and add:

```
OPENAI_API_KEY=your_openai_api_key_here
LAUNCHDARKLY_SDK_KEY=your_launchdarkly_sdk_key_here
ENV=development
GIT_SHA=local-dev
```

Get your keys:
- **OpenAI:** https://platform.openai.com/api/keys
- **LaunchDarkly:** https://app.launchdarkly.com → Account settings → Environments

##  Run the FastAPI App

```bash
fastapi dev app.py
```

OR

```bash
uvicorn app:app --reload
```

Open browser → http://127.0.0.1:8000

---

## 6. Check LaunchDarkly Dashboard

Go to https://app.launchdarkly.com → **Traces → LLM Events**

You'll see: token usage, cost, latency, request count.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Missing LAUNCHDARKLY_SDK_KEY` | Check `.env` file exists in root folder |
| `Port 8000 in use` | Change port: `uvicorn app:app --port 8001 --reload` |
| No data in LaunchDarkly | Wait 30s, make sure flag `llm_observability_v1` exists |

---

## How It Works

**Real example:** monitoring AI summarization costs.
- User sends text → OpenAI processes it → You get summary
- Meanwhile: token count, API cost, response time all tracked automatically in LaunchDarkly
- Result: You see "Each summary = 150 tokens = $0.05" → Can optimize or set cost alerts

**Production use:** Track if your LLM API is getting slower/more expensive over time/# LLM Observability with LaunchDarkly

**What it does:** Summarizes text using OpenAI + tracks token usage, cost, latency in LaunchDarkly dashboard.
