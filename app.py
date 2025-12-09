"""
HPC Matrix Operations Benchmark - Streamlit Application
Main entry point for the interactive web interface
"""

import streamlit as st
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="HPC Benchmark Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    /* Main container */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Headers with gradient */
    h1 {
        background: linear-gradient(120deg, #1f77b4 0%, #667eea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    h2 {
        color: #1f77b4;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    
    h3 {
        color: #4a5568;
        font-weight: 600;
    }
    
    /* Metrics styling */
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stMetric label {
        color: white !important;
        font-weight: 600;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2rem !important;
        font-weight: 700;
    }
    
    .stMetric [data-testid="stMetricDelta"] {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.5);
    }
    
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    /* Info, Success, Warning, Error boxes */
    .stAlert {
        border-radius: 10px;
        border-left: 5px solid;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
        color: #4a5568;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f7fafc;
        border-radius: 8px;
        font-weight: 600;
        color: #2d3748;
    }
    
    /* Code blocks */
    .stCodeBlock {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
    }
    
    /* Dataframe */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <h1 style='color: white; font-size: 2.5rem; margin: 0;'>🚀</h1>
            <h2 style='color: white; margin: 0.5rem 0;'>HPC Benchmark</h2>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("""
    ### Navigation
    Available sections:
    - System Overview
    - Run Benchmarks
    - Results Analysis
    - Documentation
    """)
    
    st.markdown("---")
    st.markdown("""
    ### About
    **HPC Matrix Operations Benchmark**
    
    Distributed computing platform utilizing:
    - Docker containerization
    - OpenMPI framework
    - Multi-node cluster architecture
    
    Kelompok 4 | High Performance Computing
    """)

# Main page content
st.title("🚀 HPC Matrix Operations Benchmark")
st.markdown("### Interactive Performance Analysis Dashboard")

st.markdown("---")

# Welcome section
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ## Dashboard Overview
    
    This platform provides comprehensive HPC benchmarking capabilities:
    
    **Run benchmarks** on various matrix algorithms  
    **Compare performance** between serial and parallel execution  
    **Visualize results** with interactive charts  
    **Analyze memory** usage and efficiency  
    **Test configurations** across single-node and multi-node setups  
    
    ### Getting Started
    1. Navigate to Run Benchmark to execute tests
    2. Configure matrix size and execution mode
    3. View detailed analysis in Results & Analysis
    
    ### System Requirements
    - Docker runtime environment
    - MPI cluster (4 nodes: hpchead, node01-03)
    - Minimum 4GB RAM
    """)

with col2:
    st.info("**Recommendation**: Begin with matrix sizes 100-500 for initial system validation.")
    
    st.success("**Documentation**: Comprehensive HPC concepts and implementation details available in the Documentation section.")
    
    st.warning("**Prerequisite**: Ensure all Docker containers are active before benchmark execution.")

st.markdown("---")

# System status section
st.subheader("🖥️ System Status")

col1, col2, col3, col4 = st.columns(4)

# We'll populate these dynamically later with actual Docker status
with col1:
    st.metric(
        label="Cluster Nodes",
        value="4",
        delta="All nodes",
        help="Total number of MPI nodes in cluster"
    )

with col2:
    st.metric(
        label="Available Cores",
        value="16",
        delta="4 per node",
        help="Total CPU cores available for parallel processing"
    )

with col3:
    st.metric(
        label="Status",
        value="Ready",
        delta="Online",
        help="Current cluster status"
    )

with col4:
    st.metric(
        label="Algorithms",
        value="4+",
        delta="Matrix ops",
        help="Number of available benchmark algorithms"
    )

st.markdown("---")

# Quick links
st.subheader("🔗 Quick Access")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Run Benchmark", use_container_width=True):
        st.switch_page("pages/2_⚡_Run_Benchmark.py")

with col2:
    if st.button("View Results", use_container_width=True):
        st.switch_page("pages/3_📈_Results.py")

with col3:
    if st.button("Documentation", use_container_width=True):
        st.switch_page("pages/6_📚_Documentation.py")

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>HPC Matrix Operations Benchmark | Course Project 2025</p>
    <p>Powered by Docker and OpenMPI</p>
</div>
""", unsafe_allow_html=True)
