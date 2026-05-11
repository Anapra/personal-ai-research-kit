# Personal AI Research Kit 🚀

**An elite, minimalist automation toolkit for researchers and builders.** 

Automate learning, lead generation, and intelligence gathering with a unified stack that works seamlessly across **Termux (Android)**, **WSL2 (Ubuntu)**, and **Windows**.

---

## ✨ Features

- **🧠 Persistent Memory** — AgentMemory background service (via PM2) for cross-session intelligence.
- **🔍 Smart Discovery** — High-speed LinkedIn and Reddit research pipelines using Apify.
- **📚 Course Processor** — Fully automated video transcript processing (yt-dlp + clean + summarize).
- **🚀 Agent Skills** — Professional-grade engineering workflows (/spec, /plan, /build) ready out-of-the-box.
- **🔄 Cross-Platform Sync** — Reliable environment and data synchronization via Google Cloud Storage.
- **🏗️ Clean Architecture** — Strict "Template vs. Live" separation to protect your secrets.

---

## 🛠️ Tech Stack

- **LLM Interface**: Gemini CLI + AgentMemory (MCP Bridge).
- **Orchestration**: Apify Actors + custom Python 3.11 scripts.
- **Media Engine**: `yt-dlp` for extraction + `ffmpeg` for processing.
- **Cloud Infrastructure**: Google Cloud Platform (GCS, BigQuery, Vertex AI).
- **Process Management**: PM2 for background automation.

---

## 🚀 Quick Start

### 1. Manual Setup
```bash
git clone https://github.com/Anapra/personal-ai-research-kit.git
cd personal-ai-research-kit
chmod +x setup/install.sh
./setup/install.sh
```

### 2. Configure Environment
Copy the provided templates and inject your personal credentials:
```bash
cp templates/.env.example .env
cp templates/GEMINI.md.example GEMINI.md
cp templates/.zshrc.example ~/.zshrc_ai_kit  # Source this in your main .zshrc
```

---

## 📁 Repository Structure

- **`apify/`**: Social discovery engines (LinkedIn Profiles, Reddit Monitoring).
- **`gemini-cli/`**: Custom prompt engineering and agent persona configurations.
- **`setup/`**: Automated installation and OS-specific bootstrapping scripts.
- **`templates/`**: Robust examples for environment variables and project rules.
- **`video-processing/`**: The core "Course Processor" (Transcribe -> Clean -> Summarize).

---

## 🤝 Contributing

This toolkit is designed for personal high-productivity workflows, but I welcome forks and PRs that enhance the core automation logic!

---

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🛡️ Best Practices

- **Security First**: Never commit `.env` files. Use the `templates/` folder for sharing structure.
- **Surgical Sync**: Use `gcloud storage rsync` for data folders; keep the core repo lean.
- **Consistent Style**: Follow the Addy Osmani skills for all development tasks.
