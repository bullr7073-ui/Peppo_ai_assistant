from brain_manager import ask_peppo


print("\nTesting Peppo brain...\n")

response = ask_peppo(
    "Hey Peppo, explain in simple words what you can help me with."
)

print("\nPeppo:")
print(response)