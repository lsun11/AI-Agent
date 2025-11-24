# src/api/routes/chat.py
import os
import json
import threading
from typing import Optional
from queue import Queue

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from ...save_utils import format_result_text, save_result_document_raw, save_result_slides
from ..models import ChatRequest, ChatResponse
from ..deps import TOPIC_WORKFLOWS, classify_topic_with_llm
from ..translate import is_chinese, translate_text

router = APIRouter()

SAVED_DOCS_DIR = "saved_docs"


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
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


@router.get("/chat_stream")
async def chat_stream(
    message: str,
    model: Optional[str] = Query(None),
    temperature: Optional[str] = Query(None),
):
    """
    Streaming chat endpoint using Server-Sent Events (SSE).
    The `message` comes from the query string, e.g. /chat_stream?message=...
    """
    user_query = message

    # --- language detection ---
    user_is_chinese = is_chinese(user_query)
    # Use an English query internally if Chinese
    internal_query = (
        translate_text(user_query, "English") if user_is_chinese else user_query
    )

    selected_model = model or "gpt-4o-mini"
    selected_temperature = float(temperature) if temperature is not None else 0.1

    print("User selected model:", selected_model)
    print("User selected temperature:", selected_temperature)

    # 1) classify topic
    topic_key, topic_label = classify_topic_with_llm(internal_query)

    # 2) get the *instance* from TOPIC_WORKFLOWS
    workflow = TOPIC_WORKFLOWS.get(topic_key)
    if workflow is None:
        workflow = TOPIC_WORKFLOWS.get("developer_tools")
        topic_key = "developer_tools"
        topic_label = "Developer Tools"

    # If Chinese, we may also translate the topic label for UI
    topic_label_display = (
        translate_text(topic_label, "Chinese") if user_is_chinese else topic_label
    )
    q: Queue[str] = Queue()

    def log_callback(msg: str) -> None:
        out_msg = msg
        if user_is_chinese:
            # You can prefix if you want, but simplest: just translate the log
            out_msg = translate_text(msg, "Chinese")
        payload = {"type": "log", "message": out_msg}
        q.put(json.dumps(payload))

    # Initial log messages (model + temp)
    q.put(json.dumps({"type": "log", "message": f"📌 Model selected: {selected_model}"}))
    q.put(json.dumps({"type": "log", "message": f"🎛️ Temperature set to: {selected_temperature}"}))

    def run_workflow():
        # set callback just for this run
        workflow.set_llm(selected_model, selected_temperature)
        workflow.set_log_callback(log_callback)
        try:
            result = workflow.run(internal_query)
            reply_text_en = format_result_text(internal_query, result)

            # translate final reply back to Chinese if needed
            reply_text = (
                translate_text(reply_text_en, "Chinese")
                if user_is_chinese
                else reply_text_en
            )

            text_path = save_result_document_raw(user_query, reply_text)
            text_filename = os.path.basename(text_path)
            download_url = f"/download/{text_filename}"

            slides_path = save_result_slides(user_query, result)
            slides_filename = os.path.basename(slides_path)
            slides_download_url = f"/download/{slides_filename}"

            final_payload = {
                "type": "final",
                "reply": reply_text,
                "download_url": download_url,
                "slides_download_url": slides_download_url,
                "topic_used": topic_label_display,
            }
            q.put(json.dumps(final_payload))
        finally:
            workflow.set_log_callback(None)
            q.put("__DONE__")

    # Run workflow in background thread so we can stream logs
    threading.Thread(target=run_workflow, daemon=True).start()

    def event_generator():
        # First send topic info so UI can update title immediately
        topic_payload = {
            "type": "topic",
            "topic_key": topic_key,
            "topic_label": topic_label_display,
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