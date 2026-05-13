# AI Portfolio Assistant 🤖💼

An intelligent, Retrieval-Augmented Generation (RAG) powered portfolio assistant. This application acts as a personal AI representative, capable of answering interview questions, detailing professional experience, and providing insights about the candidate based on a curated knowledge base.

## 🌟 Features

- **Local AI Inference**: Powered by local Large Language Models (LLMs) using `llama-cpp-python` (specifically designed for quantized `.gguf` models) ensuring complete privacy and offline capabilities.
- **Retrieval-Augmented Generation (RAG)**: Integrates `ChromaDB` for fast, local vector search, allowing the AI to pull context directly from a personalized knowledge base before answering.
- **High-Quality Embeddings**: Utilizes `SentenceTransformers` (`BAAI/bge-small-en-v1.5`) to map knowledge base text into highly accurate vector representations.
- **Flask Web Server**: A lightweight and fast backend API.
- **Clean UI**: A responsive, chat-like interface built with vanilla HTML/CSS/JS for interacting with the AI.

## 🛠️ Technology Stack

- **Backend Framework**: Flask
- **LLM Engine**: `llama-cpp-python` (Gemma-based models recommended)
- **Vector Database**: ChromaDB (Persistent Local Client)
- **Embedding Model**: `sentence-transformers`
- **Frontend**: HTML5, Vanilla JavaScript, CSS

## 📁 Project Structure

```text
ai-portfolio-assistant/
├── main.py                  # Main Flask application and LLM inference logic
├── ingest_kb.py             # Script to vectorize and store the knowledge base in ChromaDB
├── knowledge_base.json      # The raw text chunks containing professional/portfolio context
├── requirements.txt         # Python dependencies
├── .gitignore               # Ignored files (e.g., venv, pycache, Chroma DB cache)
├── static/
│   ├── script.js            # Frontend chat logic and API calls
│   └── style.css            # UI styling
└── templates/
    └── index.html           # Main frontend layout
```

## 🚀 Setup & Installation

### 1. Prerequisites

- Python 3.10+
- A compatible `.gguf` model downloaded locally (e.g., Gemma, Llama 3, Mistral). Update the `model_path` in `main.py` to point to your local model file.

### 2. Environment Setup

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/YOUR_USERNAME/ai-portfolio-assistant.git
cd ai-portfolio-assistant

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

*(Note: Depending on your hardware, you may want to install a hardware-accelerated version of `llama-cpp-python` for better performance).*

### 4. Prepare the Knowledge Base

1. Edit `knowledge_base.json` with your own professional information, resume details, and portfolio highlights.
2. Run the ingestion script to create the vector embeddings and populate ChromaDB:

```bash
python ingest_kb.py
```
*This will create an `interview_db` directory containing your local vector database.*

### 5. Run the Application

Start the Flask server:

```bash
python main.py
```

The application will be available at `http://127.0.0.1:5000/`.

## 💡 Usage

Once the server is running, navigate to the web interface in your browser. You can ask the assistant questions like:
- *"What is your experience with Machine Learning?"*
- *"Tell me about your latest projects."*
- *"Why are you a good fit for this role?"*

The assistant will query your embedded knowledge base for relevant context and formulate a professional, personalized response.

## 🤝 Contributing

Feel free to fork the repository and submit pull requests if you have ideas for improvements, such as UI enhancements, streaming responses, or multi-user support!

## 📜 License

MIT License
