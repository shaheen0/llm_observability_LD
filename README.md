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

**Real example:** You're monitoring AI summarization costs.
- User sends text → OpenAI processes it → You get summary
- Meanwhile: token count, API cost, response time all tracked automatically in LaunchDarkly
- Result: You see "Each summary = 150 tokens = $0.05" → Can optimize or set cost alerts

**Production use:** Track if your LLM API is getting slower/more expensive over time/# LLM Observability with LaunchDarkly

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

---

## 4. Create Static HTML File

Create `static/index.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Text Summarizer</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
        textarea { width: 100%; padding: 10px; min-height: 150px; border: 1px solid #ddd; }
        button { background: #0066cc; color: white; padding: 10px 20px; border: none; cursor: pointer; margin-top: 10px; }
        .result { margin-top: 20px; padding: 15px; background: #f5f5f5; display: none; }
        .result.show { display: block; }
        .error { color: red; }
        .success { color: green; }
    </style>
</head>
<body>
    <h1>📝 Text Summarizer</h1>
    <textarea id="textInput" placeholder="Paste text here (min 30 chars)..."></textarea>
    <button onclick="summarize()">Summarize</button>
    <div id="result" class="result">
        <h3>Summary:</h3>
        <p id="resultText"></p>
    </div>

    <script>
        async function summarize() {
            const text = document.getElementById("textInput").value;
            const resultDiv = document.getElementById("result");
            const resultText = document.getElementById("resultText");
            
            if (!text.trim()) {
                resultText.innerHTML = '<span class="error">⚠️ Enter text</span>';
                resultDiv.classList.add("show");
                return;
            }

            resultText.innerHTML = '<span>⏳ Loading...</span>';
            resultDiv.classList.add("show");

            try {
                const response = await fetch("/summarize", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ text })
                });
                const data = await response.json();
                
                if (data.success) {
                    resultText.innerHTML = '<span class="success">✅</span><p>' + data.summary.replace(/\n/g, "<br>") + '</p>';
                } else {
                    resultText.innerHTML = '<span class="error">❌ ' + data.error + '</span>';
                }
            } catch (error) {
                resultText.innerHTML = '<span class="error">❌ Error: ' + error.message + '</span>';
            }
        }
    </script>
</body>
</html>
```

---

## 5. Run the FastAPI App

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

Go to https://app.launchdarkly.com → **Analytics → LLM Events**

You'll see: token usage, cost, latency, request count.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Run `uv sync` |
| `Missing LAUNCHDARKLY_SDK_KEY` | Check `.env` file exists in root folder |
| `Port 8000 in use` | Change port: `uvicorn app:app --port 8001 --reload` |
| No data in LaunchDarkly | Wait 30s, make sure flag `llm_observability_v1` exists |

---

## How It Works

**Real example:** You're monitoring AI summarization costs.
- User sends text → OpenAI processes it → You get summary
- Meanwhile: token count, API cost, response time all tracked automatically in LaunchDarkly
- Result: You see "Each summary = 150 tokens = $0.05" → Can optimize or set cost alerts

**Production use:** Track if your LLM API is getting slower/more expensive over time.# LLM Observability with LaunchDarkly

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

---

## 4. Create Static HTML File

Create `static/index.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Text Summarizer</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
        textarea { width: 100%; padding: 10px; min-height: 150px; border: 1px solid #ddd; }
        button { background: #0066cc; color: white; padding: 10px 20px; border: none; cursor: pointer; margin-top: 10px; }
        .result { margin-top: 20px; padding: 15px; background: #f5f5f5; display: none; }
        .result.show { display: block; }
        .error { color: red; }
        .success { color: green; }
    </style>
</head>
<body>
    <h1>📝 Text Summarizer</h1>
    <textarea id="textInput" placeholder="Paste text here (min 30 chars)..."></textarea>
    <button onclick="summarize()">Summarize</button>
    <div id="result" class="result">
        <h3>Summary:</h3>
        <p id="resultText"></p>
    </div>

    <script>
        async function summarize() {
            const text = document.getElementById("textInput").value;
            const resultDiv = document.getElementById("result");
            const resultText = document.getElementById("resultText");
            
            if (!text.trim()) {
                resultText.innerHTML = '<span class="error">⚠️ Enter text</span>';
                resultDiv.classList.add("show");
                return;
            }

            resultText.innerHTML = '<span>⏳ Loading...</span>';
            resultDiv.classList.add("show");

            try {
                const response = await fetch("/summarize", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ text })
                });
                const data = await response.json();
                
                if (data.success) {
                    resultText.innerHTML = '<span class="success">✅</span><p>' + data.summary.replace(/\n/g, "<br>") + '</p>';
                } else {
                    resultText.innerHTML = '<span class="error">❌ ' + data.error + '</span>';
                }
            } catch (error) {
                resultText.innerHTML = '<span class="error">❌ Error: ' + error.message + '</span>';
            }
        }
    </script>
</body>
</html>
```

