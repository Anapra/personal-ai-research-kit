# Personal AI Research Kit 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Platform: WSL2 / Termux](https://img.shields.io/badge/Platform-WSL2%20%2F%20Termux-orange.svg)](#)

**An elite, minimalist automation toolkit for researchers and builders.** 

Automate learning, lead generation, and intelligence gathering with a unified stack that works seamlessly across **Termux (Android)**, **WSL2 (Ubuntu)**, and **Windows**.

---

## 💡 Motivation

I built this kit because I needed a way to bridge the gap between "consuming information" and "building intelligence." Most tools are either too heavy or locked into a single platform. This kit provides a portable, LLM-augmented environment that follows me from my workstation (WSL2) to my phone (Termux), ensuring that my research and learning never stop.

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

### 2. One-Command Restore (GCS)
If you have already synced your environment to a GCS bucket, restore it instantly:
```bash
gsutil cp gs://YOUR-BUCKET/path/to/backup/.env . && \
gsutil cp gs://YOUR-BUCKET/path/to/backup/GEMINI.md .
```

### 3. Configure Environment
Copy the provided templates and inject your personal credentials:
```bash
cp templates/.env.example .env
cp templates/GEMINI.md.example GEMINI.md
cp templates/.zshrc.example ~/.zshrc_ai_kit  # Source this in your main .zshrc
```

---

## 📸 Screenshots

| Feature | Visual |
| :--- | :--- |
| **AgentMemory Status** | ![PM2 Status](https://via.placeholder.com/400x100?text=PM2+Status+Placeholder) |
| **Gemini CLI + MCP** | ![Gemini CLI](https://via.placeholder.com/400x100?text=Gemini+CLI+MCP+Bridge) |
| **Folder Structure** | ![Structure](https://via.placeholder.com/400x200?text=Folder+Architecture) |

---

## 📁 Repository Structure

- **`apify/`**: Social discovery engines (LinkedIn Profiles, Reddit Monitoring).
- **`docs/`**: Platform-specific setup guides ([Termux](./docs/termux.md), [WSL2](./docs/wsl2.md)).
- **`gemini-cli/`**: Custom prompt engineering and agent persona configurations.
- **`setup/`**: Automated installation and OS-specific bootstrapping scripts.
- **`templates/`**: Robust examples for environment variables and project rules.
- **`video-processing/`**: The core "Course Processor" (Transcribe -> Clean -> Summarize).

---

## 🗺️ Roadmap

- [ ] **v0.2**: Local LLM integration (Ollama) for offline summarization.
- [ ] **v0.3**: Automated lead-scoring dashboard (Cloud Run).
- [ ] **v0.4**: Telegram/Discord bot interface for mobile research triggers.

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
