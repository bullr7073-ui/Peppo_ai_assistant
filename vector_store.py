import chromadb
from sentence_transformers import SentenceTransformer


# ==========================================
# VECTOR DATABASE
# ==========================================

CHROMA_PATH = "peppo_vectors"

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


# ==========================================
# EMBEDDING MODEL
# ==========================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ==========================================
# MEMORY COLLECTION
# ==========================================

collection = client.get_or_create_collection(
    name="peppo_memory"
)


# ==========================================
# ADD MEMORY
# ==========================================

def add_vector_memory(text):

    embedding = model.encode(
        text
    ).tolist()

    memory_id = str(
        collection.count() + 1
    )

    collection.add(
        ids=[memory_id],
        documents=[text],
        embeddings=[embedding]
    )

    return memory_id


# ==========================================
# SEARCH MEMORY
# ==========================================

def search_vector_memory(
    query,
    limit=3
):

    query_embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=limit
    )

    return results["documents"][0]


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print("Peppo Vector Memory Test")
    print("------------------------")

    add_vector_memory(
        "I love Formula 1."
    )

    add_vector_memory(
        "I want to learn AR and VR."
    )

    add_vector_memory(
        "I enjoy technology and artificial intelligence."
    )

    results = search_vector_memory(
        "What technology topics am I interested in?"
    )

    print("\nRelevant memories:")

    for memory in results:

        print("-", memory)