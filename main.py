from flask import Flask, request, jsonify, render_template
from llama_cpp import Llama
import chromadb
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# Setup Context Global variables
print("Initializing Aedrian's AI Assistant (Loading Model & ChromaDB)")
llm = Llama(model_path="/home/aedriansagap/models/gguf/Gemma-4-E4B-Uncensored-HauhauCS-Aggressive-Q5_K_M.gguf", n_ctx=2048)
try:
    db = chromadb.PersistentClient(path="./interview_db").get_collection("interview_kb")
except Exception as e:
    print(f"Failed to load DB collection: {e}. Was ingest_kb.py run?")
    db = None
embed_model = SentenceTransformer('BAAI/bge-small-en-v1.5')
print("Assistant Ready.")

def ask_assistant(query):
    context = ""
    # 1. Retrieve the truth
    if db:
        query_vec = embed_model.encode(query).tolist()
        results = db.query(query_embeddings=[query_vec], n_results=2)
        if results['documents'] and results['documents'][0]:
            context = "\n".join(results['documents'][0])

    # 2. Construct the Prompt
    messages = [
        {"role": "system", "content": f"You are Aedrian's AI Assistant. You are representing Aedrian Sagap in an interview context. Answer the user's questions professionally, warmly, and accurately based strictly on the provided Context. Be concise.\nContext: {context}"},
        {"role": "user", "content": query}
    ]

    # 3. Generate
    output = llm.create_chat_completion(messages=messages, max_tokens=150)
    return output['choices'][0]['message']['content']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"error": "No query provided"}), 400
    
    query = data['query']
    try:
        response = ask_assistant(query)
        return jsonify({"response": response})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Threaded False might be necessary for Llama.cpp stability in some environments, but Flask does threading by default.
    app.run(debug=True, port=5000, threaded=False)