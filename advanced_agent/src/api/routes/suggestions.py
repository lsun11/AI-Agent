# ----- Sample question suggestions -----
from datetime import datetime
import json
import random
from typing import Optional, List
from fastapi import APIRouter, FastAPI
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel
from ..translate import is_chinese, translate_text

router = APIRouter()

SUGGESTIONS_CACHE: List[str] | None = None

class SuggestionsResponse(BaseModel):
    suggestions: List[str]


def generate_sample_questions(n: int = 5) -> List[str]:
    """
    Use a quick LLM to generate example queries this app can answer.
    - We ask for JSON array.
    - We robustly extract the JSON portion (between [ and ]).
    - If anything fails, we fall back to a default pool.
    - We also inject a random 'seed' into the prompt so each call tends to differ.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9)  # higher temp for more variety

    # 🎲 randomizer to avoid provider/model caching and encourage variety
    rand_seed = random.randint(0, 10_000)
    now_iso = datetime.now().isoformat(timespec="seconds")

    system = (
        "You generate example user questions for a research assistant that helps "
        "software developers with:\n"
        "- developer tools & IDEs\n"
        "- APIs & backend services\n"
        "- cloud & databases\n"
        "- SaaS products\n"
        "- software engineering practices\n"
        "- developer careers (interviews, resumes, learning roadmaps)\n\n"
        "Return ONLY a JSON array of strings. No explanation, no code fences."
    )

    user = (
        f"Generate {n} diverse example questions a developer might ask this assistant.\n"
        f"Randomizer token: {rand_seed} at {now_iso}.\n"
        "Return strictly JSON like:\n"
        '["question1", "question2", ...]'
    )

    resp = llm.invoke(
        [
            SystemMessage(content=system),
            HumanMessage(content=user),
        ]
    )

    raw = resp.content.strip()

    questions: List[str] = []
    # ---- Try to extract a JSON array substring between [ and ] ----
    try:
        start = raw.find("[")
        end = raw.rfind("]")
        if start != -1 and end != -1 and start < end:
            json_str = raw[start : end + 1]
            parsed = json.loads(json_str)
            if isinstance(parsed, list):
                questions = [str(q).strip() for q in parsed if str(q).strip()]
    except Exception as e:
        print("Failed to parse JSON array from LLM output:", e)

    # ---- Fallback: use a pool of defaults and sample ----
    default_pool = [
        "What are some good Python IDEs for beginners?",
        "What are the pros and cons of using VS Code vs JetBrains IDEs?",
        "Which managed Postgres services should I consider on AWS, GCP, or Azure?",
        "What are good alternatives to AWS Lambda for serverless backends?",
        "What are the best coding interview platforms for LeetCode-style problems?",
        "How can I improve the architecture of a microservices-based system?",
        "What are good resources to learn system design for backend engineers?",
        "What tools can help me monitor and debug a distributed system?",
        "What are some best practices for designing multi-tenant SaaS architecture?",
        "How should I structure my software engineering resume for senior roles?",
    ]

    if not questions:
        # no valid LLM result → random sample from defaults
        questions = random.sample(default_pool, k=min(n, len(default_pool)))
    else:
        # if LLM gave more than n, trim; if fewer, keep them as-is
        questions = questions[:n]

    return questions

@router.get("/suggestions", response_model=SuggestionsResponse)
async def get_suggestions(language: str = "Eng"):
    """
    Return a small list of sample questions, translated if needed.
    """
    questions = generate_sample_questions(5)

    translated_questions = []
    for question in questions:
        if language == "Chn":
            question = translate_text(question, "Chinese")
        translated_questions.append(question)

    return SuggestionsResponse(suggestions=translated_questions)