"""Build FAISS vector index from markdown files in data/."""
import pathlib, glob
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "faiss_index"
emb = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

docs = []
for file in glob.glob(str(DATA_DIR / "*.md")):
    text = pathlib.Path(file).read_text(encoding="utf-8")
    for i, chunk in enumerate(splitter.split_text(text)):
        docs.append(Document(page_content=chunk,
                             metadata={"source": f"{pathlib.Path(file).name}#p{i}"}))

if docs:
    db = FAISS.from_documents(docs, emb)
    db.save_local(str(OUT_DIR))
    print(f"Indexed {len(docs)} chunks → {OUT_DIR}")
else:
    print("No markdown files found in data/. Nothing indexed.")
