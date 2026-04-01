from openai import OpenAI
from qdrant_client import QdrantClient, models
from app.config import OPENAI_API_KEY, COLLECTION_NAME
from app.config import QDRANT_URL, QDRANT_API_KEY, REDIS_URL
import redis
import uuid

# OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Qdrant client
qdrant = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

# Redis client
redis_client = redis.from_url(REDIS_URL, decode_responses=True)


def embed(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def index_chunks(chunks):
    points = []

    for chunk in chunks:
        vector = embed(chunk)

        points.append(
            models.PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"text": chunk}
            )
        )

    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )


def query_rag(question):
    cache_key = f"rag:{question}"

    # ✅ Check cache
    cached = redis_client.get(cache_key)
    if cached:
        return cached

    query_vector = embed(question)

    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=3
    )

    context = "\n".join([r.payload["text"] for r in results])

    prompt = f"""
Answer ONLY from the context below.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content

    # ✅ Store in cache (1 hour)
    redis_client.set(cache_key, answer, ex=3600)

    return answer