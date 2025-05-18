import sys
import os
import whisper
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("transcribe_audio.py BAŞLADI", file=sys.stderr)

if len(sys.argv) < 2:
    print("Kullanım: python transcribe_audio.py <wav_path>", file=sys.stderr)
    sys.exit(1)

audio_path = sys.argv[1]
video_id = os.path.splitext(os.path.basename(audio_path))[0]
output_path = os.path.join("Transcripts", f"{video_id}.txt")

try:
    model = whisper.load_model("tiny")  # Hızlı model
    result = model.transcribe(audio_path)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result["text"].strip())

    print("transcribe_audio.py BİTTİ", file=sys.stderr)
    print(output_path)
except Exception as e:
    print(f"HATA: {e}", file=sys.stderr)
    sys.exit(1)
