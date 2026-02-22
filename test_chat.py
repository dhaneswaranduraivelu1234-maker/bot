from app.rag_pipeline import ask_question

print("🎓 NITT Hybrid Chatbot Ready (type 'exit')\n")

while True:
    q = input("You: ")

    if q.lower() == "exit":
        break

    answer = ask_question(q)
    print("\nBot:", answer)
    print("-" * 50)
