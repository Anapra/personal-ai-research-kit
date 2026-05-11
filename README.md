# Personal AI Research Kit

**A minimalist, cross-platform automation toolkit** for serious self-learners and indie builders.

Built to "get shit done" across **Termux (Android)** and **WSL2 Ubuntu** with seamless synchronization via Google Cloud Storage.

---

## ✨ Features

- **Persistent Memory** — AgentMemory running as a background service with PM2.
- **Smart Research Pipelines** — LinkedIn and Reddit data collection via Apify.
- **Course Processor** — Automated video transcript download, cleaning, and summarization (Data Engineering Zoomcamp ready).
- **Agent Skills** — Addy Osmani’s engineering workflows integrated.
- **Cross-Platform Sync** — Template-based environment restore between devices.
- **Clean Architecture** — Strict separation between templates and live configs.

---

## 🛠️ Tech Stack

- **LLM Interface**: Gemini CLI + AgentMemory (MCP).
- **Orchestration**: Apify Actors + custom Python scripts.
- **Media**: yt-dlp + ffmpeg.
- **Cloud**: Google Cloud Storage (gcloud).
- **Persistence**: PM2 + templated GEMINI.md.
- **Environments**: Termux + WSL2 Ubuntu + Windows.

---

## 🚀 Quick Start

### 1. Manual Setup
```bash
git clone https://github.com/Anapra/personal-ai-research-kit.git
cd personal-ai-research-kit
./setup/install.sh
```

### 2. Configure Environment
Copy the templates to your home directory or project root and update with your credentials:
```bash
cp templates/.env.example .env
cp templates/GEMINI.md.example GEMINI.md
```

---

## 📁 Repository Structure

- **`apify/`**: Research pipelines for LinkedIn and Reddit.
- **`gemini-cli/`**: Custom prompts and agent workflows.
- **`setup/`**: OS-specific setup guides and master install scripts.
- **`templates/`**: Redacted configuration examples and dotfiles.
- **`video-processing/`**: Automated transcription and cleaning.

---

## 🧠 Integrated Services

- **AgentMemory**: Persistent cross-session context.
- **Gemini CLI**: High-discipline engineering skills (/spec, /plan, /build).
- **GCP**: Cloud-native storage and analysis.

---

## 🤝 Contributing

This toolkit is primarily for personal use, but feel free to fork it, adapt it, or submit pull requests for improvements!

---

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🛡️ Best Practices

- **Never commit secrets** (use `.env` and `templates/`).
- **Version control templates**, not live configs.
- **Large assets** (videos/transcripts) are ignored; use GCS for sync.
