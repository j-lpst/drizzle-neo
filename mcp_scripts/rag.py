import json
from pathlib import Path
from typing import List, Dict, Any

from sentence_transformers import SentenceTransformer, util


def rag(prompt: str, num_snippets: int, window_size: int) -> str:
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    archive_path = Path("./state/context-archive.json")
    if not archive_path.is_file():
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        archive_path.write_text(
            json.dumps({"history": []}, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    top_k = num_snippets
    window = window_size

    with open(archive_path, encoding="utf-8") as f:
        data = json.load(f)
    history = data.get("history", [])
    if not history:
        return ""

    for msg in history:
        if msg.get("content") is None:
            msg["content"] = ""

    q_emb = embedding_model.encode([prompt], normalize_embeddings=True)
    c_emb = embedding_model.encode([msg["content"] for msg in history], normalize_embeddings=True)

    scores = util.cos_sim(q_emb, c_emb).flatten()
    top_vals, top_idxs = scores.topk(k=min(top_k, len(history)), largest=True)

    blocks = []

    for rank, (score, idx) in enumerate(zip(top_vals.tolist(), top_idxs.tolist()), start=1):
        start = max(0, idx - window)
        end = min(len(history), idx + window + 1)

        header = f"===== Snippet Relevancy: {rank} (score: {score:.3f}) ====="

        body = "\n".join(
            f"{history[i]['role']}: {history[i]['content']}"
            for i in range(start, end)
        )

        blocks.append((rank, f"{header}\n{body}"))

    ordered_strings = [block for _, block in reversed(blocks)]

    return "\n\n".join(ordered_strings)
