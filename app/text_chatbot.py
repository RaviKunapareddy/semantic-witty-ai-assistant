import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sentence_transformers import SentenceTransformer
from utils.chat_core import load_vector_store, find_best_response
from utils.streaming import stream_print
from utils.feedback import log_feedback

VECTOR_STORE_PATH = os.path.join("utils", "vector_store.pkl")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def chat():
    print("\n🤖 Semantic Witty Assistant is online! Type something and get sassified.")
    model = SentenceTransformer(EMBEDDING_MODEL)
    vector_store = load_vector_store(VECTOR_STORE_PATH)

    turn_count = 0
    FEEDBACK_INTERVAL = 5
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Bot: Catch you later. I'll just be here... processing existence.")
            break
        response, score = find_best_response(user_input, vector_store, model)
        print("Bot: ", end="", flush=True)
        stream_print(response)
        turn_count += 1
        if turn_count % FEEDBACK_INTERVAL == 0:
            feedback = input("How was my wit? \U0001F610 \U0001F60F \U0001F602 (1=meh, 2=smirk, 3=LOL, Enter to skip): ").strip()
            if feedback in ['1', '2', '3']:
                log_feedback(user_input, response, feedback)

if __name__ == '__main__':
    chat()