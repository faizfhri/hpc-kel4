# 🚀 HPC Matrix Operations Benchmark

**Interactive High Performance Computing Benchmark with Streamlit Dashboard**

A comprehensive HPC project demonstrating distributed computing concepts through matrix operations, featuring a modern web interface for real-time performance analysis.

![HPC](https://img.shields.io/badge/HPC-High%20Performance%20Computing-blue)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![MPI](https://img.shields.io/badge/MPI-Parallel%20Computing-green)
![Python](https://img.shields.io/badge/Python-3.8+-yellow?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
  - [Alpine Linux](#alpine-linux-recommended)
  - [Debian/Ubuntu](#debianubuntu)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Performance Metrics](#-performance-metrics)
- [Technologies](#-technologies)
- [Contributing](#-contributing)
- [Team](#-team)

---

## 🎯 Overview

This project simulates a **multi-node HPC cluster** using Docker containers to benchmark matrix operations. It compares performance between:

- ⚡ **Serial Execution**: Single-threaded baseline
- 🖥️ **Single-Node Parallel**: Multi-core on one machine
- 🌐 **Multi-Node Distributed**: Cluster computing across multiple nodes

### Key Objectives

1. **Performance Analysis**: Measure speedup and efficiency of parallel algorithms
2. **Scalability Testing**: Evaluate performance across different configurations
3. **Interactive Visualization**: Real-time results through web dashboard
4. **Educational Tool**: Demonstrate HPC concepts in an accessible way

---

## ✨ Features

### 🎨 Interactive Streamlit Dashboard
- **Live Benchmarking**: Run tests directly from the browser
- **Real-time Visualization**: Interactive charts with Plotly
- **Custom Configurations**: Adjustable matrix sizes and process counts
- **Results Management**: Save, load, and compare benchmark results

### 🔬 Comprehensive Analysis
- **Speedup Metrics**: Serial vs parallel performance comparison
- **Efficiency Calculations**: Parallel efficiency and scalability analysis
- **Memory Profiling**: Track memory usage across nodes
- **Multiple Algorithms**: Matrix multiplication, LU decomposition, and more

### 🐳 Docker-Based Architecture
- **Portability**: Run anywhere with Docker
- **Reproducibility**: Consistent environment across platforms
- **Easy Scaling**: Add or remove nodes effortlessly
- **Isolated Environment**: No conflicts with host system

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│           Alpine Linux Host                     │
│                                                  │
│   ┌──────────────────────────────────────────┐ │
│   │  Streamlit App (Port 8501)               │ │
│   │  - Interactive UI                        │ │
│   │  - Docker Management                     │ │
│   │  - Benchmark Orchestration               │ │
│   └───────────────┬──────────────────────────┘ │
│                   │                              │
│                   ▼                              │
│   ┌──────────────────────────────────────────┐ │
│   │    Docker Network: mpi-net               │ │
│   │                                           │ │
│   │  ┌──────────┐      ┌──────────┐         │ │
│   │  │ hpchead  │◄────►│  node01  │         │ │
│   │  │ (Master) │      │ (Worker) │         │ │
│   │  └────┬─────┘      └──────────┘         │ │
│   │       │                                   │ │
│   │       ├────────────►┌──────────┐         │ │
│   │       │             │  node02  │         │ │
│   │       │             │ (Worker) │         │ │
│   │       │             └──────────┘         │ │
│   │       │                                   │ │
│   │       └────────────►┌──────────┐         │ │
│   │                     │  node03  │         │ │
│   │                     │ (Worker) │         │ │
│   │                     └──────────┘         │ │
│   │                                           │ │
│   │      Shared Volume: mpi_home             │ │
│   └──────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

---

## 📦 Prerequisites

### System Requirements
- **OS**: Alpine Linux (recommended) or Debian/Ubuntu
- **RAM**: 4GB minimum, 8GB recommended
- **CPU**: Multi-core processor (4+ cores recommended)
- **Storage**: 10GB free space

### Software Dependencies
- Docker (latest version)
- Docker Compose (optional, for easier management)
- Git
- Python 3.8+

---

## 🚀 Installation

### Alpine Linux (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/faizfhri/hpc-kel4.git
cd hpc-kel4

# 2. Run the automated setup script
chmod +x setup_alpine.sh
./setup_alpine.sh

# 3. Activate virtual environment
source venv/bin/activate

# 4. Start the application
streamlit run app.py
```

### Debian/Ubuntu

```bash
# 1. Clone the repository
git clone https://github.com/faizfhri/hpc-kel4.git
cd hpc-kel4

# 2. Run the automated setup script
chmod +x setup_debian.sh
./setup_debian.sh

# 3. Activate virtual environment
source venv/bin/activate

# 4. Start the application
streamlit run app.py
```

### Using Docker Compose (Alternative)

```bash
# Build and start all containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop cluster
docker-compose down
```

---

## 🎮 Quick Start

### 1. Access the Dashboard

Open your browser and navigate to:
```
http://localhost:8501
```

For network access from other devices:
```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```
Then access via: `http://<your-server-ip>:8501`

### 2. Start the Cluster

Navigate to **🏠 Overview** page and click **"🚀 Start Cluster"**

### 3. Run Your First Benchmark

1. Go to **⚡ Run Benchmark** page
2. Select **Matrix Multiplication** algorithm
3. Set matrix size to **500** (for quick test)
4. Choose **"Compare All"** mode
5. Click **"▶️ RUN BENCHMARK"**

### 4. Analyze Results

Visit **📈 Results & Analysis** to view:
- Interactive charts
- Performance metrics
- Speedup calculations
- Efficiency analysis

---

## 📖 Usage

### Running Benchmarks

#### Serial Execution
```python
# From Streamlit UI:
1. Select "Matrix Multiplication"
2. Choose "Serial" mode
3. Set matrix size (e.g., 1000)
4. Click "Run Benchmark"
```

#### Parallel Execution
```python
# Single-Node (4 processes on one machine)
Mode: Single Node
Processes: 4
Matrix Size: 1000

# Multi-Node (distributed across cluster)
Mode: Multi Node
Processes: 4
Matrix Size: 1000
```

#### Comparison Mode
```python
# Automatically runs all three modes:
- Serial
- Single Node (4 processes)
- Multi Node (4 processes)

# Provides direct comparison and speedup metrics
```

### Manual CLI Usage (Advanced)

```bash
# Enter head node
docker exec -it hpchead bash

# Compile serial version
gcc -o serial serial.c

# Run serial benchmark
./serial 1000

# Compile parallel version
mpicc -o matrix matrix.c -lm

# Run parallel (single node)
mpirun -np 4 --host hpchead ./matrix 1000

# Run parallel (multi node)
mpirun -np 4 --host hpchead,node01,node02,node03 ./matrix 1000
```

---

## 📁 Project Structure

```
hpc-kel4/
├── app.py                      # Main Streamlit application
├── pages/                      # Streamlit pages
│   ├── 1_🏠_Overview.py       # System status and control
│   ├── 2_⚡_Run_Benchmark.py  # Interactive benchmarking
│   ├── 3_📈_Results.py        # Results visualization
│   └── 6_📚_Documentation.py  # Comprehensive docs
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── docker_manager.py      # Docker container management
│   ├── benchmark_runner.py    # Benchmark execution
│   └── visualizer.py          # Chart generation
├── data/                       # Data storage
│   └── results/               # Benchmark results (JSON)
├── matrix.c                    # Parallel matrix multiplication (MPI)
├── serial.c                    # Serial matrix multiplication
├── benchmark.sh               # Legacy CLI benchmark script
├── Dockerfile                  # MPI node container image
├── docker-compose.yml         # Cluster orchestration
├── requirements.txt           # Python dependencies
├── setup_alpine.sh            # Alpine Linux setup
├── setup_debian.sh            # Debian/Ubuntu setup
└── README.md                  # This file
```

---

## 📊 Performance Metrics

### Speedup
```
Speedup = T_serial / T_parallel
```
**Ideal**: Linear speedup (S = N processors)

### Efficiency
```
Efficiency = Speedup / Number_of_Processors
```
**Good**: E > 0.70 (70%)

### GFLOPS
```
GFLOPS = Operations / (Time × 10⁹)

For N×N matrix multiplication:
Operations = 2 × N³
```

### Example Results

| Matrix Size | Serial Time | Multi-Node Time | Speedup | Efficiency |
|-------------|-------------|-----------------|---------|------------|
| 500×500     | 2.3s        | 0.8s            | 2.87x   | 71.8%      |
| 1000×1000   | 18.5s       | 5.2s            | 3.56x   | 89.0%      |
| 2000×2000   | 148.2s      | 41.3s           | 3.59x   | 89.8%      |

---

## 🛠️ Technologies

### Backend
- **C/C++**: High-performance computation
- **OpenMPI**: Message Passing Interface for parallel processing
- **GCC**: GNU Compiler Collection

### Infrastructure
- **Docker**: Containerization platform
- **Docker Compose**: Multi-container orchestration
- **Alpine Linux**: Lightweight container OS
- **Debian**: Stable MPI node OS

### Frontend & Visualization
- **Python 3.8+**: Application logic
- **Streamlit**: Interactive web framework
- **Plotly**: Interactive charting library
- **Pandas**: Data manipulation

### DevOps
- **Git**: Version control
- **Bash**: Automation scripts

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/hpc-kel4.git

# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes and commit
git commit -m "Add your feature"

# Push and create pull request
git push origin feature/your-feature-name
```

---

## 👥 Team

**Kelompok 4** - High Performance Computing Course 2025

- Project Lead & Backend Development
- Frontend & UI/UX Design
- DevOps & Infrastructure
- Documentation & Testing

---

## 📄 License

This project is created for educational purposes as part of the High Performance Computing course.

---

## 🙏 Acknowledgments

- Course Instructor: [Instructor Name]
- OpenMPI Community
- Streamlit Team
- Docker Community

---

## 📞 Contact

For questions or feedback, please open an issue on GitHub.

---

<div align="center">

**Built with ❤️ for High Performance Computing Education**

⭐ Star this repo if you find it helpful!

</div>