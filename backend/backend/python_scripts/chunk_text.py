import sys
import os
import nltk
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')



print("chunk_text.py BAŞLADI", file=sys.stderr)
nltk.download('punkt', quiet=True)

if len(sys.argv) < 2:
    print("Kullanım: python chunk_text.py <transcript_path>", file=sys.stderr)
    sys.exit(1)

transcript_path = sys.argv[1]
video_id = os.path.splitext(os.path.basename(transcript_path))[0]

with open(transcript_path, "r", encoding="utf-8") as f:
    text = f.read()

sentences = nltk.sent_tokenize(text)
chunks = [sentences[i:i + 2] for i in range(0, len(sentences), 2)]

os.makedirs("Chunks", exist_ok=True)
output_paths = []

for i, chunk in enumerate(chunks):
    out_path = os.path.join("Chunks", f"{video_id}_chunk_{i}.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(" ".join(chunk))
    output_paths.append(out_path)

print("chunk_text.py BİTTİ", file=sys.stderr)
print(output_paths[-1])  # son chunk yeterli
