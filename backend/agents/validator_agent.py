import os
from langchain.chat_models import ChatOpenAI, ChatAnthropic

PROMPT = (
    "You are a classifier. Reply ONLY yes/no.\n"
    "Does this question relate to statistics concepts or the R language?\n"
    "Question: {q}"
)

def _llm():
    prov = os.getenv("MODEL_PROVIDER", "openai")
    if prov == "anthropic":
        return ChatAnthropic(model_name="claude-3-haiku-20240229")
    return ChatOpenAI(model="gpt-4o-mini")

def validate_question(question: str) -> bool:
    llm = _llm()
    resp = llm.invoke(PROMPT.format(q=question)).content.strip().lower()
    return resp.startswith("y")
