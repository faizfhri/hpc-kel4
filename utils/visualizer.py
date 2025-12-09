"""
Data Processing and Visualization Utilities
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List
import json


def parse_benchmark_results(results: Dict) -> pd.DataFrame:
    """Convert benchmark results dictionary to DataFrame"""
    rows = []
    
    if "tests" in results:
        # Comparison results
        for mode, data in results["tests"].items():
            if data.get("success"):
                row = {
                    "mode": mode,
                    "matrix_size": results.get("matrix_size"),
                    "num_processes": data.get("num_processes", 1),
                    "execution_time": data.get("execution_time"),
                    "speedup": data.get("speedup", 1.0),
                    "efficiency": data.get("efficiency", 1.0),
                    "gflops": data.get("gflops", 0.0),
                    "memory_mb": data.get("memory_mb", 0.0)
                }
                rows.append(row)
    else:
        # Single result
        row = {
            "mode": results.get("mode"),
            "matrix_size": results.get("matrix_size"),
            "num_processes": results.get("num_processes", 1),
            "execution_time": results.get("execution_time"),
            "speedup": results.get("speedup", 1.0),
            "efficiency": results.get("efficiency", 1.0),
            "gflops": results.get("gflops", 0.0),
            "memory_mb": results.get("memory_mb", 0.0)
        }
        rows.append(row)
    
    return pd.DataFrame(rows)


def create_speedup_chart(df: pd.DataFrame) -> go.Figure:
    """Create speedup comparison chart"""
    fig = go.Figure()
    
    modes = df['mode'].unique()
    colors = {'serial': '#636EFA', 'single_node': '#EF553B', 'multi_node': '#00CC96'}
    
    for mode in modes:
        mode_data = df[df['mode'] == mode]
        fig.add_trace(go.Bar(
            name=mode.replace('_', ' ').title(),
            x=mode_data['matrix_size'],
            y=mode_data['speedup'],
            marker_color=colors.get(mode, '#AB63FA')
        ))
    
    fig.update_layout(
        title="Speedup Comparison",
        xaxis_title="Matrix Size",
        yaxis_title="Speedup (vs Serial)",
        barmode='group',
        template='plotly_white',
        height=400
    )
    
    return fig


def create_execution_time_chart(df: pd.DataFrame) -> go.Figure:
    """Create execution time comparison chart"""
    fig = go.Figure()
    
    modes = df['mode'].unique()
    colors = {'serial': '#636EFA', 'single_node': '#EF553B', 'multi_node': '#00CC96'}
    
    for mode in modes:
        mode_data = df[df['mode'] == mode]
        fig.add_trace(go.Scatter(
            name=mode.replace('_', ' ').title(),
            x=mode_data['matrix_size'],
            y=mode_data['execution_time'],
            mode='lines+markers',
            line=dict(color=colors.get(mode, '#AB63FA'), width=3),
            marker=dict(size=10)
        ))
    
    fig.update_layout(
        title="Execution Time Comparison",
        xaxis_title="Matrix Size",
        yaxis_title="Time (seconds)",
        template='plotly_white',
        height=400,
        hovermode='x unified'
    )
    
    return fig


def create_efficiency_chart(df: pd.DataFrame) -> go.Figure:
    """Create parallel efficiency chart"""
    parallel_data = df[df['mode'] != 'serial']
    
    fig = px.bar(
        parallel_data,
        x='matrix_size',
        y='efficiency',
        color='mode',
        barmode='group',
        title='Parallel Efficiency',
        labels={'efficiency': 'Efficiency', 'matrix_size': 'Matrix Size'},
        color_discrete_map={'single_node': '#EF553B', 'multi_node': '#00CC96'}
    )
    
    fig.update_layout(
        template='plotly_white',
        height=400,
        yaxis_range=[0, 1.1]
    )
    
    # Add ideal efficiency line
    fig.add_hline(y=1.0, line_dash="dash", line_color="gray", 
                  annotation_text="Ideal Efficiency")
    
    return fig


def create_memory_chart(df: pd.DataFrame) -> go.Figure:
    """Create memory usage comparison chart"""
    fig = go.Figure()
    
    modes = df['mode'].unique()
    colors = {'serial': '#636EFA', 'single_node': '#EF553B', 'multi_node': '#00CC96'}
    
    for mode in modes:
        mode_data = df[df['mode'] == mode]
        fig.add_trace(go.Bar(
            name=mode.replace('_', ' ').title(),
            x=mode_data['matrix_size'],
            y=mode_data['memory_mb'],
            marker_color=colors.get(mode, '#AB63FA')
        ))
    
    fig.update_layout(
        title="Memory Usage Comparison",
        xaxis_title="Matrix Size",
        yaxis_title="Memory (MB)",
        barmode='group',
        template='plotly_white',
        height=400
    )
    
    return fig


def calculate_metrics_summary(df: pd.DataFrame) -> Dict:
    """Calculate summary metrics"""
    summary = {
        "best_speedup": df['speedup'].max(),
        "avg_speedup": df[df['mode'] != 'serial']['speedup'].mean(),
        "best_efficiency": df['efficiency'].max(),
        "avg_efficiency": df[df['mode'] != 'serial']['efficiency'].mean(),
        "total_tests": len(df),
        "avg_execution_time": df['execution_time'].mean()
    }
    return summary
