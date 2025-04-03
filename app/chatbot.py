import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import json

# --- Paths ---
DATA_PATH = os.path.join("data", "responses_witty_500.json")
VECTOR_STORE_PATH = os.path.join("utils", "vector_store.pkl")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- Load vector store ---
def load_vector_store(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

# --- Load original prompts/responses (optional fallback if needed) ---
def load_responses(path):
    with open(path, 'r') as f:
        return json.load(f)

# --- Get best matching response ---
def find_best_response(user_input, vector_store, model, top_k=1):
    user_vec = model.encode([user_input])
    stored_vecs = np.array([np.array(entry['embedding']) for entry in vector_store])
    similarities = cosine_similarity(user_vec, stored_vecs)[0]
    top_index = np.argmax(similarities)
    best_match = vector_store[top_index]
    return best_match['response'], similarities[top_index]

# --- Main Chat Loop ---
def chat():
    print("\n🤖 Semantic Witty Assistant is online! Type something and get sassified.")
    model = SentenceTransformer(EMBEDDING_MODEL)
    vector_store = load_vector_store(VECTOR_STORE_PATH)

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Bot: Catch you later. I'll just be here... processing existence.")
            break
        response, score = find_best_response(user_input, vector_store, model)
        print(f"Bot: {response}")

if __name__ == '__main__':
    chat()