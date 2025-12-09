# HPC Benchmark Results Directory

This directory stores benchmark result files in JSON format.

## File Structure

Result files are named: `benchmark_<timestamp>.json`

Example: `benchmark_1733123456.json`

## JSON Format

```json
{
  "matrix_size": 1000,
  "num_processes": 4,
  "tests": {
    "serial": {
      "success": true,
      "execution_time": 18.5,
      "mode": "serial",
      "num_processes": 1
    },
    "single_node": {
      "success": true,
      "execution_time": 5.2,
      "speedup": 3.56,
      "efficiency": 0.89,
      "mode": "single_node",
      "num_processes": 4
    },
    "multi_node": {
      "success": true,
      "execution_time": 5.8,
      "speedup": 3.19,
      "efficiency": 0.80,
      "mode": "multi_node",
      "num_processes": 4
    }
  }
}
```

## Usage

Results are automatically saved here when running benchmarks with the "Save results" option enabled.

You can load and analyze saved results from the "📈 Results & Analysis" page.
