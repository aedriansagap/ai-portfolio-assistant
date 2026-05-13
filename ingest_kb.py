import json
import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="./interview_db")
collection = client.get_or_create_collection(name="interview_kb")

model = SentenceTransformer('BAAI/bge-small-en-v1.5')

try:
    with open("knowledge_base.json", "r") as f:
        lore_chunks = json.load(f)
except Exception as e:
    print(f"Error loading knowledge_base.json: {e}")
    exit(1)

for i, text in enumerate(lore_chunks):
    vector = model.encode(text).tolist()
    collection.upsert(
        ids=[f"id_{i}"],
        embeddings=[vector],
        documents=[text]
    )

print("Knowledge base successfully updated")