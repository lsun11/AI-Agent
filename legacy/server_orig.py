# server.py
import os
from typing import Optional
import uvicorn
import json
import threading
from queue import Queue
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from src.save_utils import format_result_text, save_result_document_raw
from src.topics.registry import build_workflows, get_topic_descriptions, get_topic_labels, TOPIC_CONFIGS

# ---------------------------------------------------------
# Build workflows & topic descriptions from registry
# ---------------------------------------------------------
TOPIC_WORKFLOWS = build_workflows()
TOPIC_LABELS = get_topic_labels()
TOPIC_DESCRIPTIONS = get_topic_descriptions()
TOPIC_KEYS = list(TOPIC_CONFIGS.keys())

# LLM used for classification (small, deterministic)
topic_classifier_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def classify_topic_with_llm(query: str) -> tuple[str, str]:
    """
    Returns (key, label)
    - key: internal name (e.g. 'database')
    - label: user-facing display (e.g. 'Databases & Data Platforms')
    """

    topic_list_text = "\n".join(
        f"- {cfg.label}: {cfg.description}"
        for cfg in TOPIC_CONFIGS.values()
    )

    system_prompt = (
        "You are a topic router. You classify user queries into categories.\n\n"
        "Available research categories:\n"
        f"{topic_list_text}\n\n"
        "Your job:\n"
        "- Read the query.\n"
        "- Choose EXACTLY one category.\n"
        "- Return ONLY the category *label*, nothing else.\n"
        "If ambiguous, choose the closest match."
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"User query: {query}"),
    ]

    try:
        response = topic_classifier_llm.invoke(messages)
        label = response.content.strip()

        # Find which config matches this label
        for key, cfg in TOPIC_CONFIGS.items():
            if cfg.label.lower() == label.lower():
                return key, cfg.label

        # fallback — shouldn't happen
        default_key = next(iter(TOPIC_CONFIGS.keys()))
        return default_key, TOPIC_CONFIGS[default_key].label

    except Exception as e:
        print("Topic classification error:", e)

        default_key = next(iter(TOPIC_CONFIGS.keys()))
        return default_key, TOPIC_CONFIGS[default_key].label


# ---------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static_build", StaticFiles(directory="static_build"), name="static_build")

SAVED_DOCS_DIR = "../advanced_agent/saved_docs"
SAVED_SLIDES_DIR = "../advanced_agent/saved_slides"

@app.get("/", response_class=FileResponse)
async def index():
    return FileResponse("../advanced_agent/static/index.html")

class TopicRequest(BaseModel):
    message: str

class TopicResponse(BaseModel):
    topic_key: str
    topic_label: str

class ChatRequest(BaseModel):
    message: str
    # Optional manual override; if provided and valid, we use it.
    topic: str | None = None


class ChatResponse(BaseModel):
    reply: str
    download_url: str | None = None
    topic_used: str | None = None
    logs: list[str] = []

class ChatStreamRequest(BaseModel):
    message: str

# ---------- new: fast topic classification endpoint ----------

@app.post("/classify_topic", response_model=TopicResponse)
async def classify_topic(req: TopicRequest):
    key, label = classify_topic_with_llm(req.message)
    return TopicResponse(topic_key=key, topic_label=label)

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # 1) Decide topic: use user override if valid, else classify with LLM
    if req.topic is not None and req.topic in TOPIC_WORKFLOWS:
        topic = req.topic
    elif req.topic is not None and req.topic not in TOPIC_WORKFLOWS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unknown topic '{req.topic}'. "
                f"Valid topics: {', '.join(TOPIC_WORKFLOWS.keys())}"
            ),
        )
    else:
        topic, topic_label = classify_topic_with_llm(req.message)

    workflow = TOPIC_WORKFLOWS[topic]

    # 2) Run the selected workflow
    result = workflow.run(req.message)
    reply_text = format_result_text(req.message, result)

    # 🆕 get logs from the result state
    logs = getattr(result, "log_messages", []) or []

    # 3) Save summary to a file for download
    path = save_result_document_raw(req.message, reply_text)
    filename = os.path.basename(path)
    download_url = f"/download/{filename}"

    return ChatResponse(reply=reply_text, download_url=download_url, topic_used=topic, logs=logs)


@app.get("/chat_stream")
async def chat_stream(message: str,
                      model: Optional[str] = Query(None),  # e.g. "gpt-4o", "gpt-5.1", etc.
                      temperature: Optional[str] = Query(None)
):
    """
    Streaming chat endpoint using Server-Sent Events (SSE).
    The `message` comes from the query string, e.g. /chat_stream?message=...
    """

    user_query = message
    selected_model = model or "gpt-4o-mini"
    selected_temperature = float(temperature) or 0.1
    print("User selected model:", selected_model)
    print("User selected temperature:", selected_temperature)
    # 1) classify topic (reuse your existing classifier)
    #    This should return (topic_key, topic_label)
    topic_key, topic_label = classify_topic_with_llm(user_query)

    # 2) get the *instance* from TOPIC_WORKFLOWS
    workflow = TOPIC_WORKFLOWS.get(topic_key)
    if workflow is None:
        # fallback to a default, e.g. developer_tools
        workflow = TOPIC_WORKFLOWS.get("developer_tools")
        topic_key = "developer_tools"
        topic_label = "Developer Tools"

    q: Queue[str] = Queue()

    def log_callback(msg: str) -> None:
        payload = {"type": "log", "message": msg}
        q.put(json.dumps(payload))
    # ---- Send model + temp to UI as initial log messages ----
    q.put(json.dumps({"type": "log",
                      "message": f"📌 Model selected: {selected_model}"}))
    q.put(json.dumps({"type": "log",
                      "message": f"🎛️ Temperature set to: {selected_temperature}"}))

    def run_workflow():
        # set callback just for this run
        workflow.set_llm(selected_model, selected_temperature)
        workflow.set_log_callback(log_callback)
        try:
            result = workflow.run(user_query)
            reply_text = format_result_text(user_query, result)

            path = save_result_document_raw(user_query, reply_text)
            filename = os.path.basename(path)
            download_url = f"/download/{filename}"

            final_payload = {
                "type": "final",
                "reply": reply_text,
                "download_url": download_url,
                "topic_used": topic_label,
            }
            q.put(json.dumps(final_payload))
        finally:
            # clear callback so it doesn't leak into subsequent runs
            workflow.set_log_callback(None)
            q.put("__DONE__")

    # run workflow in a background thread so we can stream logs
    threading.Thread(target=run_workflow,  daemon=True).start()

    def event_generator():
        # First send topic info so UI can update title immediately
        topic_payload = {
            "type": "topic",
            "topic_key": topic_key,
            "topic_label": topic_label,
        }
        yield f"data: {json.dumps(topic_payload)}\n\n"

        while True:
            item = q.get()
            if item == "__DONE__":
                break
            yield f"data: {item}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )



@app.get("/download/{filename}")
async def download_file(filename: str):
    # pick media_type based on extension
    if filename.lower().endswith(".pptx"):
        file_path = os.path.join(SAVED_SLIDES_DIR, filename)
        media_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        if not os.path.exists(file_path):
            # You'd see a clean 404, not a 500
            raise HTTPException(status_code=404, detail="File not found")
    else:
        file_path = os.path.join(SAVED_DOCS_DIR, filename)
        media_type = "text/plain; charset=utf-8"
        if not os.path.exists(file_path):
            # You'd see a clean 404, not a 500
            raise HTTPException(status_code=404, detail="File not found")

    # Let FileResponse set Content-Disposition correctly
    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=filename,  # Starlette will generate the header safely
    )


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
