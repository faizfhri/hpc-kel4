#!/bin/sh
# Setup script for Alpine Linux Host
# This script installs all dependencies needed to run the HPC Benchmark Streamlit app

set -e

echo "🚀 Setting up HPC Benchmark Environment on Alpine Linux..."

# Check if running as root - adjust commands accordingly
if [ "$(id -u)" -eq 0 ]; then
    echo "Running as root - will install packages directly"
    SUDO=""
else
    echo "Running as normal user - will use sudo"
    SUDO="sudo"
fi

# Update package index
echo "📦 Updating package index..."
$SUDO apk update

# Install system dependencies
echo "🔧 Installing system dependencies..."
$SUDO apk add --no-cache \
    python3 \
    py3-pip \
    python3-dev \
    docker \
    docker-compose \
    gcc \
    g++ \
    musl-dev \
    linux-headers \
    libffi-dev \
    openssl-dev \
    git \
    bash

# Setup Docker
echo "🐳 Configuring Docker..."
$SUDO rc-update add docker boot 2>/dev/null || true
$SUDO service docker start 2>/dev/null || true

# Add current user to docker group (only if not root)
if [ "$(id -u)" -ne 0 ]; then
    $SUDO addgroup $USER docker 2>/dev/null || true
    echo "⚠️  You may need to log out and log back in for docker group changes to take effect"
fi

# Create Python virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv venv
. venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install Python packages
echo "📦 Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

# Build Docker MPI image
echo "🏗️  Building Docker MPI node image..."
docker build -t mpi-node .

# Create Docker network
echo "🌐 Creating Docker network..."
docker network create mpi-net 2>/dev/null || echo "Network already exists"

# Create shared volume
echo "💾 Creating shared volume..."
docker volume create mpi_home 2>/dev/null || echo "Volume already exists"

# Install ngrok (optional for remote access)
echo ""
echo "🌐 Installing ngrok for remote access..."
if ! command -v ngrok &> /dev/null; then
    if [ "$(uname -m)" = "x86_64" ]; then
        wget -q https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
        $SUDO tar xvzf ngrok-v3-stable-linux-amd64.tgz -C /usr/local/bin
        rm ngrok-v3-stable-linux-amd64.tgz
        echo "✅ ngrok installed successfully"
    elif [ "$(uname -m)" = "aarch64" ]; then
        wget -q https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz
        $SUDO tar xvzf ngrok-v3-stable-linux-arm64.tgz -C /usr/local/bin
        rm ngrok-v3-stable-linux-arm64.tgz
        echo "✅ ngrok installed successfully"
    fi
else
    echo "✅ ngrok already installed"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run Streamlit app: streamlit run app.py"
echo "  3. Access in browser: http://localhost:8501"
echo ""
echo "To access remotely using ngrok:"
echo "  1. Sign up at https://ngrok.com and get your authtoken"
echo "  2. Authenticate: ngrok config add-authtoken YOUR_TOKEN"
echo "  3. Start Streamlit: streamlit run app.py"
echo "  4. In new terminal: ngrok http 8501"
echo "  5. Copy the https URL (e.g., https://xxxx.ngrok.io)"
echo ""
echo "Alternative - run on network (LAN access):"
echo "  streamlit run app.py --server.address=0.0.0.0 --server.port=8501"
