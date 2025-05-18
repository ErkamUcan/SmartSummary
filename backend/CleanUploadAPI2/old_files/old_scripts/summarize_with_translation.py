import os
import sys
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, T5Tokenizer, T5ForConditionalGeneration

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def translate(text, src_model_name, tokenizer_name):
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, use_auth_token=False)
    model = AutoModelForSeq2SeqLM.from_pretrained(src_model_name, use_auth_token=False).to(device)


    inputs = tokenizer.encode(text, return_tensors="pt", truncation=True, max_length=512).to(device)
    translated = model.generate(inputs, max_length=512, num_beams=4, early_stopping=True)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

def summarize_english(text):
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    model = T5ForConditionalGeneration.from_pretrained("t5-base").to(device)

    input_text = "summarize: " + text
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True).to(device)
    summary_ids = model.generate(inputs, max_length=128, min_length=40, num_beams=4, length_penalty=1.2, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def main():
    if len(sys.argv) != 2:
        print("Kullanım: python summarize_with_translation.py <chunk_dosya_yolu>")
        sys.exit(1)

    chunk_path = sys.argv[1]
    if not os.path.exists(chunk_path):
        print(f"❌ Dosya bulunamadı: {chunk_path}")
        sys.exit(1)

    with open(chunk_path, "r", encoding="utf-8") as f:
        turkish_text = f.read().strip()

    print("🔄 Türkçeden İngilizceye çeviriliyor...")
    english_text = translate(
        turkish_text,
        "Helsinki-NLP/opus-mt-tr-en",
        "Helsinki-NLP/opus-mt-tr-en"
    )

    print("📜 İngilizce özetleniyor...")
    english_summary = summarize_english(english_text)

    print("🔄 İngilizceden tekrar Türkçeye çeviriliyor...")
    turkish_summary = translate(
        english_summary,
        "Helsinki-NLP/opus-mt-en-tr",
        "Helsinki-NLP/opus-mt-en-tr"
    )

    output_path = os.path.join("Summaries", os.path.splitext(os.path.basename(chunk_path))[0] + "_t5_translated_summary.txt")
    os.makedirs("Summaries", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(turkish_summary)

    print("✅ Tamamlandı!")
    print("📝 Türkçe Özet:\n" + turkish_summary)

if __name__ == "__main__":
    main()
