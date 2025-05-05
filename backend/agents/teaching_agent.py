import os
from textwrap import dedent
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI, ChatAnthropic

SYSTEM = dedent("""        You are an AI tutor. Explain the answer clearly,
cite sources inline like (Source 1) (Source 2),
and—if code is helpful—include a runnable R code
block fenced with ```r … ```.

If the user asks for interpretation, provide both numeric
output and plain‑English explanation.
""")

def _llm():
    prov = os.getenv("MODEL_PROVIDER", "openai")
    if prov == "anthropic":
        return ChatAnthropic(model_name="claude-3-haiku-20240229")
    return ChatOpenAI(model="gpt-4o-mini")

_TEMPLATE = PromptTemplate(
    input_variables=["question", "context"],
    template=SYSTEM + "\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:",
)

def answer_question(question: str, docs):
    context = "\n".join([d.page_content for d in docs])
    llm = _llm()
    answer = llm.invoke(_TEMPLATE.format(question=question, context=context)).content
    code_block = None
    if "```r" in answer:
        try:
            code_block = answer.split("```r")[1].split("```")[0]
        except Exception:
            pass
    return answer, code_block
