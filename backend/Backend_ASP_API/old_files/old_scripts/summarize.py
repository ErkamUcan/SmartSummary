import os
import sys
import torch
from transformers import MT5ForConditionalGeneration, MT5Tokenizer

try:
    if len(sys.argv) != 2:
        print("Kullanım: python summarize.py <chunk_dosya_yolu>", flush=True)
        sys.exit(1)

    chunk_path = sys.argv[1]

    if not os.path.exists(chunk_path):
        print(f"Chunk dosyası bulunamadı: {chunk_path}", flush=True)
        sys.exit(1)

    with open(chunk_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    # GPU kullanımı ayarı
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Model ve tokenizer yükleniyor
    tokenizer = MT5Tokenizer.from_pretrained("google/mt5-base")
    model = MT5ForConditionalGeneration.from_pretrained("google/mt5-base").to(device)

    # Prompt Türkçeleştirildi
    input_text = "summarize: " + text  # veya "özetle: " da deneyebilirsin

    input_ids = tokenizer.encode(
    input_text,
    return_tensors="pt",
    max_length=512,
    truncation=True
    ).to(device)

    summary_ids = model.generate(
    input_ids,
    max_length=300,
    min_length=50,
    length_penalty=1.5,
    num_beams=5,
    early_stopping=True
)


    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # Çıktıyı kaydetme
    summaries_dir = "Summaries"
    os.makedirs(summaries_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(chunk_path))[0]
    output_path = os.path.join(summaries_dir, f"{base_name}_summary.txt")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)

    # Bilgilendirme
    print(f"✅ Özetleme tamamlandı: {output_path}", flush=True)
    print("📝 Özet:\n" + summary, flush=True)

except Exception as e:
    print(f"❌ Hata oluştu: {str(e)}", flush=True)
