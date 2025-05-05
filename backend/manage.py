from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.validator_agent import validate_question
from agents.retriever_agent import retrieve_chunks
from agents.teaching_agent import answer_question
from agents.nextstep_agent import suggest_next
from tools.r_exec_tool import run_r_code_safe

app = FastAPI()

class QueryIn(BaseModel):
    question: str
    run_code: bool | None = False   # optional: execute R code

@app.post("/api/query/")
async def query_endpoint(item: QueryIn):
    if not validate_question(item.question):
        raise HTTPException(status_code=400, detail="Not a stats/R question 🤖")
    docs = retrieve_chunks(item.question)
    answer, code_block = answer_question(item.question, docs)
    next_step = suggest_next(item.question)
    exec_out = None
    if item.run_code and code_block:
        exec_out = run_r_code_safe(code_block)
    return {
        "answer": answer,
        "citations": [d.metadata.get("source", "") for d in docs],
        "next_step": next_step,
        "r_output": exec_out,
    }

@app.get("/")
def root():
    return {"msg": "Stats‑and‑R‑Learning‑AI backend OK"}
