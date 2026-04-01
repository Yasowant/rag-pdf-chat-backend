from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from app.pdf_loader import load_pdf, chunk_text
from app.rag import index_chunks, query_rag
from app.qdrant_client import init_collection
from app.ats import calculate_ats_score

app = FastAPI(
    title="Chat with PDF API + ATS on Chat"
)

# ✅ Store resume text (temporary memory)
resume_text_global = ""

# ✅ CORS
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

# ✅ Startup
@app.on_event("startup")
def startup():
    init_collection()

# ✅ Upload PDF (ONLY INDEX, NO ATS)
@app.post("/upload")
async def upload_pdf(file: UploadFile):
    global resume_text_global

    try:
        file_path = f"/tmp/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text
        text = load_pdf(file_path)

        if not text:
            return {"error": "No text found in PDF"}

        # ✅ Save for later ATS use
        resume_text_global = text

        # ✅ RAG indexing
        chunks = chunk_text(text)
        index_chunks(chunks)

        os.remove(file_path)

        return {"message": "PDF indexed successfully"}

    except Exception as e:
        return {"error": str(e)}

# ✅ Chat endpoint (ATS happens here)
@app.get("/chat")
def chat(query: str):
    global resume_text_global

    try:
        # 🔥 Detect ATS request
        if "ats" in query.lower() or "score" in query.lower():
            if not resume_text_global:
                return {"error": "No resume uploaded"}

            ats_result = calculate_ats_score(
                resume_text_global,
                query   # treat query as job description
            )

            return {
                "type": "ats",
                "result": ats_result
            }

        # ✅ Normal RAG chat
        answer = query_rag(query)
        return {
            "type": "chat",
            "answer": answer
        }

    except Exception as e:
        return {"error": str(e)}

# ✅ Health
@app.get("/")
def health():
    return {"status": "ok"}