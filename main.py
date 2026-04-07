import os 
import sys 
import subprocess

# ── Force the correct virtual environment ────────────────────────────────────
# If this script is NOT already running inside the project .venv, re-launch
# itself with the correct interpreter automatically. This happens when the
# user types plain `python main.py` instead of `.venv/bin/python main.py`.
_VENV_PY = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".venv", "bin", "python")
if os.path.exists(_VENV_PY) and os.path.abspath(sys.executable) != os.path.abspath(_VENV_PY):
    print(f"[INFO] Re-launching with project venv: {_VENV_PY}")
    os.execv(_VENV_PY, [_VENV_PY] + sys.argv)
# ─────────────────────────────────────────────────────────────────────────────

try:
    from dotenv import load_dotenv  # type: ignore
    import feedparser  # type: ignore
    from pinecone import Pinecone # type: ignore

except ImportError:
    print("Missing dependencies detected! Installing them right now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv", "feedparser", "google-generativeai", "pinecone", "numpy"])
    from dotenv import load_dotenv  # type: ignore
    import feedparser  # type: ignore

# Automatically load environment variables before importing ML libraries
load_dotenv()

# Add the project root to sys.path so we can import from src regardless of where the script is run
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.search.store import find_similar  # type: ignore
from src.scorer import evaluate_article  # type: ignore

# 1. Provide a curated list of AI/Philosophy/Psychology RSS feeds
FEEDS = [
    "https://bair.berkeley.edu/blog/feed.xml",          # AI & Machine Learning Research
    "https://astralcodexten.substack.com/feed",         # Rationality / Philosophy
    "https://waitbutwhy.com/feed",                      # Deep Thinking / Psychology
    "https://fs.blog/feed/",                            # Mental Models / Philosophy
    "https://dailynous.com/feed/"                       # Philosophy News / Ideas
]

def run_pipeline():
    print("\n=========================================")
    print("Starting Content Discovery Engine Pipeline")
    print("=========================================\n")
    
    passed_articles = []
    
    for feed_url in FEEDS:
        print(f"\n[FETCHING] -> {feed_url}")
        feed = feedparser.parse(feed_url)
        
        # 2. Pull the latest 10 articles from each feed
        entries = feed.entries[:10]
        
        for entry in entries:
            title = entry.get('title', 'Unknown Title')
            link = entry.get('link', '')
            summary = entry.get('summary', '')
            
            content_text = f"{title}\n{summary}"
            
            # 3. Check similarity against user profile (store.py)
            sim_score = find_similar(content_text)
            
            if sim_score > 0.75:
                print(f"  [PASS: {sim_score:.2f}] {title[:60]}...")
                
                # 4. Score the article intelligently with Gemini (scorer.py)
                score_data = evaluate_article(title, summary)
                final_score = score_data.get('final_score', 0.0)
                
                # 5. Collect articles holding a final score >= 6.5
                if final_score >= 6.5:
                    print(f"    -> [SCORED {final_score:.1f}/10] Added to collection!")
                    passed_articles.append({
                        'title': title,
                        'source': feed.feed.get('title', 'Unknown Source'),
                        'score': final_score,
                        'reason': score_data.get('reason', 'No reasoning provided.'),
                        'link': link
                    })
                else:
                    print(f"    -> [SCORED {final_score:.1f}/10] Rejected.")
            else:
                pass # Filtered out due to irrelevant similarity threshold
                
    # 6. Rank and Print the Final Results
    print("\n\n" + "*"*60)
    print("              FINAL RECOMMENDATIONS               ")
    print("*"*60)
    
    if not passed_articles:
        print("\nNo articles met the high threshold criteria today.")
        return
        
    # Sort descending by final score
    passed_articles.sort(key=lambda x: float(x['score']), reverse=True)
    
    for idx, article in enumerate(passed_articles, 1):
        print(f"\n{idx}. {article['title']}")
        print(f"   Source : {article['source']}")
        print(f"   Score  : {float(article['score']):.1f}/10.0")
        print(f"   Reason : {article['reason']}")
        print(f"   Link   : {article['link']}")

if __name__ == "__main__":
    run_pipeline()
