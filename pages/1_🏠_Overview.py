"""
Overview Page - System Architecture and Status
"""

import streamlit as st
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))

from utils import DockerManager

st.set_page_config(page_title="Overview", page_icon="🏠", layout="wide")

# Add custom CSS
st.markdown("""
    <style>
    .overview-header {
        background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 114, 255, 0.3);
    }
    .node-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    .node-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='overview-header'>
        <h1 style='color: white; margin: 0;'>🏠 System Overview</h1>
        <p style='color: white; margin: 0.5rem 0 0 0; font-size: 1.1rem;'>Multi-Node HPC Cluster Dashboard</p>
    </div>
""", unsafe_allow_html=True)

# Initialize Docker manager
if 'docker_manager' not in st.session_state:
    st.session_state.docker_manager = DockerManager()

docker_mgr = st.session_state.docker_manager

# Check Docker availability
if not docker_mgr.is_docker_available():
    st.error("🚨 Docker is not available! Please start Docker and refresh this page.")
    st.stop()

st.success("✅ Docker is running")

st.markdown("---")

# Architecture Overview
st.header("🏗️ Architecture Overview")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### Multi-Node MPI Cluster Architecture
    
    Distributed computing infrastructure consisting of:
    
    - **Head Node** (hpchead): Master coordination node
    - **Worker Nodes** (node01-03): Parallel computation nodes
    - **Shared Volume**: Unified filesystem access
    - **Docker Network**: Inter-node communication layer
    
    #### Technology Stack:
    - Docker: Container orchestration
    - OpenMPI: Parallel processing framework
    - C/GCC: Optimized computation
    - SSH: Secure node communication
    """)

with col2:
    st.info("""
    **Cluster Configuration**
    
    Total Nodes: 4  
    Cores per Node: 4  
    Shared Storage: Volume  
    Network: Bridge  
    Authentication: SSH Key-based  
    """)

st.markdown("---")

# Cluster Status
st.header("🖥️ Cluster Status")

# Get cluster status
cluster_status = docker_mgr.get_cluster_status()

# Summary metrics
running_nodes = sum(1 for status in cluster_status.values() if status == "running")
total_nodes = len(cluster_status)

col_metric1, col_metric2, col_metric3 = st.columns(3)
with col_metric1:
    st.metric("Active Nodes", f"{running_nodes}/{total_nodes}")
with col_metric2:
    health = "Healthy" if running_nodes == total_nodes else "Degraded" if running_nodes > 0 else "Offline"
    st.metric("Cluster Health", health)
with col_metric3:
    st.metric("Total Capacity", f"{total_nodes * 4} cores")

st.markdown("")

# Create columns for each node
cols = st.columns(4)

nodes_info = [
    ("hpchead", "Head Node", "🖥️"),
    ("node01", "Worker 1", "⚙️"),
    ("node02", "Worker 2", "⚙️"),
    ("node03", "Worker 3", "⚙️")
]

for col, (node_name, node_label, icon) in zip(cols, nodes_info):
    with col:
        status = cluster_status.get(node_name, "unknown")
        
        # Node card with real status
        if status == "running":
            st.success(f"{icon} **{node_label}**")
            st.markdown("**Status:** Running ✓")
            
            # Get real container info
            try:
                container = docker_mgr.client.containers.get(node_name)
                attrs = container.attrs
                
                # Calculate uptime
                started_at = attrs['State']['StartedAt']
                st.caption(f"ID: {container.short_id}")
                st.caption(f"Started: {started_at[:19].replace('T', ' ')}")
                
            except Exception as e:
                st.caption("Info unavailable")
                
        elif status == "exited":
            st.warning(f"{icon} **{node_label}**")
            st.markdown("**Status:** Stopped")
            st.caption("Start cluster to activate")
            
        elif status == "not_found":
            st.error(f"{icon} **{node_label}**")
            st.markdown("**Status:** Not Created")
            st.caption("Container needs to be created")
            
        elif status == "docker_unavailable":
            st.error(f"{icon} **{node_label}**")
            st.markdown("**Status:** Docker Offline")
            st.caption("Start Docker service")
            
        else:
            st.info(f"{icon} **{node_label}**")
            st.markdown(f"**Status:** {status.title()}")
            st.caption(f"Unexpected state: {status}")

st.markdown("---")

# Control Panel
st.header("🎛️ Cluster Control Panel")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Start Cluster", use_container_width=True):
        with st.spinner("Starting cluster nodes..."):
            results = docker_mgr.start_cluster()
            
            success_count = sum(1 for v in results.values() if v)
            if success_count == 4:
                st.success(f"All nodes started successfully")
            else:
                st.warning(f"Started {success_count}/4 nodes")
            
            st.rerun()

with col2:
    if st.button("Stop Cluster", use_container_width=True):
        with st.spinner("Stopping cluster nodes..."):
            results = docker_mgr.stop_cluster()
            st.success("Cluster stopped")
            st.rerun()

with col3:
    if st.button("Refresh Status", use_container_width=True):
        st.rerun()

st.markdown("---")

# System Information
st.header("📊 System Information")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Container Configuration")
    st.code("""
Image: mpi-node
Base OS: Debian/Ubuntu
Network: mpi-net (bridge)
Volume: mpi_home
User: faiz
    """)

with col2:
    st.subheader("MPI Configuration")
    st.code("""
MPI Implementation: OpenMPI
Version: 4.x
SSH: Passwordless (key-based)
Hostfile: Dynamic generation
    """)

st.markdown("---")

# Network Diagram (Simplified)
st.header("🌐 Network Topology")

st.markdown("""
```
┌─────────────────────────────────────────────────┐
│           Docker Host (Alpine Linux)            │
│                                                  │
│   ┌──────────────────────────────────────────┐ │
│   │    Docker Network: mpi-net (bridge)      │ │
│   │                                           │ │
│   │  ┌──────────┐      ┌──────────┐         │ │
│   │  │ hpchead  │◄────►│  node01  │         │ │
│   │  │(Master)  │      │ (Worker) │         │ │
│   │  └────┬─────┘      └──────────┘         │ │
│   │       │                                   │ │
│   │       │            ┌──────────┐          │ │
│   │       └───────────►│  node02  │          │ │
│   │                    │ (Worker) │          │ │
│   │       │            └──────────┘          │ │
│   │       │                                   │ │
│   │       │            ┌──────────┐          │ │
│   │       └───────────►│  node03  │          │ │
│   │                    │ (Worker) │          │ │
│   │                    └──────────┘          │ │
│   │                                           │ │
│   │      Shared Volume: mpi_home             │ │
│   └──────────────────────────────────────────┘ │
│                                                  │
│   Streamlit App (Port 8501) ◄─── User Browser  │
└─────────────────────────────────────────────────┘
```
""")

st.markdown("---")

# Quick Links
st.header("🔗 Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Run Benchmark", use_container_width=True, type="primary"):
        st.switch_page("pages/2_⚡_Run_Benchmark.py")

with col2:
    if st.button("View Results", use_container_width=True):
        st.switch_page("pages/3_📈_Results.py")

with col3:
    if st.button("Documentation", use_container_width=True):
        st.switch_page("pages/6_📚_Documentation.py")
