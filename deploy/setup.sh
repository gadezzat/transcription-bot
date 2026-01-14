#!/bin/bash
# Transcription Bot - Setup Script for Oracle Cloud

echo "🚀 Starting Transcription Bot Setup..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
echo "🐍 Installing Python 3.11 and dependencies..."
sudo apt install -y python3.11 python3.11-venv python3-pip git ffmpeg

# Create project directory
echo "📁 Setting up project directory..."
cd /home/ubuntu
rm -rf transcription-bot
git clone https://github.com/gadezzat/transcription-bot.git
cd transcription-bot

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "📦 Installing Python dependencies (this may take a while)..."
pip install -r requirements.txt

# Create .env file template
echo "⚙️ Creating .env template..."
cat > .env << 'EOF'
BOT_TOKEN=your_bot_token_here
BOT_USERNAME=your_bot_username
ADMIN_IDS=your_admin_id
BANK_ACCOUNT_NAME=Your Name
BANK_ACCOUNT_NUMBER=1234567890123456
BANK_IBAN=EG380002000112345678901234567890
WHATSAPP_NUMBER=+201234567890
EXCHANGE_RATE=31.2
LOG_LEVEL=INFO
EOF

# Create temp directories
mkdir -p temp_files

echo ""
echo "✅ Setup complete!"
echo ""
echo "⚠️  IMPORTANT: Edit .env file with your bot credentials!"
echo "Run: nano .env"
echo ""
echo "📋 After editing .env, run these commands:"
echo "1. sudo cp deploy/transcription-bot.service /etc/systemd/system/"
echo "2. sudo systemctl daemon-reload"
echo "3. sudo systemctl enable transcription-bot"
echo "4. sudo systemctl start transcription-bot"
echo "5. sudo systemctl status transcription-bot"
