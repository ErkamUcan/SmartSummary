import os
import subprocess
import sys

def log(msg):
    print(msg, flush=True)

# === 0. Komut satırı argümanı kontrolü ===
if len(sys.argv) < 3:
    log("Kullanım: python run_pipeline.py <video_dosyası.mp4> <soru>")
    sys.exit()

video_filename = sys.argv[1]
question = sys.argv[2]
video_id = os.path.splitext(video_filename)[0]

video_path = os.path.join("Uploads", video_filename)
wav_path = video_path.replace(".mp4", ".wav")
transcript_path = os.path.join("Transcripts", f"{video_id}.txt")

# === 1. Ses çıkarma ===
log("=== [1] Ses çıkarma işlemi başlıyor ===")
result = subprocess.run(["python", "python_scripts/extract_audio.py", video_path], capture_output=True, text=True)
log("STDOUT:\n" + result.stdout)
log("STDERR:\n" + result.stderr)
if result.returncode != 0:
    log("Ses çıkarma başarısız.")
    sys.exit()
log("Ses çıkarma tamamlandı.")

# === 2. Transkripsiyon ===
log("\n=== [2] Transkripsiyon işlemi başlıyor ===")
result = subprocess.run(["python", "python_scripts/transcribe_audio.py", wav_path], capture_output=True, text=True)
log("STDOUT:\n" + result.stdout)
log("STDERR:\n" + result.stderr)
if result.returncode != 0:
    log("Transkripsiyon başarısız.")
    sys.exit()
log("Transkripsiyon tamamlandı.")

# === 3. Transkript dosyasını kontrol et ===
log("\n=== [3] Transkript kontrolü yapılıyor ===")
if not os.path.exists(transcript_path):
    log(f"Transkript dosyası bulunamadı: {transcript_path}")
    sys.exit()

try:
    with open(transcript_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            log(f"Transkript dosyası boş: {transcript_path}")
            sys.exit()
        log("Transkript bulundu ve dolu.")
except Exception as e:
    log(f"Transkript okunamadı. Hata: {str(e)}")
    sys.exit()

# === 4. Chunking ===

log("\n=== [4] Chunking işlemi başlıyor ===")
log(f"Chunking'e gönderilen transcript_path: {transcript_path}")

try:
    with open(transcript_path, "r", encoding="utf-8") as f:
        test_read = f.read(200)
        log("Transkript dosyası okunabiliyor.")
        log(f"İlk 200 karakter:\n{test_read}")
except Exception as e:
    log(f"Transkript dosyası okunamadı. Hata: {str(e)}")
    sys.exit()

python_executable = sys.executable
result = subprocess.run(
    [python_executable, "python_scripts/chunk_text.py", transcript_path],
    capture_output=True,
    text=True,
    cwd=os.getcwd()
)
log("STDOUT:\n" + result.stdout)
log("STDERR:\n" + result.stderr)
log(f"Return code: {result.returncode}")
if result.returncode != 0:
    log("Chunking başarısız.")
    sys.exit()
log("Chunking tamamlandı.")

# === 5. Semantic Search ===
log("\n=== [5] Semantic Search başlatılıyor ===")
result = subprocess.run(
    ["python", "python_scripts/semantic_search.py", question, video_id],
    capture_output=True, text=True
)
log("STDOUT:\n" + result.stdout)
log("STDERR:\n" + result.stderr)
if result.returncode != 0:
    log("Semantic Search başarısız.")
    sys.exit()

best_chunk_path = result.stdout.strip()
if not os.path.exists(best_chunk_path):
    log(f"Seçilen chunk bulunamadı: {best_chunk_path}")
    sys.exit()
log(f"En iyi chunk bulundu: {best_chunk_path}")

# === 6. Özetleme ve Çeviri ===
log("\n=== [6] Özetleme başlatılıyor ===")
result = subprocess.run(
    ["python", "python_scripts/summarize_with_nllb_translation.py", best_chunk_path],
    capture_output=True, text=True
)
log("STDOUT:\n" + result.stdout)
log("STDERR:\n" + result.stderr)
if result.returncode != 0:
    log("Özetleme başarısız.")
    sys.exit()
log("Özetleme tamamlandı.")

# === TAMAMLANDI ===
log("\nTüm işlem başarıyla tamamlandı.")
