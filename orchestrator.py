"""
Top-level orchestrator for parallel-bench.
Runs benchmarks across frameworks and saves results.
"""

from src.runners.wgpu_runner import WGPURunner
from src.runners.omp_runner import OMPRunner

def main():
    sizes = [1_000_000, 5_000_000, 10_000_000]

    wgpu = WGPURunner()
    omp = OMPRunner()

    wgpu.build()
    omp.build()

    # header
    print(f"{'N':>12} | {'WGPU (ms)':>10} | {'OpenMP (ms)':>11}")
    print("-" * 39)

    for N in sizes:
        wgpu_ms = wgpu.run(N)
        omp_ms  = omp.run(N)
        print(f"{N:>12,d} | {wgpu_ms:>10} | {omp_ms:>11}")

if __name__ == "__main__":
    main()