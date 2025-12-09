"""
Documentation Page - Theory and Concepts
"""

import streamlit as st

st.set_page_config(page_title="Documentation", page_icon="📚", layout="wide")

# Add custom CSS
st.markdown("""
    <style>
    .docs-header {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(250, 112, 154, 0.3);
    }
    .concept-card {
        background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='docs-header'>
        <h1 style='color: white; margin: 0;'>Documentation</h1>
        <p style='color: white; margin: 0.5rem 0 0 0; font-size: 1.2rem;'>Understanding HPC Concepts and This Project</p>
    </div>
""", unsafe_allow_html=True)

# Table of Contents
st.markdown("---")
st.markdown("""
## Table of Contents
1. [Project Overview](#project-overview)
2. [High Performance Computing Concepts](#hpc-concepts)
3. [Matrix Multiplication Algorithm](#matrix-algorithm)
4. [Serial vs Parallel Execution](#serial-vs-parallel)
5. [Single Node vs Multi-Node](#single-vs-multi)
6. [Performance Metrics](#performance-metrics)
7. [Setup and Installation](#setup)
8. [Usage Guide](#usage)
""")

st.markdown("---")

# Project Overview
st.header("Project Overview", anchor="project-overview")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### Objective
    This project demonstrates **High Performance Computing (HPC)** concepts through:
    
    - **Performance comparison** between serial and parallel execution
    - **Scalability analysis** across different node configurations
    - **Real-world simulation** using Docker containers as cluster nodes
    - **Interactive visualization** of benchmark results
    
    ### Technologies Used
    - **Docker**: Container orchestration for node simulation
    - **MPI (Message Passing Interface)**: Parallel communication library
    - **C Programming**: High-performance compiled code
    - **Python**: Streamlit web interface and data visualization
    - **Plotly**: Interactive charts and graphs
    """)

with col2:
    st.info("""
    **Key Features:**
    - Multi-node cluster simulation
    - Interactive benchmarking
    - Real-time results visualization
    - Performance analysis
    - Easy deployment
    """)

st.markdown("---")

# HPC Concepts
st.header("High Performance Computing Concepts", anchor="hpc-concepts")

tab1, tab2, tab3 = st.tabs(["What is HPC?", "Why Parallel Computing?", "MPI Basics"])

with tab1:
    st.markdown("""
    ### What is High Performance Computing?
    
    **High Performance Computing (HPC)** refers to the practice of aggregating computing power 
    to deliver much higher performance than a single computer could provide.
    
    #### Applications:
    - **Weather Forecasting**: Simulating atmospheric conditions
    - **Bioinformatics**: Genome sequencing and protein folding
    - **Engineering**: Crash simulations and aerodynamics
    - **AI/ML**: Training large neural networks
    - **Finance**: Risk analysis and trading algorithms
    
    #### Key Characteristics:
    - **Massive Parallelism**: Using thousands of processors simultaneously
    - **High Throughput**: Processing large amounts of data quickly
    - **Low Latency**: Fast communication between compute nodes
    - **Scalability**: Performance improves with added resources
    """)

with tab2:
    st.markdown("""
    ### Why Parallel Computing?
    
    **Moore's Law is slowing down!** Single-core performance improvements have plateaued.
    
    #### Benefits of Parallel Computing:
    
    1. **Speed**: Solve problems faster by dividing work
    2. **Scale**: Handle larger problems that don't fit on one machine
    3. **Efficiency**: Better resource utilization
    4. **Cost**: Use many cheap processors instead of expensive specialized hardware
    
    #### Example: Matrix Multiplication
    
    **Serial (1 core):**
    ```
    Time for 1000×1000: ~18 seconds
    ```
    
    **Parallel (4 cores):**
    ```
    Time for 1000×1000: ~5 seconds
    Speedup: 3.6x
    ```
    
    #### Amdahl's Law
    The theoretical speedup is limited by the serial portion of the code:
    
    **Speedup = 1 / [(1 - P) + P/N]**
    
    Where:
    - P = Parallel portion of code
    - N = Number of processors
    """)

with tab3:
    st.markdown("""
    ### MPI (Message Passing Interface) Basics
    
    **MPI** is a standardized communication protocol for parallel computing.
    
    #### Key Concepts:
    
    **Processes**: Independent programs running simultaneously
    ```c
    int rank;  // Process ID (0, 1, 2, 3, ...)
    int size;  // Total number of processes
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    ```
    
    **Communication Patterns**:
    - **Point-to-Point**: One process sends to another
      - `MPI_Send()` / `MPI_Recv()`
    
    - **Collective**: All processes participate
      - `MPI_Bcast()` - Broadcast data to all
      - `MPI_Scatter()` - Distribute data chunks
      - `MPI_Gather()` - Collect results
      - `MPI_Reduce()` - Aggregate results
    
    #### Example Code:
    ```c
    MPI_Init(&argc, &argv);
    
    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    
    if (rank == 0) {
        printf("I am the master!\\n");
    } else {
        printf("I am worker %d\\n", rank);
    }
    
    MPI_Finalize();
    ```
    """)

st.markdown("---")

# Matrix Multiplication
st.header("Matrix Multiplication Algorithm", anchor="matrix-algorithm")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Sequential Algorithm
    
    **Time Complexity: O(N³)**
    
    ```c
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++) {
            sum = 0.0;
            for (k = 0; k < n; k++) {
                sum += A[i][k] * B[k][j];
            }
            C[i][j] = sum;
        }
    }
    ```
    
    For N=1000: **1 billion operations!**
    """)

