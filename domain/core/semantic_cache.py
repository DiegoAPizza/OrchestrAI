import redis
import json
import hashlib
from sentence_transformers import SentenceTransformer
from typing import Optional
import numpy as np
import os
redis_host = os.getenv("REDIS_HOST", "localhost")

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
SIMILARITY_THRESHOLD = 0.75  # distancia coseno mínima para considerar hit

class SemanticCache:
    def __init__(self, ttl: int = 3600):
        self.client = redis.Redis(host=redis_host, port=6379, decode_responses=True)
        self.ttl = ttl
    
    def _embedding(self, text: str) -> list:
        return model.encode(text).tolist()
    
    def _cosine_similarity(self, a: list, b: list) -> float:
        a, b = np.array(a), np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    
    def get(self, topic: str) -> Optional[dict]:
        # 1. Generar embedding del topic
        topic_embedding = self._embedding(topic)
        # 2. Buscar todos los keys de cache en Redis (prefijo "cache:*")
        cache_keys = self.client.keys("cache:*")
        # 3. Para cada key, comparar similitud con el topic
        for key in cache_keys:
            cache_data = json.loads(self.client.get(key))
            cached_embedding = cache_data["embedding"]
            similarity = self._cosine_similarity(topic_embedding, cached_embedding)
            print(f"DEBUG similitud: {similarity:.4f} — '{cache_data['topic']}'")  # ← temporal
            if similarity >= SIMILARITY_THRESHOLD:
                return cache_data["result"]
            # 5. Si no hay hit, retornar None
        return None
    
    def set(self, topic: str, result: dict) -> None:
        # 1. Generar embedding del topic
        topic_embeddings=self._embedding(topic)
        # 2. Guardar en Redis con key "cache:{hash_del_topic}"
        key = f"cache:{hashlib.md5(topic.encode()).hexdigest()}"
        cache_data = {
            "topic": topic,
            "embedding": topic_embeddings,
            "result": result
        }
        # 3. Guardar: {"topic": topic, "embedding": [...], "result": result}
        self.client.setex(
            key,
            self.ttl,
            json.dumps(cache_data)
        )
        # 4. Setear TTL
        