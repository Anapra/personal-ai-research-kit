# WSL2 Setup Guide 💻

WSL2 (Windows Subsystem for Linux) is the primary development environment for this kit.

## Prerequisites
1. Windows 10/11 with WSL2 enabled.
2. Ubuntu 22.04 or 24.04 LTS installed.
3. [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and authenticated.

## Installation steps
1. Ensure your system is up to date:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
2. Clone and Run Setup:
   ```bash
   git clone https://github.com/Anapra/personal-ai-research-kit.git
   cd personal-ai-research-kit
   chmod +x setup/install.sh
   ./setup/install.sh
   ```

## Local Networking
AgentMemory runs on `localhost:3111`. You can access this directly from Windows browsers or applications.
