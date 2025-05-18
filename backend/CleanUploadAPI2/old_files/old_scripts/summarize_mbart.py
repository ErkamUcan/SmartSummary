import os
import sys
import torch
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

try:
    if len(sys.argv) != 2:
        print("Kullanım: python summarize_mbart.py <chunk_dosya_yolu>")
        sys.exit(1)

    chunk_path = sys.argv[1]

    if not os.path.exists(chunk_path):
        print(f"❌ Chunk dosyası bulunamadı: {chunk_path}")
        sys.exit(1)

    with open(chunk_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # ✅ Model ve tokenizer yükleniyor
    model_name = "facebook/mbart-large-50-many-to-many-mmt"
    tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
    model = MBartForConditionalGeneration.from_pretrained(model_name).to(device)

    # 🌍 Türkçe dili ayarlanıyor
    tokenizer.src_lang = "tr_TR"
    tokenizer.tgt_lang = "tr_TR"

    # 📌 Türkçe prompt ile yönlendirme
    input_text = "Bu metni sadece 2 cümle ile özetle : " + text

    input_ids = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512).input_ids.to(device)

    # ✅ Türkçe çıktı garantisi için BOS token ayarı
    summary_ids = model.generate(
        input_ids,
        max_length=128,
        min_length=40,
        num_beams=4,
        length_penalty=1.2,
        early_stopping=True,
        forced_bos_token_id=tokenizer.lang_code_to_id["tr_TR"]
    )

    summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True)[0]

    # 📁 Özet dosyası kaydediliyor
    summaries_dir = "Summaries"
    os.makedirs(summaries_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(chunk_path))[0]
    output_path = os.path.join(summaries_dir, f"{base_name}_mbart_summary.txt")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"✅ MBART özetleme tamamlandı: {output_path}")
    print("📝 Özet:\n" + summary)

except Exception as e:
    print(f"❌ Hata oluştu: {str(e)}")
