from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import shutil

from app.pdf_loader import load_pdf, chunk_text
from app.rag import index_chunks, query_rag
from app.qdrant_client import init_collection

app = FastAPI(
    title="Chat with PDF API"
)

# ✅ CORS FIX (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "https://rag-pdf-chat-frontend.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Startup event
@app.on_event("startup")
def startup():
    init_collection()

# ✅ Upload PDF
@app.post("/upload")
async def upload_pdf(file: UploadFile):
    file_path = f"/tmp/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = load_pdf(file_path)
    chunks = chunk_text(text)

    index_chunks(chunks)

    return {"message": "PDF indexed successfully"}

# ✅ Chat endpoint
@app.get("/chat")
def chat(query: str):
    answer = query_rag(query)
    return {"answer": answer}

# ✅ Health check (optional but useful)
@app.get("/")
def health():
    return {"status": "ok"}