# app.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

# Import our setup — this triggers re-instrumentation in every worker!
from openai_client import generate , ensure_openai_instrumented


@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs in EVERY Uvicorn worker process
    ensure_openai_instrumented()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/summarize")
async def summarize_text(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "").strip()
        if not text or len(text) < 30:
            return {"success": False, "error": "Text too short"}

        summary = generate(TEXT=text)
        return {"success": True, "summary": summary}

    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html") as f:
        return HTMLResponse(f.read())

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)