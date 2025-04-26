import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# utils/chat_core.py
# Shared logic for chatbot apps (used by app/text_chatbot.py and app/voice_chatbot.py)
# Provides vector store loading and response selection.

def load_vector_store(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def find_best_response(user_input, vector_store, model):
    user_vec = model.encode([user_input])
    stored_vecs = np.array([np.array(entry['embedding']) for entry in vector_store])
    similarities = cosine_similarity(user_vec, stored_vecs)[0]
    top_index = np.argmax(similarities)
    best_match = vector_store[top_index]
    return best_match['response'], similarities[top_index]
