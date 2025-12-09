"""
Benchmark Runner Utilities
Execute and manage benchmark tests on the HPC cluster
"""

import subprocess
import time
import json
import re
from pathlib import Path
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)


class BenchmarkRunner:
    """Handles execution of benchmark tests"""
    
    def __init__(self, docker_manager):
        """Initialize with Docker manager"""
        self.docker_manager = docker_manager
        self.results_dir = Path("data/results")
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    def compile_code(self, algorithm: str, container: str = "hpchead") -> tuple:
        """Compile C code for the specified algorithm"""
        compile_commands = {
            "matrix_multiplication": "mpicc -o /home/faiz/matrix /home/faiz/matrix.c -lm",
            "serial": "gcc -o /home/faiz/serial /home/faiz/serial.c",
        }
        
        if algorithm not in compile_commands:
            return False, f"Unknown algorithm: {algorithm}"
        
        cmd = compile_commands[algorithm]
        exit_code, output = self.docker_manager.execute_command(container, cmd)
        
        if exit_code == 0:
            return True, "Compilation successful"
        else:
            return False, f"Compilation failed: {output}"
    
    def run_serial_benchmark(self, matrix_size: int) -> Dict:
        """Run serial benchmark"""
        logger.info(f"Running serial benchmark with matrix size {matrix_size}")
        
        # Compile serial code
        success, msg = self.compile_code("serial")
        if not success:
            return {"success": False, "error": msg}
        
        # Run benchmark
        cmd = f"/home/faiz/serial {matrix_size}"
        start_time = time.time()
        exit_code, output = self.docker_manager.execute_command("hpchead", cmd)
        end_time = time.time()
        
        if exit_code != 0:
            return {"success": False, "error": output}
        
        # Parse output
        result = self._parse_output(output)
        result.update({
            "success": True,
            "mode": "serial",
            "algorithm": "matrix_multiplication",
            "matrix_size": matrix_size,
            "num_processes": 1,
            "timestamp": time.time()
        })
        
        return result
    
    def run_parallel_benchmark(
        self, 
        matrix_size: int, 
        num_processes: int,
        mode: str = "single_node"
    ) -> Dict:
        """Run parallel benchmark with MPI"""
        logger.info(f"Running parallel benchmark: size={matrix_size}, procs={num_processes}, mode={mode}")
        
        # Compile parallel code
        success, msg = self.compile_code("matrix_multiplication")
        if not success:
            return {"success": False, "error": msg}
        
        # Build MPI command based on mode
        if mode == "single_node":
            mpi_cmd = f"mpirun -np {num_processes} --host hpchead /home/faiz/matrix {matrix_size}"
        else:  # multi_node
            # Distribute across nodes
            hosts = self._generate_hostlist(num_processes)
            mpi_cmd = f"mpirun -np {num_processes} {hosts} /home/faiz/matrix {matrix_size}"
        
        # Run benchmark
        start_time = time.time()
        exit_code, output = self.docker_manager.execute_command("hpchead", mpi_cmd)
        end_time = time.time()
        
        if exit_code != 0:
            return {"success": False, "error": output}
        
        # Parse output
        result = self._parse_output(output)
        result.update({
            "success": True,
            "mode": mode,
            "algorithm": "matrix_multiplication",
            "matrix_size": matrix_size,
            "num_processes": num_processes,
            "timestamp": time.time()
        })
        
        return result
    
    def run_comparison(self, matrix_size: int, num_processes: int = 4) -> Dict:
        """Run comparison between serial, single-node, and multi-node"""
        results = {
            "matrix_size": matrix_size,
            "num_processes": num_processes,
            "tests": {}
        }
        
        # Run serial
        results["tests"]["serial"] = self.run_serial_benchmark(matrix_size)
        
        # Run single-node parallel
        results["tests"]["single_node"] = self.run_parallel_benchmark(
            matrix_size, num_processes, "single_node"
        )
        
        # Run multi-node parallel
        results["tests"]["multi_node"] = self.run_parallel_benchmark(
            matrix_size, num_processes, "multi_node"
        )
        
        # Calculate speedups
        if results["tests"]["serial"]["success"]:
            serial_time = results["tests"]["serial"]["execution_time"]
            
            for mode in ["single_node", "multi_node"]:
                if results["tests"][mode]["success"]:
                    parallel_time = results["tests"][mode]["execution_time"]
                    speedup = serial_time / parallel_time
                    efficiency = speedup / num_processes
                    results["tests"][mode]["speedup"] = speedup
                    results["tests"][mode]["efficiency"] = efficiency
        
        return results
    
    def _generate_hostlist(self, num_processes: int) -> str:
        """Generate MPI host list for multi-node execution"""
        nodes = ["hpchead", "node01", "node02", "node03"]
        procs_per_node = max(1, num_processes // len(nodes))
        
        hostlist = []
        for node in nodes[:min(len(nodes), num_processes)]:
            hostlist.append(f"{node}:{procs_per_node}")
        
        return "--host " + ",".join(hostlist)
    
    def _parse_output(self, output: str) -> Dict:
        """Parse benchmark output to extract metrics"""
        result = {
            "execution_time": 0.0,
            "gflops": 0.0,
            "memory_mb": 0.0,
            "raw_output": output
        }
        
        # Extract execution time
        time_match = re.search(r'Total Time Elapsed is ([\d.]+) seconds', output)
        if time_match:
            result["execution_time"] = float(time_match.group(1))
        
        # Extract GFLOPS (if available)
        gflops_match = re.search(r'GFLOPS: ([\d.]+)', output)
        if gflops_match:
            result["gflops"] = float(gflops_match.group(1))
        
        # Extract memory usage (if available)
        mem_match = re.search(r'Memory: ([\d.]+) MB', output)
        if mem_match:
            result["memory_mb"] = float(mem_match.group(1))
        
        return result
    
    def save_results(self, results: Dict, filename: Optional[str] = None):
        """Save benchmark results to JSON file"""
        if filename is None:
            filename = f"benchmark_{int(time.time())}.json"
        
        filepath = self.results_dir / filename
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Results saved to {filepath}")
        return filepath
    
    def load_results(self, filename: str) -> Dict:
        """Load benchmark results from JSON file"""
        filepath = self.results_dir / filename
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def list_results(self) -> List[str]:
        """List all saved result files"""
        return [f.name for f in self.results_dir.glob("*.json")]
