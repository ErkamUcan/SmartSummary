import sys
import io
from bert_score import score

# UTF-8 karakter desteği
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("evaluate_summary.py BAŞLADI", file=sys.stderr)

if len(sys.argv) < 3:
    print("Kullanım: python evaluate_summary.py <candidate_summary_path> <reference_summary_path>", file=sys.stderr)
    sys.exit(1)

candidate_path = sys.argv[1]
reference_path = sys.argv[2]

try:
    with open(candidate_path, "r", encoding="utf-8") as f:
        candidate = [f.read().strip()]
    with open(reference_path, "r", encoding="utf-8") as f:
        reference = [f.read().strip()]

    if not candidate[0] or not reference[0]:
        print("HATA: Dosyalardan biri boş!", file=sys.stderr)
        sys.exit(1)

    P, R, F1 = score(candidate, reference, lang="tr", verbose=False)
    final_score = F1.mean().item()

    print("evaluate_summary.py BİTTİ", file=sys.stderr)
    print(f"F1 Skoru: {final_score:.4f} (BERTScore - Türkçe semantik benzerlik)")

except Exception as e:
    print(f"HATA: {e}", file=sys.stderr)
    sys.exit(1)
