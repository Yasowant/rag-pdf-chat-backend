from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from app.config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

def init_collection():
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
    )