#!/bin/sh
# Setup script for Alpine Linux Host
# This script installs all dependencies needed to run the HPC Benchmark Streamlit app

set -e

echo "🚀 Setting up HPC Benchmark Environment on Alpine Linux..."

# Check if running as root
if [ "$(id -u)" -eq 0 ]; then
    echo "⚠️  Please run this script as a normal user, not root"
    exit 1
fi

# Update package index
echo "📦 Updating package index..."
sudo apk update

# Install system dependencies
echo "🔧 Installing system dependencies..."
sudo apk add --no-cache \
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
sudo rc-update add docker boot
sudo service docker start

# Add current user to docker group
sudo addgroup $USER docker 2>/dev/null || true
echo "⚠️  You may need to log out and log back in for docker group changes to take effect"

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

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run Streamlit app: streamlit run app.py"
echo "  3. Access in browser: http://localhost:8501"
echo ""
echo "To run on network (accessible from other machines):"
echo "  streamlit run app.py --server.address=0.0.0.0 --server.port=8501"
