"""
Top-level orchestrator for parallel-bench.
Runs benchmarks across frameworks and saves results.
"""

from src.runners.wgpu_runner import WGPURunner
from src.runners.omp_runner import OMPRunner
import time

def main():
    sizes = [1_000_000, 5_000_000, 10_000_000]

    llvmpipe = WGPURunner(backend="llvmpipe")
    swiftshader = WGPURunner(backend="swiftshader")
    omp = OMPRunner()

    llvmpipe.build()
    swiftshader.build()
    omp.build()

    # header
    print(f"{'N':>12} | {'LLVMPipe (ms)':>15} | {'SwiftShader (ms)':>15} | {'OpenMP (ms)':>15}")
    print("-" * (12 + 3 + 15 + 3 + 15 + 3 + 15))

    for N in sizes:
        llvmpipe_ms = llvmpipe.run(N)
        time.sleep(1)
        swiftshader_ms = swiftshader.run(N)
        time.sleep(1)
        omp_ms  = omp.run(N)
        print(f"{N:>12,d} | {llvmpipe_ms:>15} | {swiftshader_ms:>15} | {omp_ms:>15}")

if __name__ == "__main__":
    main()