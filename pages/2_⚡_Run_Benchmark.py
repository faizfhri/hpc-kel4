"""
Run Benchmark Page - Interactive Benchmark Execution
"""

import streamlit as st
import sys
from pathlib import Path
import time

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))

from utils import DockerManager, BenchmarkRunner

st.set_page_config(page_title="Run Benchmark", page_icon="⚡", layout="wide")

# Add custom CSS
st.markdown("""
    <style>
    .run-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    .config-card {
        background: #f7fafc;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='run-header'>
        <h1 style='color: white; margin: 0;'>⚡ Run Benchmark</h1>
        <p style='color: white; margin: 0.5rem 0 0 0; font-size: 1.2rem;'>Interactive Performance Testing</p>
    </div>
""", unsafe_allow_html=True)

# Initialize managers
if 'docker_manager' not in st.session_state:
    st.session_state.docker_manager = DockerManager()

if 'benchmark_runner' not in st.session_state:
    st.session_state.benchmark_runner = BenchmarkRunner(st.session_state.docker_manager)

docker_mgr = st.session_state.docker_manager
bench_runner = st.session_state.benchmark_runner

# Check Docker status
if not docker_mgr.is_docker_available():
    st.error("Docker is not available. Please start Docker and refresh this page.")
    st.stop()

# Check cluster status
cluster_status = docker_mgr.get_cluster_status()
running_nodes = sum(1 for status in cluster_status.values() if status == "running")

if running_nodes == 0:
    st.warning("No cluster nodes are running. Please start the cluster first.")
    if st.button("Start Cluster Now"):
        with st.spinner("Starting cluster..."):
            docker_mgr.start_cluster()
            st.success("Cluster started")
            st.rerun()
    st.stop()

st.success(f"Cluster active: {running_nodes}/4 nodes online")

st.markdown("---")

# Configuration Panel
st.header("⚙️ Benchmark Configuration")

col1, col2 = st.columns([2, 1])

with col1:
    # Algorithm selection
    algorithm = st.selectbox(
        "Algorithm:",
        [
            "Matrix Multiplication",
            "LU Decomposition (Coming Soon)",
            "Cholesky Decomposition (Coming Soon)",
            "Matrix Transpose (Coming Soon)"
        ],
        help="Select matrix operation for benchmarking"
    )
    
    # Matrix size
    matrix_size = st.slider(
        "Matrix Size (N×N):",
        min_value=100,
        max_value=5000,
        value=1000,
        step=100,
        help="Square matrix dimension (larger matrices require more computation)"
    )
    
    st.info(f"Matrix dimensions: {matrix_size:,} × {matrix_size:,} = {matrix_size**2:,} elements")

with col2:
    # Execution mode
    st.markdown("### Execution Mode")
    
    exec_mode = st.radio(
        "Select mode:",
        ["Serial", "Single Node", "Multi Node", "Compare All"],
        help="Serial: 1 process | Single: Multiple processes on 1 node | Multi: Distributed across nodes"
    )
    
    # Additional parameters
    if exec_mode in ["Single Node", "Multi Node", "Compare All"]:
        num_processes = st.select_slider(
            "Number of Processes:",
            options=[1, 2, 4, 8, 16],
            value=4,
            help="Total MPI processes (must be perfect square for matrix multiplication)"
        )
    else:
        num_processes = 1

# Advanced options
with st.expander("Advanced Options"):
    repeat_runs = st.number_input(
        "Repeat Runs (for averaging):",
        min_value=1,
        max_value=10,
        value=1,
        help="Execute benchmark multiple times and average results"
    )
    
    show_output = st.checkbox(
        "Show detailed output",
        value=True,
        help="Display raw command output"
    )
    
    save_results = st.checkbox(
        "Save results to file",
        value=True,
        help="Store results in data/results/ directory"
    )

st.markdown("---")

# Execution Panel
st.header("🚀 Execute Benchmark")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Matrix Size", f"{matrix_size}×{matrix_size}")
with col2:
    st.metric("Mode", exec_mode)
with col3:
    st.metric("Processes", num_processes)

