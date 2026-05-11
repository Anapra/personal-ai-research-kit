# Personal AI Research Kit

**A minimalist, cross-platform automation toolkit** for serious self-learners and indie builders.

Built to "get shit done" across **Termux (Android)** and **WSL2 Ubuntu** with seamless synchronization via Google Cloud Storage.

---

## ✨ Features

- **Persistent Memory** — AgentMemory running as a background service with PM2
- **Smart Research Pipelines** — LinkedIn and Reddit data collection via Apify
- **Course Processor** — Automated video transcript download, cleaning, and summarization (Data Engineering Zoomcamp ready)
- **Agent Skills** — Addy Osmani’s engineering workflows integrated
- **Cross-Platform Sync** — One-command environment restore between devices
- **Clean Architecture** — Strict separation between templates and live configs

---

## 🛠️ Tech Stack

- **LLM Interface**: Gemini CLI + AgentMemory (MCP)
- **Orchestration**: Apify Actors + custom Python scripts
- **Media**: yt-dlp + ffmpeg
- **Cloud**: Google Cloud Storage (gcloud)
- **Persistence**: PM2 + templated GEMINI.md
- **Environments**: Termux + WSL2 Ubuntu + Windows

---

## 🚀 Quick Start

### 1. Restore Environment (Recommended)
```bash
gcloud storage cp gs://YOUR-BUCKET/scripts/setup_agentmemory_sync.sh . && \
chmod +x setup_agentmemory_sync.sh && \
./setup_agentmemory_sync.sh
```

### 2. Manual Setup
```bash
git clone https://github.com/Anapra/personal-ai-research-kit.git
cd personal-ai-research-kit
./setup/install.sh
```

---

## 📁 Repository Structure
- **setup/**: OS-specific setup guides and master install scripts.
- **apify/**: Research pipelines for LinkedIn and Reddit.
- **video-processing/**: Automated transcription and cleaning.
- **gemini-cli/**: Custom prompts and agent workflows.
- **templates/**: Redacted configuration examples.

---

## 🧠 Integrated Services
- **AgentMemory**: Persistent cross-session context.
- **Gemini CLI**: High-discipline engineering skills (/spec, /plan, /build).
- **GCP**: Cloud-native storage and analysis.

---

## ⚖️ Best Practices
- Never commit secrets (use .env).
- Version control templates, not live configs.
- Large assets (videos/transcripts) are ignored; use GCS for sync.
