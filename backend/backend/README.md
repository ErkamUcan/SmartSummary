# 🧠 Smart Summary – Backend API

This is the **backend API** of the Smart Summary system — an AI-powered pipeline that processes video input and generates a Turkish summary based on user-defined context.

---

## ⚙️ Technologies Used

- ASP.NET Core Web API  
- Python (integrated via ProcessStartInfo)  
- FFmpeg (audio extraction)  
- OpenAI Whisper (speech-to-text)  
- Sentence-BERT (semantic search)  
- BART (abstractive summarization)  
- NLLB (English-to-Turkish translation)

---

## 🔁 AI Pipeline Workflow

1. 🎞️ Extracts audio from MP4 using FFmpeg  
2. 🧏 Converts audio to text using Whisper  
3. ✂️ Splits transcript into sentence-level chunks  
4. 🔍 Uses Sentence-BERT to find semantically relevant chunks  
5. 🧠 Summarizes using BART (English)  
6. 🌍 Translates summary to Turkish using NLLB  
7. 📦 Returns final output to frontend as JSON

---

## 🚀 How to Run the API

### 1. Prepare Python environment

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start the ASP.NET Core Web API

```bash
cd backend
dotnet run
```

The API runs on:  
[http://localhost:5236](http://localhost:5236)

---

## 📦 API Endpoint

### `POST /pipeline/run`

#### Request Body:

```json
{
  "videoName": "example.mp4",
  "question": "What is the topic?"
}
```

#### Response:

```json
{
  "summary": "This video explains the digital transformation of money..."
}
```

> Note: CORS settings are already configured in `Program.cs`.

---

## 📁 Directory Structure

```
backend/
├── Controllers/
├── Models/
├── python_scripts/
│   ├── extract_audio.py
│   ├── transcribe_audio.py
│   ├── chunk_text.py
│   ├── semantic_search.py
│   └── summarize_with_nllb_translation.py
├── Uploads/          # Uploaded video files
├── Transcripts/      # Whisper-generated transcripts
├── Chunks/           # Sentence-level chunks
├── Summaries/        # Final translated summaries
```

---

## 🧪 Python Script Details

Each Python script handles one stage of the AI pipeline:

- `extract_audio.py` → Converts video to WAV  
- `transcribe_audio.py` → Uses Whisper for transcription  
- `chunk_text.py` → Splits transcript into manageable parts  
- `semantic_search.py` → Finds the most relevant content  
- `summarize_with_nllb_translation.py` → Summarizes and translates

---

## 👤 Developer

**Erkam Uçan**  
GitHub: [@ErkamUcan](https://github.com/ErkamUcan)

---

## 📄 License

This project is licensed under the MIT License.
