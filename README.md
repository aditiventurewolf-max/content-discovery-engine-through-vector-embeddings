# Content Discovery Engine

A framework for semantic search and content discovery utilizing vector embeddings.

## Project Structure

- `.env`: Contains your private environment variables (API keys). This file should **not** be committed to version control.
- `.env.example`: A template showing the required environment variables.
- `requirements.txt`: Python package dependencies for the project.
- `.venv/`: The Python isolated virtual environment.
- `src/`: The directory where the application's main code will be placed.
  - `embeddings/`: Will contain logic for generating vector embeddings (e.g., with Google Generative AI).
  - `search/`: Will contain logic for vector storage and retrieval (e.g., using Pinecone).
  - `ingestion/`: Will contain scripts for parsing content feeds (e.g., with feedparser).

## Setup Instructions

1. **Activate the Virtual Environment**:
   Ensure you're using the provided virtual environment to keep your dependencies isolated.
   ```bash
   source .venv/bin/activate
   ```

2. **Install Dependencies**:
   Install the necessary libraries (`google-generativeai`, `pinecone-client`, etc.):
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup**:
   Open the `.env` file (or copy `.env.example` to `.env` if not present) and add your actual API credentials:
   ```env
   GEMINI_API_KEY=your_actual_gemini_key
   PINECONE_API_KEY=your_actual_pinecone_key
   ```
