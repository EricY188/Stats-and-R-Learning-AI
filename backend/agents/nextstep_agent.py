from langchain.chat_models import ChatOpenAI
from textwrap import dedent

_PROMPT = dedent("""        You are a curriculum assistant for statistics learners.
Given the last user question, suggest ONE next concept or R
package/function to explore, plus a resource link
(e.g., chapter in R4DS or a CRAN article).
Reply in max 40 words.
Question: {q}
Next:
""")

def suggest_next(question: str) -> str:
    llm = ChatOpenAI(model="gpt-4o-mini")
    return llm.invoke(_PROMPT.format(q=question)).content.strip()
