# Personal AI Research Kit 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Platform: WSL2 / Termux](https://img.shields.io/badge/Platform-WSL2%20%2F%20Termux-orange.svg)](#)

**An elite, minimalist automation toolkit for researchers and builders.** 

Automate learning, trend discovery, and intelligence gathering with a unified stack that works seamlessly across **Termux (Android)**, **WSL2 (Ubuntu)**, and **Windows**.

---

## 💡 Motivation

I built this kit to bridge the gap between "consuming information" and "building intelligence." It provides a portable, LLM-augmented environment that follows me from my workstation (WSL2) to my phone (Termux), ensuring that research and learning never stop.

---

## 🔄 End-to-End Workflow

This toolkit orchestrates a complete data intelligence pipeline:

1.  **Extraction:** Scrapers (LinkedIn, Reddit) trigger **Apify Actors** to extract trending AI/Tech data.
2.  **Ingestion:** Extracted JSON data is automatically saved to **Local Storage** and mirrored to **Google Cloud Storage (GCS)**.
3.  **Synthesis:** **Gemini CLI** (via Vertex AI) reads the raw data to provide instant summaries, trend analysis, and action items.
4.  **Visualization:** A modular **Flask Research Dashboard** (deployed via Cloud Run) provides a visual interface for reviewing and scoring processed insights stored in **Firestore**.

---

## ✨ Features

- **🧠 Persistent Memory** — AgentMemory background service (via PM2) for cross-session intelligence.
- **🔍 Smart Discovery** — Generic AI research pipelines for monitoring tech trends on LinkedIn and Reddit.
- **📚 Course Processor** — Fully automated video transcript processing (yt-dlp + clean + summarize).
- **🚀 Agent Skills** — Professional-grade engineering workflows (/spec, /plan, /build) ready out-of-the-box.
- **📊 Research Dashboard** — Flask-based UI for reviewing AI-scored insights and trends.
- **⚡ Cloud-Native** — Serverless Cloud Functions for automatic data processing and scoring.

---

## 🛠️ Tech Stack

- **LLM Interface**: Gemini CLI + AgentMemory (MCP Bridge).
- **Orchestration**: Apify Actors + custom Python 3.11 scripts.
- **Media Engine**: `yt-dlp` for extraction + `ffmpeg` for processing.
- **Cloud Infrastructure**: Google Cloud Platform (GCS, Firestore, Cloud Functions, Vertex AI, Cloud Run).
- **Web Framework**: Flask (Research Dashboard).

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
cp templates/.zshrc.example ~/.zshrc_ai_kit
```

---

## 📁 Repository Structure

- **`apify/`**: Social discovery engines (AI Tech Research on LinkedIn and Reddit).
- **`cloud-function/`**: Logic for AI-driven scoring and ingestion into Firestore.
- **`dashboard/`**: Flask-based web interface for insight review.
- **`docs/`**: Platform-specific setup guides ([Termux](./docs/termux.md), [WSL2](./docs/wsl2.md)).
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
