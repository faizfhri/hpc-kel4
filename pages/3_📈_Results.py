"""
Results and Analysis Page - Visualization and Data Analysis
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))

from utils import (
    BenchmarkRunner, 
    DockerManager,
    parse_benchmark_results,
    create_speedup_chart,
    create_execution_time_chart,
    create_efficiency_chart,
    calculate_metrics_summary
)

st.set_page_config(page_title="Results & Analysis", page_icon="📈", layout="wide")

# Add custom CSS
st.markdown("""
    <style>
    .results-header {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
    }
    .insight-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='results-header'>
        <h1 style='color: white; margin: 0;'>📈 Results & Analysis</h1>
        <p style='color: white; margin: 0.5rem 0 0 0; font-size: 1.2rem;'>Performance Visualization and Metrics</p>
    </div>
""", unsafe_allow_html=True)

# Initialize managers
if 'docker_manager' not in st.session_state:
    st.session_state.docker_manager = DockerManager()

if 'benchmark_runner' not in st.session_state:
    st.session_state.benchmark_runner = BenchmarkRunner(st.session_state.docker_manager)

bench_runner = st.session_state.benchmark_runner

st.markdown("---")

# Check for recent results
if 'last_result' in st.session_state:
    st.success("Displaying results from latest benchmark run")
    current_result = st.session_state.last_result
    has_data = True
else:
    # Try to load saved results
    saved_results = bench_runner.list_results()
    
    if saved_results:
        st.info(f"Found {len(saved_results)} saved result file(s)")
        selected_file = st.selectbox("Select a result file to load:", saved_results)
        
        if st.button("Load Selected Results"):
            current_result = bench_runner.load_results(selected_file)
            st.session_state.last_result = current_result
            has_data = True
            st.rerun()
        else:
            has_data = False
    else:
        st.warning("No benchmark results available. Please run a benchmark first.")
        if st.button("Go to Run Benchmark"):
            st.switch_page("pages/2_⚡_Run_Benchmark.py")
        has_data = False

if not has_data or 'last_result' not in st.session_state:
    st.stop()

# Parse results
result = st.session_state.last_result

st.markdown("---")

# Display results based on type
if "tests" in result:
    # Comparison results
    st.header("Comprehensive Comparison Analysis")
    
    # Summary metrics
    st.subheader("Summary Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate best speedup
    best_speedup = 1.0
    best_mode = "serial"
    for mode, data in result["tests"].items():
        if data.get("success") and data.get("speedup", 1.0) > best_speedup:
            best_speedup = data["speedup"]
            best_mode = mode
    
    with col1:
        st.metric(
            "Matrix Size",
            f"{result['matrix_size']}×{result['matrix_size']}",
            help="Size of the test matrix"
        )
    
    with col2:
        st.metric(
            "Best Speedup",
            f"{best_speedup:.2f}x",
            delta=best_mode.replace('_', ' ').title(),
            help="Maximum speedup achieved"
        )
    
    with col3:
        # Calculate average efficiency
        efficiencies = [data.get('efficiency', 0) for data in result["tests"].values() 
                       if data.get("success") and 'efficiency' in data]
        avg_eff = sum(efficiencies) / len(efficiencies) if efficiencies else 0
        st.metric(
            "Avg Efficiency",
            f"{avg_eff:.1%}",
            help="Average parallel efficiency"
        )
    
    with col4:
        st.metric(
            "Processes Used",
            result.get('num_processes', 4),
            help="Number of MPI processes"
        )
    
    st.markdown("---")
    
    # Detailed comparison table
    st.subheader("Detailed Results")
    
    rows = []
    for mode, data in result["tests"].items():
        if data.get("success"):
            rows.append({
                "Execution Mode": mode.replace('_', ' ').title(),
                "Time (seconds)": f"{data['execution_time']:.4f}",
                "Speedup": f"{data.get('speedup', 1.0):.2f}x",
                "Efficiency": f"{data.get('efficiency', 1.0):.2%}",
                "Processes": data.get('num_processes', 1),
                "GFLOPS": f"{data.get('gflops', 0):.2f}",
                "Memory (MB)": f"{data.get('memory_mb', 0):.2f}"
            })
    
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Results (CSV)",
        data=csv,
        file_name=f"benchmark_results_{result['matrix_size']}.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    
    # Visualizations
    st.header("Performance Visualizations")
    
    # Prepare data for visualization
    viz_data = parse_benchmark_results(result)
    
    # Execution time comparison
    st.subheader("Execution Time Comparison")
    fig_time = create_execution_time_chart(viz_data)
    st.plotly_chart(fig_time, use_container_width=True)
    
    st.markdown("---")
    
    # Speedup chart
    st.subheader("Speedup Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_speedup = create_speedup_chart(viz_data)
        st.plotly_chart(fig_speedup, use_container_width=True)
    
    with col2:
        # Efficiency chart
        fig_eff = create_efficiency_chart(viz_data)
        st.plotly_chart(fig_eff, use_container_width=True)
    
    st.markdown("---")
    
    # Analysis insights
    st.header("Performance Insights")
    
    # Serial vs best parallel
    serial_time = result["tests"]["serial"]["execution_time"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Multi-Node vs Single-Node")
        
        if "multi_node" in result["tests"] and "single_node" in result["tests"]:
            multi_time = result["tests"]["multi_node"]["execution_time"]
            single_time = result["tests"]["single_node"]["execution_time"]
            
            if multi_time < single_time:
                improvement = ((single_time - multi_time) / single_time) * 100
                st.success(f"Multi-Node is {improvement:.1f}% faster than Single-Node")
                st.info("Multi-node architecture provides better performance for this workload due to distributed memory and reduced communication overhead per node.")
            else:
                difference = ((multi_time - single_time) / single_time) * 100
                st.warning(f"Single-Node is {difference:.1f}% faster than Multi-Node")
                st.info("For this matrix size, communication overhead between nodes may exceed distribution benefits. Consider larger matrices.")
    
    with col2:
        st.markdown("### Parallel vs Serial")
        
        if best_speedup > 1:
            time_saved = serial_time - (serial_time / best_speedup)
            st.success(f"Parallel processing saved {time_saved:.2f} seconds")
            st.info(f"Using {result['num_processes']} processes achieved {best_speedup:.2f}x speedup.")
        else:
            st.warning("No speedup achieved - serial execution was faster")
    
    st.markdown("---")
    
    # Recommendations
    st.header("Recommendations")
    
    if best_speedup < 2:
        st.warning("""
        **Low Speedup Detected**
        
        Possible causes:
        - Matrix size too small (communication overhead dominates)
        - Increase matrix size to 2000+ for better parallel efficiency
        - Verify all cluster nodes are operational
        """)
    elif avg_eff < 0.5:
        st.info("""
        **Low Parallel Efficiency**
        
        Suggestions:
        - Reduce number of processes for better efficiency
        - Increase problem size to improve computation/communication ratio
        - Check network latency between nodes
        """)
    else:
        st.success("""
        **Good Performance**
        
        System is performing well. Consider:
        - Testing with larger matrices
        - Exploring different process configurations
        - Evaluating alternative algorithms
        """)

else:
    # Single result
    st.header("Single Benchmark Result")
    
    if result.get("success"):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Execution Time", f"{result['execution_time']:.4f}s")
        with col2:
            st.metric("Mode", result['mode'].replace('_', ' ').title())
        with col3:
            st.metric("Matrix Size", f"{result['matrix_size']}×{result['matrix_size']}")
        with col4:
            st.metric("Processes", result.get('num_processes', 1))
        
        st.info("Run a comparison benchmark to analyze performance differences between execution modes.")
        
        if st.button("Run Comparison Benchmark", type="primary"):
            st.switch_page("pages/2_⚡_Run_Benchmark.py")

st.markdown("---")

# Footer with action buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Run New Benchmark", use_container_width=True):
        st.switch_page("pages/2_⚡_Run_Benchmark.py")

with col2:
    if st.button("Back to Overview", use_container_width=True):
        st.switch_page("pages/1_🏠_Overview.py")

with col3:
    if st.button("View Documentation", use_container_width=True):
        st.switch_page("pages/6_📚_Documentation.py")
