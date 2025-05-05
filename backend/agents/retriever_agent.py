import pathlib
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document

_ROOT = pathlib.Path(__file__).resolve().parents[2]
_INDEX = _ROOT / "faiss_index"

_embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")
_vectorstore = FAISS.load_local(str(_INDEX), _embeddings) if _INDEX.exists() else None

def retrieve_chunks(question: str, k: int = 4) -> list[Document]:
    if _vectorstore is None:
        return []
    return _vectorstore.similarity_search(question, k=k)