# Run button
if st.button("RUN BENCHMARK", type="primary", use_container_width=True):
    
    # Validate algorithm
    if "Coming Soon" in algorithm:
        st.error("This algorithm is not yet implemented. Please select Matrix Multiplication.")
        st.stop()
    
    # Create results container
    results_container = st.container()
    
    with results_container:
        st.markdown("### Benchmark Execution")
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            if exec_mode == "Serial":
                # Serial execution
                status_text.text("Compiling serial code...")
                progress_bar.progress(20)
                time.sleep(0.5)
                
                status_text.text("Running serial benchmark...")
                progress_bar.progress(40)
                
                result = bench_runner.run_serial_benchmark(matrix_size)
                progress_bar.progress(100)
                
                if result["success"]:
                    status_text.text("Benchmark completed successfully")
                    st.session_state.last_result = result
                else:
                    st.error(f"Benchmark failed: {result.get('error')}")
                    if show_output and 'error' in result:
                        st.code(result['error'])
            
            elif exec_mode == "Single Node":
                # Single node parallel
                status_text.text("🔧 Compiling parallel code...")
                progress_bar.progress(20)
                time.sleep(0.5)
                
                status_text.text(f"🚀 Running on single node with {num_processes} processes...")
                progress_bar.progress(40)
                
                result = bench_runner.run_parallel_benchmark(
                    matrix_size, num_processes, "single_node"
                )
                progress_bar.progress(100)
                
                if result["success"]:
                    status_text.text("✅ Benchmark completed successfully!")
                    st.session_state.last_result = result
                else:
                    st.error(f"❌ Benchmark failed: {result.get('error')}")
                    if show_output and 'error' in result:
                        st.code(result['error'])
            
            elif exec_mode == "Multi Node":
                # Multi node parallel
                status_text.text("🔧 Compiling parallel code...")
                progress_bar.progress(20)
                time.sleep(0.5)
                
                status_text.text(f"🚀 Running across multiple nodes with {num_processes} processes...")
                progress_bar.progress(40)
                
                result = bench_runner.run_parallel_benchmark(
                    matrix_size, num_processes, "multi_node"
                )
                progress_bar.progress(100)
                
                if result["success"]:
                    status_text.text("✅ Benchmark completed successfully!")
                    st.session_state.last_result = result
                else:
                    st.error(f"❌ Benchmark failed: {result.get('error')}")
                    if show_output and 'error' in result:
                        st.code(result['error'])
            
            else:  # Compare All
                status_text.text("🔧 Running comprehensive comparison...")
                progress_bar.progress(10)
                
                result = bench_runner.run_comparison(matrix_size, num_processes)
                progress_bar.progress(100)
                status_text.text("✅ All benchmarks completed!")
                st.session_state.last_result = result
        
        except Exception as e:
            st.error(f"Error during benchmark execution: {e}")
            status_text.text("Benchmark failed")
            import traceback
            st.code(traceback.format_exc())

st.markdown("---")

# Results Display
if 'last_result' in st.session_state:
    st.header("Results")
    
    result = st.session_state.last_result
    
    if "tests" in result:
        # Comparison results
        st.subheader("Comparison Results")
        
        cols = st.columns(3)
        
        for idx, (mode, data) in enumerate(result["tests"].items()):
            with cols[idx % 3]:
                if data.get("success"):
                    st.metric(
                        label=mode.replace('_', ' ').title(),
                        value=f"{data['execution_time']:.3f}s",
                        delta=f"Speedup: {data.get('speedup', 1.0):.2f}x" if 'speedup' in data else None
                    )
        
        # Detailed table
        st.subheader("Detailed Metrics")
        
        import pandas as pd
        rows = []
        for mode, data in result["tests"].items():
            if data.get("success"):
                rows.append({
                    "Mode": mode.replace('_', ' ').title(),
                    "Time (s)": f"{data['execution_time']:.3f}",
                    "Speedup": f"{data.get('speedup', 1.0):.2f}x",
                    "Efficiency": f"{data.get('efficiency', 1.0):.2%}",
                    "Processes": data.get('num_processes', 1)
                })
        
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    else:
        # Single result
        if result.get("success"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Execution Time", f"{result['execution_time']:.3f}s")
            with col2:
                st.metric("Mode", result['mode'].replace('_', ' ').title())
            with col3:
                st.metric("Matrix Size", f"{result['matrix_size']}×{result['matrix_size']}")
    
    # Show raw output
    if show_output and 'raw_output' in result:
        with st.expander("Raw Output"):
            st.code(result['raw_output'])
    
    # Save button
    if save_results:
        if st.button("Save Results", use_container_width=True):
            filepath = bench_runner.save_results(result)
            st.success(f"Results saved to: {filepath}")
    
    # Navigate to results page
    if st.button("View Detailed Analysis", use_container_width=True):
        st.switch_page("pages/3_📈_Results.py")