with col2:
    st.markdown("""
    ### Parallel Algorithm (Cannon's Algorithm)
    
    **Strategy**: Distribute matrix blocks across processes
    
    1. **Partition**: Divide matrices into blocks
    2. **Distribute**: Send blocks to different processes
    3. **Compute**: Each process computes its block
    4. **Communicate**: Exchange blocks as needed
    5. **Gather**: Collect final result
    
    **Benefit**: N³ operations distributed across P processes
    
    **Theoretical speedup: P times faster!**
    """)

st.markdown("---")

# Serial vs Parallel
st.header("Serial vs Parallel Execution", anchor="serial-vs-parallel")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Serial Execution
    
    **Definition**: Code runs on a single processor, one instruction at a time.
    
    #### Characteristics:
    - Simple to program and debug
    - Deterministic behavior
    - No communication overhead
    - Limited by single-core performance
    - Cannot scale beyond one processor
    
    #### When to Use:
    - Small problems
    - Inherently sequential algorithms
    - Debugging and validation
    """)

with col2:
    st.markdown("""
    ### Parallel Execution
    
    **Definition**: Multiple processors work simultaneously on different parts of the problem.
    
    #### Characteristics:
    - Much faster for large problems
    - Scalable to hundreds/thousands of processors
    - Can solve larger problems
    - More complex programming
    - Communication overhead
    - Potential for race conditions
    
    #### When to Use:
    - Large computational problems
    - Embarrassingly parallel tasks
    - Real-time processing needs
    """)

st.markdown("---")

# Single vs Multi Node
st.header("Single Node vs Multi-Node", anchor="single-vs-multi")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Single Node (Shared Memory)
    
    **All processes run on ONE computer**
    
    #### Architecture:
    ```
    ┌─────────────────────┐
    │    One Computer     │
    │                     │
    │  [CPU - 4 cores]    │
    │  [Shared RAM]       │
    │                     │
    │  P0 P1 P2 P3        │
    └─────────────────────┘
    ```
    
    #### Characteristics:
    - Very fast communication (shared memory)
    - Low latency
    - Simpler setup
    - Limited by one machine's resources
    - RAM and core limits
    
    #### Best For:
    - Medium-sized problems
    - Low communication overhead algorithms
    - Development and testing
    """)

