import sys
import io
import torch
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    BartForConditionalGeneration,
    BartTokenizer,
    pipeline
)

# UTF-8 karakter desteği
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("summarize_with_nllb_translation.py BAŞLADI", file=sys.stderr)

# === 1. Argüman kontrolü ===
if len(sys.argv) < 2:
    print("Kullanım: python summarize_with_nllb_translation.py <chunk_path | - >", file=sys.stderr)
    sys.exit(1)

input_arg = sys.argv[1]

# === 2. Metni oku (dosyadan ya da stdin'den) ===
if input_arg == "-":
    print("STDIN'den metin alınıyor...", file=sys.stderr)
    english_text = sys.stdin.read().strip()
else:
    with open(input_arg, "r", encoding="utf-8") as f:
        english_text = f.read().strip()

if not english_text:
    print("HATA: Giriş metni boş!", file=sys.stderr)
    sys.exit(1)

# === 3. İngilizce Özetleme (BART) ===
try:
    bart_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
    bart_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

    inputs = bart_tokenizer(english_text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = bart_model.generate(
        inputs["input_ids"],
        max_length=150,
        min_length=40,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )
    english_summary = bart_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
except Exception as e:
    print(f"HATA (özette): {e}", file=sys.stderr)
    sys.exit(1)

# === 4. Türkçeye Çeviri (NLLB) ===
try:
    nllb_model_id = "facebook/nllb-200-distilled-600M"
    nllb_tokenizer = AutoTokenizer.from_pretrained(nllb_model_id)
    nllb_model = AutoModelForSeq2SeqLM.from_pretrained(nllb_model_id)

    translator = pipeline(
        "translation",
        model=nllb_model,
        tokenizer=nllb_tokenizer,
        src_lang="eng_Latn",
        tgt_lang="tur_Latn"
    )

    translated = translator(english_summary, max_length=512)[0]['translation_text']
except Exception as e:
    print(f"HATA (çeviride): {e}", file=sys.stderr)
    sys.exit(1)

print("summarize_with_nllb_translation.py BİTTİ", file=sys.stderr)
print(translated)
