```md id="be-readme-001"
# 🚀 Chat with PDF – Backend

A production-ready FastAPI backend for chatting with PDFs using RAG (Retrieval-Augmented Generation).

Upload a PDF → generate embeddings → store in Qdrant → query with OpenAI.

---

## 🧠 Features

- 📄 PDF upload & parsing
- 🔍 Semantic search with Qdrant
- 🤖 AI responses using OpenAI
- ⚡ FastAPI high-performance APIs
- 🧠 RAG architecture
- 🗂️ Vector database integration
- ⚡ Caching with Valkey (Redis alternative)
- 🐳 Fully Dockerized setup

---

## 🏗️ Tech Stack

- ⚡ FastAPI
- 🤖 OpenAI API
- 🔎 Qdrant (Vector DB)
- ⚡ Valkey (Redis)
- 📄 PyPDF
- 🐳 Docker & Docker Compose

---

## 📁 Project Structure

```

chat-with-pdf/
│
├── app/
│   ├── main.py              # FastAPI app
│   ├── rag.py               # RAG logic
│   ├── pdf_loader.py        # PDF parsing
│   ├── qdrant_client.py     # Vector DB
│   ├── valkey_client.py     # Cache
│   └── config.py            # Configs
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env

````

---

## ⚙️ Setup Instructions

### 1️⃣ Clone repository

```bash id="clone1"
git clone https://github.com/your-username/chat-with-pdf.git
cd chat-with-pdf
````

---

### 2️⃣ Create `.env`

```env id="env1"
OPENAI_API_KEY=your_openai_api_key
```

---

### 3️⃣ Run with Docker

```bash id="docker1"
docker-compose up --build
```

---

### 4️⃣ Access API

```id="apiurl"
http://localhost:8000/docs
```

👉 Swagger UI available

---

## 📡 API Endpoints

### 📄 Upload PDF

```http id="uploadapi"
POST /upload
```

**Request:**

* multipart/form-data
* key: `file`

---

### 💬 Chat with PDF

```http id="chatapi"
GET /chat?query=your_question
```

**Response:**

```json id="resp1"
{
  "answer": "AI-generated answer"
}
```

---

### ❤️ Health Check

```http id="healthapi"
GET /
```

---

## 🔄 How It Works (RAG Flow)

```

User Question
     ↓
Embedding (OpenAI)
     ↓
Vector Search (Qdrant)
     ↓
Relevant Context
     ↓
GPT Response
     ↓
Answer

```

---

## 🐳 Services

| Service | Port |
| ------- | ---- |
| FastAPI | 8000 |
| Qdrant  | 6333 |
| Valkey  | 6379 |

---

## ⚠️ Common Issues

### ❌ CORS Error

Fix in `main.py`:

```python id="corsfix"
allow_origins=["http://localhost:8080"]
```

---

### ❌ Port already in use

```bash id="fixport"
docker-compose down -v
```

---

### ❌ OpenAI error

* Check API key
* Check `.env` file

---

## 🔥 Environment Variables

| Variable       | Description    |
| -------------- | -------------- |
| OPENAI_API_KEY | OpenAI API key |

---

## 🚀 Future Improvements

* 📁 Multi-PDF support
* 💬 Chat memory
* ⚡ Streaming responses
* 🔐 Authentication
* 📊 Analytics
* 🌐 Deployment (AWS/GCP)

---

## 👨‍💻 Author

**Yasowant**

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!

```

---

# 💥 DONE

This backend README includes:

- ✅ Setup (Docker + env)
- ✅ API docs
- ✅ RAG explanation
- ✅ Debugging help
- ✅ Clean structure

---
