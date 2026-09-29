from vector_store import search_vector_memory
from local_brain import ask_local_peppo


# ==========================================
# RAG + QWEN
# ==========================================

def ask_peppo_with_memory(question):

    # --------------------------------------
    # SEARCH VECTOR MEMORY
    # --------------------------------------

    memories = search_vector_memory(
        question,
        limit=3
    )

    # --------------------------------------
    # BUILD MEMORY CONTEXT
    # --------------------------------------

    if memories:

        memory_context = "\n".join(
            f"- {memory}"
            for memory in memories
        )

    else:

        memory_context = "No relevant memories found."


    # --------------------------------------
    # BUILD PROMPT FOR QWEN
    # --------------------------------------

    prompt = f"""
Relevant memories about the user:

{memory_context}

User's question:

{question}

Use the relevant memories when answering.
Do not mention the memory system.
Do not say that you searched a database.
Answer naturally as Peppo.
"""


    # --------------------------------------
    # ASK LOCAL QWEN
    # --------------------------------------

    response = ask_local_peppo(
        prompt
    )

    return response


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print("Peppo RAG + Qwen Test")
    print("=====================")

    question = (
        "What kinds of things am I interested in?"
    )

    response = ask_peppo_with_memory(
        question
    )

    print("\nPeppo:", response)