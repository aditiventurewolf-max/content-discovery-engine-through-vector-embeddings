# Content Discovery Engine

Reads recent posts from a few blogs and shows only the ones that match what I care about.

## Pipeline (from `main.py`)

1. Fetch the 10 most recent entries from each of five RSS feeds (BAIR blog, Astral Codex Ten, Wait But Why, Farnam Street, Daily Nous).
2. Look up similarity against a Pinecone index of seed topics (short descriptions of things I like). Keep items with similarity above 0.75.
3. Ask an LLM (Gemini) to score each remaining item. Keep scores of 6.5 or higher.
4. Print the results with the score and link.

`seed.py` loads example seed topics into Pinecone.

## Stack

Python, Google Gemini, Pinecone, feedparser, python-dotenv, numpy.

## Run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# add your Gemini and Pinecone keys to a .env file
python seed.py
python main.py
```

## Limitations

- Feeds and seed topics are hard-coded, and there is no history or de-duplication across runs.
- Some modules that `main.py` imports (`src.search.store`, `src.scorer`) are currently inside `src.zip` and need to be unzipped to run it.
- `test_migration.py` only checks that imports and the client load. It makes no API calls.
- No evaluation of whether the filtered list beats the raw feed.
