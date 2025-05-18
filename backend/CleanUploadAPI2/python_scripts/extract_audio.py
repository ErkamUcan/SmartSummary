import sys
import os
import subprocess
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# === 1. Argüman kontrolü ===
if len(sys.argv) < 2:
    print("Kullanım: python extract_audio.py <video_path>", file=sys.stderr)
    sys.exit(1)

video_path = sys.argv[1]
wav_path = video_path.replace(".mp4", ".wav")

print("extract_audio.py BAŞLADI", file=sys.stderr)

# === 2. FFmpeg komutu ===
command = ["ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "pcm_s16le", wav_path]
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# === 3. Başarısızlık kontrolü ===
if result.returncode != 0:
    print("FFmpeg HATASI:", file=sys.stderr)
    print(result.stderr, file=sys.stderr)
    sys.exit(1)

# === 4. Başarılıysa çıkış ===
print("extract_audio.py BİTTİ", file=sys.stderr)
print(wav_path)  # stdout ile sonucu döndür (C# bunu alacak)