with col2:
    st.markdown("""
    ### Multi-Node (Distributed Memory)
    
    **Processes distributed across MULTIPLE computers**
    
    #### Architecture:
    ```
    ┌──────┐   ┌──────┐
    │ PC 1 │   │ PC 2 │
    │  P0  │◄─►│  P1  │
    └──────┘   └──────┘
        ▲         ▲
        │         │
        ▼         ▼
    ┌──────┐   ┌──────┐
    │ PC 3 │   │ PC 4 │
    │  P2  │◄─►│  P3  │
    └──────┘   └──────┘
    ```
    
    #### Characteristics:
    - Virtually unlimited scalability
    - Large aggregate memory
    - Real HPC architecture
    - Network communication overhead
    - Higher latency
    - More complex setup
    
    #### Best For:
    - Very large problems
    - Production HPC systems
    - Supercomputers
    """)

st.markdown("---")

# Performance Metrics
st.header("Performance Metrics", anchor="performance-metrics")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Key Metrics
    
    #### 1. Speedup (S)
    ```
    S = T_serial / T_parallel
    ```
    - **Ideal**: S = N (linear speedup)
    - **Typical**: S < N (due to overhead)
    - **Super-linear**: S > N (rare, due to cache effects)
    
    **Example**: Serial takes 18s, parallel with 4 cores takes 5s
    ```
    Speedup = 18 / 5 = 3.6x
    ```
    
    #### 2. Efficiency (E)
    ```
    E = Speedup / Number_of_Processors
    ```
    - **Ideal**: E = 1.0 (100%)
    - **Good**: E > 0.7 (70%)
    - **Poor**: E < 0.5 (50%)
    
    **Example**: Speedup of 3.6x with 4 processors
    ```
    Efficiency = 3.6 / 4 = 0.9 (90%)
    ```
    """)

with col2:
    st.markdown("""
    #### 3. Scalability
    How performance changes with:
    - More processors (strong scaling)
    - Larger problems (weak scaling)
    
    **Strong Scaling**: Fixed problem size
    ```
    Ideal: Time halves when processors double
    ```
    
    **Weak Scaling**: Problem size grows with processors
    ```
    Ideal: Time stays constant
    ```
    
    #### 4. GFLOPS
    **Giga FLoating point Operations Per Second**
    ```
    GFLOPS = Operations / (Time × 10⁹)
    ```
    
    For matrix multiplication (N×N):
    ```
    Operations = 2 × N³
    
    Example for N=1000:
    Operations = 2 × 10⁹
    If time = 5s:
    GFLOPS = 2 / 5 = 0.4 GFLOPS
    ```
    """)

st.markdown("---")

# Setup
st.header("Setup and Installation", anchor="setup")

tab1, tab2 = st.tabs(["Alpine Linux", "Debian/Ubuntu"])

with tab1:
    st.markdown("""
    ### Setup on Alpine Linux
    
    #### Prerequisites:
    ```bash
    # Ensure you have:
    - Alpine Linux (host OS)
    - Docker installed
    - Git installed
    - Sufficient RAM (4GB+)
    ```
    
    #### Installation Steps:
    
    **1. Clone Repository:**
    ```bash
    git clone https://github.com/faizfhri/hpc-kel4.git
    cd hpc-kel4
    ```
    
    **2. Run Setup Script:**
    ```bash
    chmod +x setup_alpine.sh
    ./setup_alpine.sh
    ```
    
    **3. Activate Virtual Environment:**
    ```bash
    source venv/bin/activate
    ```
    
    **4. Start Streamlit App:**
    ```bash
    streamlit run app.py
    ```
    
    **5. Access in Browser:**
    ```
    http://localhost:8501
    ```
    
    #### For Network Access:
    ```bash
    streamlit run app.py --server.address=0.0.0.0 --server.port=8501
    ```
    Then access from any device: `http://<server-ip>:8501`
    """)

with tab2:
    st.markdown("""
    ### Setup on Debian/Ubuntu
    
    #### Prerequisites:
    ```bash
    # Ensure you have:
    - Debian/Ubuntu Linux
    - Docker installed
    - Git installed
    - Sufficient RAM (4GB+)
    ```
    
    #### Installation Steps:
    
    **1. Clone Repository:**
    ```bash
    git clone https://github.com/faizfhri/hpc-kel4.git
    cd hpc-kel4
    ```
    
    **2. Run Setup Script:**
    ```bash
    chmod +x setup_debian.sh
    ./setup_debian.sh
    ```
    
    **3. Activate Virtual Environment:**
    ```bash
    source venv/bin/activate
    ```
    
    **4. Start Streamlit App:**
    ```bash
    streamlit run app.py
    ```
    
    **5. Access in Browser:**
    ```
    http://localhost:8501
    ```
    """)

st.markdown("---")

# Usage Guide
st.header("Usage Guide", anchor="usage")

st.markdown("""
### Step-by-Step Tutorial

