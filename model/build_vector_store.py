import json
import pickle
from sentence_transformers import SentenceTransformers
import os

# Paths
RESPONSES_PATH = os.path.join(os.path.dirname(__file__), '../data/responses.json')
VECTOR_STORE_PATH = os.path.join(os.path.dirname(__file__), '../utils/vector_store.pkl')

# Load responses
def load_responses():
    with open(RESPONSES_PATH, 'r', encoding='utf-8') as f:
        responses = json.load(f)
    return responses

# Build embeddings
def build_vector_store(responses, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    prompts = [item['prompt'] for item in responses]
    embeddings = model.encode(prompts, show_progress_bar=True)
    return {
        'prompts': prompts,
        'responses': [item['response'] for item in responses],
        'embeddings': embeddings
    }

# Save vector store
def save_vector_store(vector_store):
    with open(VECTOR_STORE_PATH, 'wb') as f:
        pickle.dump(vector_store, f)

if __name__ == '__main__':
    responses = load_responses()
    vector_store = build_vector_store(responses)
    save_vector_store(vector_store)
    print(f"Vector store built and saved to {VECTOR_STORE_PATH}")
