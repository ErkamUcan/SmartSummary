import sys
import os
import io
import torch
from sentence_transformers import SentenceTransformer, util

# UTF-8 karakter desteği
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("semantic_search.py BAŞLADI", file=sys.stderr)

if len(sys.argv) < 3:
    print("Kullanım: python semantic_search.py <soru> <video_id>", file=sys.stderr)
    sys.exit(1)

question = sys.argv[1]
video_id = sys.argv[2]
chunks_folder = "Chunks"
top_n = 3  # En iyi kaç chunk alınsın?

device = "cpu"

try:
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2", device=device)
except Exception as e:
    print(f"Model yüklenirken hata: {e}", file=sys.stderr)
    sys.exit(1)

chunk_paths = [os.path.join(chunks_folder, f) for f in os.listdir(chunks_folder) if f.startswith(video_id)]

if not chunk_paths:
    print(f"HATA: {video_id} için chunk dosyası bulunamadı!", file=sys.stderr)
    sys.exit(1)

chunks = []
valid_paths = []
for path in chunk_paths:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if content:
            chunks.append(content)
            valid_paths.append(path)
        else:
            print(f"UYARI: {path} dosyası boş", file=sys.stderr)

if not chunks:
    print("HATA: Chunk içerikleri boş!", file=sys.stderr)
    sys.exit(1)

chunk_embeddings = model.encode(chunks, convert_to_tensor=True, device=device)
question_embedding = model.encode(question, convert_to_tensor=True, device=device)

cosine_scores = util.cos_sim(question_embedding, chunk_embeddings)[0]
top_indices = torch.topk(cosine_scores, k=min(top_n, len(cosine_scores))).indices.tolist()

selected_chunks = [chunks[i] for i in top_indices]

# Sıralı birleştirme (istenirse skor sırasına göre değil dosya sırasına göre de yapılabilir)
combined_text = "\n".join(selected_chunks)

print("semantic_search.py BİTTİ", file=sys.stderr)
print(combined_text)  # stdout'a birleştirilmiş özetlenecek metin gönderilir
