import json
import pickle
from sentence_transformers import SentenceTransformer
import os
from tqdm import tqdm

# --- Config ---
DATA_PATH = os.path.join("data", "responses.json")
SAVE_PATH = os.path.join("utils", "vector_store.pkl")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- Load Response Data ---
def load_responses(path):
    with open(path, 'r') as f:
        return json.load(f)

# --- Embed Prompts ---
def build_embeddings(responses, model):
    prompts = [item['prompt'] for item in responses]
    embeddings = model.encode(prompts, show_progress_bar=True)
    vector_store = [
        {"embedding": emb.tolist(), "response": responses[i]["response"]}
        for i, emb in enumerate(embeddings)
    ]
    return vector_store

# --- Save Vector Store ---
def save_vector_store(vector_store, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        pickle.dump(vector_store, f)

# --- Main Execution ---
def main():
    print("\n[1] Loading responses...")
    responses = load_responses(DATA_PATH)

    print("[2] Initializing embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    print("[3] Encoding prompts into vectors...")
    vector_store = build_embeddings(responses, model)

    print("[4] Saving vector store to disk...")
    save_vector_store(vector_store, SAVE_PATH)

    print("\n✅ Vector store created successfully at:", SAVE_PATH)

if __name__ == "__main__":
    main()