---

## 5. Run the FastAPI App

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

Go to https://app.launchdarkly.com → **Analytics → LLM Events**

You'll see: token usage, cost, latency, request count.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Run `uv sync` |
| `Missing LAUNCHDARKLY_SDK_KEY` | Check `.env` file exists in root folder |
| `Port 8000 in use` | Change port: `uvicorn app:app --port 8001 --reload` |
| No data in LaunchDarkly | Wait 30s, make sure flag `llm_observability_v1` exists |

---

## How It Works

**Real example:** You're monitoring AI summarization costs.
- User sends text → OpenAI processes it → You get summary
- Meanwhile: token count, API cost, response time all tracked automatically in LaunchDarkly
- Result: You see "Each summary = 150 tokens = $0.05" → Can optimize or set cost alerts

**Production use:** Track if your LLM API is getting slower/more expensive over time.# LLM Observability with LaunchDarkly

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

---

## 4. Create Static HTML File

Create `static/index.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Text Summarizer</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
        textarea { width: 100%; padding: 10px; min-height: 150px; border: 1px solid #ddd; }
        button { background: #0066cc; color: white; padding: 10px 20px; border: none; cursor: pointer; margin-top: 10px; }
        .result { margin-top: 20px; padding: 15px; background: #f5f5f5; display: none; }
        .result.show { display: block; }
        .error { color: red; }
        .success { color: green; }
    </style>
</head>
<body>
    <h1>📝 Text Summarizer</h1>
    <textarea id="textInput" placeholder="Paste text here (min 30 chars)..."></textarea>
    <button onclick="summarize()">Summarize</button>
    <div id="result" class="result">
        <h3>Summary:</h3>
        <p id="resultText"></p>
    </div>

    <script>
        async function summarize() {
            const text = document.getElementById("textInput").value;
            const resultDiv = document.getElementById("result");
            const resultText = document.getElementById("resultText");
            
            if (!text.trim()) {
                resultText.innerHTML = '<span class="error">⚠️ Enter text</span>';
                resultDiv.classList.add("show");
                return;
            }

            resultText.innerHTML = '<span>⏳ Loading...</span>';
            resultDiv.classList.add("show");

            try {
                const response = await fetch("/summarize", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ text })
                });
                const data = await response.json();
                
                if (data.success) {
                    resultText.innerHTML = '<span class="success">✅</span><p>' + data.summary.replace(/\n/g, "<br>") + '</p>';
                } else {
                    resultText.innerHTML = '<span class="error">❌ ' + data.error + '</span>';
                }
            } catch (error) {
                resultText.innerHTML = '<span class="error">❌ Error: ' + error.message + '</span>';
            }
        }
    </script>
</body>
</html>
```

---

## 5. Run the FastAPI App

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

Go to https://app.launchdarkly.com → **Analytics → LLM Events**

You'll see: token usage, cost, latency, request count.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Run `uv sync` |
| `Missing LAUNCHDARKLY_SDK_KEY` | Check `.env` file exists in root folder |
| `Port 8000 in use` | Change port: `uvicorn app:app --port 8001 --reload` |
| No data in LaunchDarkly | Wait 30s, make sure flag `llm_observability_v1` exists |

---

## How It Works

**Real example:** You're monitoring AI summarization costs.
- User sends text → OpenAI processes it → You get summary
- Meanwhile: token count, API cost, response time all tracked automatically in LaunchDarkly
- Result: You see "Each summary = 150 tokens = $0.05" → Can optimize or set cost alerts

**Production use:** Track if your LLM API is getting slower/more expensive over time.