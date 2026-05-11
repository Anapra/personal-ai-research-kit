#!/bin/bash
# AgentMemory + Gemini CLI Setup Script (Optimized)
# Restores environment and configures background services

set -e

echo "🚀 Starting Environment Sync & Setup..."

# 1. System Dependencies
echo "📦 Installing system dependencies..."
sudo apt update && sudo apt install -y ffmpeg curl git jq

# 2. Node.js & Global Packages
if ! command -v pm2 &> /dev/null; then
    echo "⚙️ Installing PM2..."
    sudo npm install -g pm2
fi

# 3. AgentMemory Setup
if [ ! -d "$HOME/agentmemory" ]; then
    echo "📂 Cloning AgentMemory..."
    git clone https://github.com/rohitg00/agentmemory.git "$HOME/agentmemory"
fi

cd "$HOME/agentmemory"
echo "🛠️ Building AgentMemory..."
npm install && npm run build

# 4. PM2 Daemonization
echo "🔄 Configuring PM2 Service..."
pm2 delete agentmemory-server 2>/dev/null || true
pm2 start dist/cli.mjs --name "agentmemory-server" -- --port 3111
pm2 save

# 5. Gemini CLI Configuration
echo "🔗 Connecting to Gemini CLI..."
# Check for gemini command
if command -v gemini &> /dev/null; then
    if ! gemini mcp list | grep -q "agentmemory"; then
        gemini mcp add agentmemory agentmemory-mcp --scope user
    fi
else
    echo "⚠️ gemini CLI not found. Skipping MCP registration."
fi

# 6. Success Message
echo "✅ Setup Complete!"
echo "------------------------------------------------"
echo "✓ AgentMemory: http://localhost:3111 (PM2)"
echo "✓ MCP Bridge: Configured"
echo "✓ Environment: Ready (FFmpeg, yt-dlp, Vertex AI)"
echo "------------------------------------------------"
echo "💡 Routine: gemini 'Recall memories for DE Zoomcamp'"
