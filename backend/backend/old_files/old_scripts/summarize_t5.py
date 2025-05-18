import os
import sys
import torch
from transformers import MT5ForConditionalGeneration, MT5Tokenizer

try:
    if len(sys.argv) != 2:
        print("Kullanım: python summarize_t5.py <chunk_dosya_yolu>")
        sys.exit(1)

    chunk_path = sys.argv[1]

    if not os.path.exists(chunk_path):
        print(f"❌ Chunk dosyası bulunamadı: {chunk_path}")
        sys.exit(1)

    with open(chunk_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # ✅ Model ve tokenizer yükleniyor
    model_name = "google/mt5-base"
    tokenizer = MT5Tokenizer.from_pretrained(model_name)
    model = MT5ForConditionalGeneration.from_pretrained(model_name).to(device)

    # 📌 Prompt: "özetle:" ile model yönlendirilir
    input_text = "özetle: " + text

    input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True).to(device)

    summary_ids = model.generate(
        input_ids,
        max_length=128,
        min_length=40,
        num_beams=4,
        length_penalty=1.2,
        early_stopping=True
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # 📁 Sonucu kaydet
    summaries_dir = "Summaries"
    os.makedirs(summaries_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(chunk_path))[0]
    output_path = os.path.join(summaries_dir, f"{base_name}_t5_summary.txt")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"✅ T5 özetleme tamamlandı: {output_path}")
    print("📝 Özet:\n" + summary)

except Exception as e:
    print(f"❌ Hata oluştu: {str(e)}")
