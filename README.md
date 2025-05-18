# 🧠 Smart Summary

**Smart Summary** is a full-stack AI-powered application that takes a user-uploaded video and returns a context-specific **Turkish summary** based on a user-provided question or topic.

---

## 🔧 How It Works (AI Pipeline)

1. 🎞️ User uploads an `.mp4` video via the frontend
2. 🧏 The backend extracts audio using **FFmpeg**
3. 📝 Audio is transcribed using **Whisper**
4. ✂️ Transcript is split into sentence-level **chunks**
5. 🔍 The user's question is encoded and **matched semantically** using **Sentence-BERT**
6. 🧠 Relevant chunks are summarized with **BART** (English)
7. 🌍 Final summary is translated to **Turkish** via **NLLB**

The result is returned to the frontend and displayed.

---

## 📁 Project Structure

```
SmartSummary/
├── frontend/   # React + Tailwind user interface
├── backend/    # ASP.NET Core API + Python AI pipeline
```

---

## 🖥️ Frontend

📁 [`frontend/`](./frontend)

- Built with **React** and **TailwindCSS**
- Allows users to upload `.mp4` videos and type a question/topic
- Sends data to the backend via a `POST` request
- Displays the final summary returned from the API

### 🔧 Setup

```bash
cd frontend
npm install
npm start
```

➡️ Runs at: [http://localhost:3000](http://localhost:3000)

More details in [`frontend/README.md`](./frontend/README.md)

---

## 🧠 Backend

📁 [`backend/`](./backend)

- Built with **ASP.NET Core Web API**
- Integrates with **Python scripts** for AI tasks
- Runs a complete summarization and translation pipeline

### 🔧 Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
dotnet run
```

➡️ API runs at: [http://localhost:5236](http://localhost:5236)

More details in [`backend/README.md`](./backend/README.md)

---

## 🧪 Example API Call

### Endpoint

```http
POST /pipeline/run
```

### Request

```json
{
  "videoName": "example.mp4",
  "question": "economic system"
}
```

### Response

```json
{
  "summary": "This video explains the transformation of economic systems into digital platforms..."
}
```

---

## 💡 Use Cases

- Educational video summarization  
- Media content compression  
- Intelligent transcript analysis  
- Personalized question-based summarization

---

## 👤 Developer

**Erkam Uçan**  
GitHub: [@ErkamUcan](https://github.com/ErkamUcan)

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 📌 Notes

This repository serves as the master project combining both frontend and backend.  
If you're viewing this on GitHub, explore each subfolder for detailed instructions.
