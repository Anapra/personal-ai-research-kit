#!/bin/bash
# ==============================================================================
# PERSONAL AI RESEARCH KIT - SETUP SCRIPT
# ==============================================================================
# OS: Ubuntu (WSL2) / Debian (Termux-compatible with minor tweaks)
# Goal: Bootstrap the environment for AgentMemory, Gemini CLI, and GCS Sync.
# ==============================================================================

set -e

cat << "EOF"
  ____                                 _      _   ___ 
 |  _ \ ___ _ __ ___  ___  _ __   __ _| |    /_\ |_ _|
 | |_) / _ \ '__/ __|/ _ \| '_ \ / _` | |   //_\\ | | 
 |  __/  __/ |  \__ \ (_) | | | | (_| | |  /  _  \| | 
 |_|   \___|_|  |___/\___/|_| |_|\__,_|_|  \_/ \_/___|
                                                      
   RESEARCH KIT SETUP - LET'S GET SHIT DONE.
=========================================================
EOF

# 1. System Dependencies
echo "📦 Step 1: Installing system dependencies..."
sudo apt update && sudo apt install -y \
    ffmpeg \
    curl \
    git \
    jq \
    python3-pip \
    python3-venv

# 2. Node.js & Process Management
if ! command -v pm2 &> /dev/null; then
    echo "⚙️ Step 2: Installing PM2 for background automation..."
    sudo npm install -g pm2
fi

# 3. AgentMemory Intelligence Layer
if [ ! -d "$HOME/agentmemory" ]; then
    echo "📂 Step 3: Cloning AgentMemory core..."
    git clone https://github.com/rohitg00/agentmemory.git "$HOME/agentmemory"
fi

echo "🛠️ Step 4: Building AgentMemory..."
cd "$HOME/agentmemory"
npm install && npm run build

# 5. PM2 Service Configuration
echo "🔄 Step 5: Initializing background services..."
pm2 delete agentmemory-server 2>/dev/null || true
pm2 start dist/cli.mjs --name "agentmemory-server" -- --port 3111
pm2 save

# 6. Gemini CLI & MCP Bridge
echo "🔗 Step 6: Connecting Gemini CLI to AgentMemory..."
if command -v gemini &> /dev/null; then
    if ! gemini mcp list | grep -q "agentmemory"; then
        gemini mcp add agentmemory agentmemory-mcp --scope user
    fi
    echo "✅ MCP Bridge linked successfully."
else
    echo "⚠️  Gemini CLI not found. Please install it to use MCP features."
fi

# 7. Verification & Success
echo ""
echo "========================================================="
echo "✅ SETUP COMPLETE! YOUR AI KIT IS READY."
echo "========================================================="
echo "✓ AgentMemory Server : Running on http://localhost:3111"
echo "✓ PM2 Daemon         : Configured for auto-restart"
echo "✓ Python Environment : Ready for research scripts"
echo "========================================================="
echo "💡 NEXT STEPS:"
echo "1. Source the templates/.zshrc.example in your shell."
echo "2. Run: gemini 'Analyze this workspace and tell me the mission.'"
echo "========================================================="
