import os
import sys

# ── Force the correct virtual environment ────────────────────────────────────
_VENV_PY = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".venv", "bin", "python")
if os.path.exists(_VENV_PY) and os.path.abspath(sys.executable) != os.path.abspath(_VENV_PY):
    print(f"[INFO] Re-launching with project venv: {_VENV_PY}")
    os.execv(_VENV_PY, [_VENV_PY] + sys.argv)
# ─────────────────────────────────────────────────────────────────────────────

# Add project root to path natively so we can import src.search
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv  # type: ignore
load_dotenv()

from src.search.store import save_seed  # type: ignore

def run_seed():
    print("=========================================")
    print("  PLANTING SEEDS IN PINECONE DATABASE")
    print("=========================================\n")
    
    seeds = [
        {
            "title": "Paul Graham on Thinking and Writing",
            "description": "Any essay by Paul Graham exploring how the process of writing is intrinsically linked to the process of thinking. It emphasizes that writing forces clarity of thought and helps uncover new counterintuitive ideas."
        },
        {
            "title": "Finite and Infinite Games",
            "description": "The concept of Finite and Infinite Games by James Carse. The philosophical idea that life consists of two types of games. Finite games are played to win and end, while infinite games are played indefinitely for the purpose of continuing the play."
        },
        {
            "title": "Writing is Thinking",
            "description": "The idea that writing is thinking — clarity of prose is a cognitive skill. It posits that the act of articulating ideas clearly in prose is fundamentally a cognitive exercise that sharpens logic, reasoning, and depth of insight."
        },
        {
            "title": "The Backwards Law",
            "description": "The backwards law — wanting something reduces your chance of getting it. The paradoxical idea that the more forcefully you pursue something, like happiness or success, the further it slips away. Acceptance allows natural emergence."
        },
        {
            "title": "AI Agents and Execution Loops",
            "description": "How AI agents work — LLMs that take actions in loops with tools and memory. The mechanics of how autonomous agents utilize Large Language Models to reason, formulate plans, and take actions in iterative execution loops."
        }
    ]
    
    success_count: int = 0
    
    for idx, seed in enumerate(seeds, 1):
        print(f"Planting Seed #{idx}: {seed['title']}")
        
        success = save_seed(seed["title"], seed["description"])
        
        if success:
            print(f"  --> [SUCCESS] Successfully saved to Pinecone index.\n")
            success_count += 1  # type: ignore[assignment]
        else:
            print(f"  --> [FAIL] Could not save to Pinecone.\n")
            
    print("=========================================")
    print(f"  FINISHED: Planted {success_count}/{len(seeds)} seeds.")
    print("=========================================")

if __name__ == "__main__":
    run_seed()
