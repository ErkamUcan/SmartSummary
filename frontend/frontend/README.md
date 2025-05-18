# 🖥️ Smart Summary – Frontend

This is the **frontend interface** of the Smart Summary system — a full-stack AI-based video summarization tool.  
It allows users to upload video files and request context-specific summaries through a clean and responsive interface.

---

## ⚙️ Technologies Used

- React (via Create React App)  
- TailwindCSS (for minimal, responsive design)  
- Fetch API (to communicate with backend)  
- Modular components (`UploadBox`, `InputField`, etc.)

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
npm install
```

### 2. Start the development server

```bash
npm start
```

The app will run on: [http://localhost:3000](http://localhost:3000)

---

## 🔁 Communication with Backend

This interface sends a `POST` request to the backend API at:

```
http://localhost:5236/pipeline/run
```

With the following JSON body:

```json
{
  "videoName": "yourfile.mp4",
  "question": "your topic or question"
}
```

The backend returns a context-specific **Turkish summary** in response.

---

## 📁 Project Structure

```
src/
├── components/       # UI components (e.g., UploadBox)
├── assets/           # Static files (logo, icons)
├── App.jsx           # Main component
├── index.js          # App entry point
tailwind.config.js    # Tailwind configuration
postcss.config.js     # PostCSS plugins
```

---

## 🧠 Backend Info

This frontend is designed to work with the **Smart Summary Backend**, which includes:

- ASP.NET Core Web API  
- Python AI processing pipeline  
- FFmpeg, Whisper  
- Sentence-BERT, BART, NLLB models

---

## 👤 Developer

**Erkam Uçan**  
GitHub: [@ErkamUcan](https://github.com/ErkamUcan)

---

## 📄 License

This project is licensed under the MIT License.
