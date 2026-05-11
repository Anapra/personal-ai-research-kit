# Termux Setup Guide 📱

The Personal AI Research Kit is designed to be lightweight enough to run on Android via Termux.

## Prerequisites
1. Install [Termux](https://termux.dev/) (preferably from F-Droid).
2. Grant storage permissions: `termux-setup-storage`.

## Installation steps
1. Update packages:
   ```bash
   pkg update && pkg upgrade
   ```
2. Install dependencies:
   ```bash
   pkg install git python nodejs-lts ffmpeg openssh
   ```
3. Clone and Run Setup:
   ```bash
   git clone https://github.com/Anapra/personal-ai-research-kit.git
   cd personal-ai-research-kit
   ./setup/install.sh
   ```

## Note on AgentMemory
Running a background PM2 service on Termux may require disabling battery optimizations for the Termux app to prevent the Android system from killing the process.
