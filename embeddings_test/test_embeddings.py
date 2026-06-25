"""
Embedding test: pass words/phrases, inspect the resulting vectors.

Model: all-MiniLM-L6-v2
  - 384-dimensional dense vectors
  - ~80MB download on first run, cached locally after that
  - No API key needed

Run: uv run python embeddings_test/test_embeddings.py
"""

import matplotlib.pyplot as plt
import numpy as np
from sentence_transformers import SentenceTransformer

# ── Words / phrases to embed ─────────────────────────────────────────────────
WORDS = [
    "Interest Rates hikes",
    "Monetary policy tightening",
    "Sustainability",
    "Central Bank",
    "Inflation",
    "Quantitative Easing",
    "Fiscal Policy",
    "Money",
    "Exchange Rates",
    "Currency Depreciation"]

# ── Load model & generate embeddings ─────────────────────────────────────────
print("Loading model…")
model = SentenceTransformer("all-MiniLM-L6-v2")

print(f"Encoding {len(WORDS)} words…\n")
embeddings = model.encode(WORDS, show_progress_bar=False)  # shape: (N, 384)

# ── Inspect vectors ───────────────────────────────────────────────────────────
print("=" * 60)
print(f"Vector shape per word: {embeddings[0].shape}")
print(f"dtype: {embeddings.dtype}")
print()

for word, vec in zip(WORDS, embeddings):
    preview = ", ".join(f"{v:.4f}" for v in vec[:6])
    print(f"  {word:<20} [{preview}, …]")

# ── Cosine similarity matrix ──────────────────────────────────────────────────
print("\n" + "=" * 60)
print("Cosine similarity matrix (1.0 = identical, 0.0 = unrelated):\n")

norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
normed = embeddings / norms
sim_matrix = normed @ normed.T

# Print header
col_width = 12
header = " " * 22 + "".join(f"{w[:col_width]:<{col_width}}" for w in WORDS)
print(header)

for i, word_i in enumerate(WORDS):
    row = f"  {word_i:<20}"
    for j in range(len(WORDS)):
        val = sim_matrix[i, j]
        marker = "■" if val > 0.7 and i != j else " "
        row += f"{val:>6.3f}{marker}     "
    print(row)

# ── Most similar pairs ────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("Top 5 most similar pairs:\n")

pairs = []
for i in range(len(WORDS)):
    for j in range(i + 1, len(WORDS)):
        pairs.append((sim_matrix[i, j], WORDS[i], WORDS[j]))

pairs.sort(reverse=True)
for score, a, b in pairs[:5]:
    print(f"  {score:.3f}  {a}  <->  {b}")

print("\nDone.")

# ── Heatmap ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 7))

im = ax.imshow(sim_matrix, vmin=0, vmax=1, cmap="RdYlGn")
fig.colorbar(im, ax=ax, label="Cosine similarity")

ax.set_xticks(range(len(WORDS)))
ax.set_yticks(range(len(WORDS)))
ax.set_xticklabels(WORDS, rotation=45, ha="right", fontsize=10)
ax.set_yticklabels(WORDS, fontsize=10)

for i in range(len(WORDS)):
    for j in range(len(WORDS)):
        val = sim_matrix[i, j]
        color = "white" if val < 0.35 or val > 0.75 else "black"
        ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=8, color=color)

ax.set_title("Cosine Similarity between Word Embeddings", fontsize=13, pad=14)
fig.tight_layout()
plt.savefig("embeddings_test/similarity_heatmap.png", dpi=150)
print("Heatmap saved to embeddings_test/similarity_heatmap.png")
plt.show()
