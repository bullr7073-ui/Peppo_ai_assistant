from brain_manager import (
    ask_peppo,
    switch_brain,
    get_current_brain
)


print("Current brain:")
print(get_current_brain())


print("\nTesting local brain + RAG...")

response = ask_peppo(
    "What kinds of things am I interested in?"
)

print("\nPeppo:")
print(response)