#### 1️⃣ Check System Status
Navigate to **🏠 Overview** page to:
- Verify Docker is running
- Check cluster node status
- Start/stop cluster as needed

#### 2️⃣ Run Your First Benchmark
Go to **Run Benchmark** page:

1. **Select Algorithm**: Choose "Matrix Multiplication"
2. **Set Matrix Size**: Start with 500 for quick test
3. **Choose Mode**: Try "Compare All" to see all modes
4. **Click Run**: Watch the benchmark execute!

#### 3️⃣ Analyze Results
Visit **Results & Analysis** page to:
- View execution times
- Compare speedup metrics
- Analyze efficiency
- Download results

#### 4️⃣ Experiment
Try different configurations:
- **Small matrices** (100-500): See overhead effects
- **Medium matrices** (1000-2000): Optimal range
- **Large matrices** (3000-5000): Test scalability
- **Different process counts**: 1, 4, 9, 16

#### 5️⃣ Interpret Results
Look for:
- **Speedup > 2x**: Good parallelization
- **Efficiency > 70%**: Efficient use of resources
- **Multi-node vs Single-node**: Communication overhead analysis
""")

st.markdown("---")

# Troubleshooting
with st.expander("Troubleshooting"):
    st.markdown("""
    ### Common Issues and Solutions
    
    #### Docker not available
    **Problem**: "Docker is not available" error
    
    **Solutions**:
    ```bash
    # Check Docker status
    docker ps
    
    # Start Docker (Alpine)
    service docker start
    
    # Start Docker (Debian/Ubuntu)
    sudo systemctl start docker
    
    # Add user to docker group
    sudo usermod -aG docker $USER
    # Log out and back in
    ```
    
    #### Containers not starting
    **Problem**: Nodes show as "not_found"
    
    **Solutions**:
    ```bash
    # Check if image exists
    docker images | grep mpi-node
    
    # Rebuild image
    docker build -t mpi-node .
    
    # Check network
    docker network ls | grep mpi-net
    
    # Recreate network
    docker network create mpi-net
    ```
    
    #### Slow compilation
    **Problem**: Compilation takes too long
    
    **Solutions**:
    - Check container CPU limits
    - Ensure sufficient resources allocated to Docker
    - Restart Docker daemon
    
    #### MPI errors
    **Problem**: "MPI_Init failed" or connection errors
    
    **Solutions**:
    ```bash
    # Exec into head node
    docker exec -it hpchead bash
    
    # Test SSH connectivity
    ssh node01
    ssh node02
    ssh node03
    
    # Regenerate SSH keys if needed
    ssh-keygen -t rsa
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
    ```
    """)

# References
with st.expander("📚 References and Further Reading"):
    st.markdown("""
    ### Recommended Resources
    
    #### Books:
    - "Introduction to Parallel Computing" by Ananth Grama
    - "Parallel Programming with MPI" by Peter Pacheco
    - "High Performance Computing" by Charles Severance
    
    #### Online Resources:
    - [MPI Tutorial](https://mpitutorial.com/)
    - [OpenMPI Documentation](https://www.open-mpi.org/doc/)
    - [Docker Documentation](https://docs.docker.com/)
    - [Streamlit Documentation](https://docs.streamlit.io/)
    
    #### Papers:
    - Cannon's Algorithm for Matrix Multiplication
    - Amdahl's Law and Gustafson's Law
    - Scalability in Parallel Computing
    """)

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>HPC Matrix Operations Benchmark</strong></p>
    <p>Built for High Performance Computing Course</p>
    <p>Team: Kelompok 4 | 2025</p>
</div>
""", unsafe_allow_html=True)
